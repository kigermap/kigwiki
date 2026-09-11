from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
CENSUS_ASSET_DIR = DOCS_DIR / "assets" / "images" / "kigurumi-census-2017"
CENSUS_MANIFEST = CENSUS_ASSET_DIR / "manifest.tsv"
CENSUS_REPORT_GLOB = "*/sources/survey-reports/kigurumi-census-2017/index.md"
FIGURE_PATTERN = re.compile(r"figure-(\d{3})\.png")
REPORT_PATTERN = re.compile(r"^docs/(?P<locale>[^/]+)/sources/survey-reports/(?P<slug>[^/]+)/index\.md$")
ARCHIVE_LOCALES = {
    "zh-Hans": {"zh-CN"},
    "zh-Hant": {"zh-Hant", "zh-TW"},
    "en": {"en"},
    "ja": {"ja"},
    "ru": {"ru"},
}
ARCHIVE_SECTIONS = {
    "years": re.compile(r"^\d{4}$"),
    "digests": re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])$"),
}
# These English annual pages intentionally use mkdocs-static-i18n's default-language fallback.
ARCHIVE_LOCALE_FALLBACKS = {
    ("years", "2023", "en"),
    ("years", "2024", "en"),
    ("years", "2025", "en"),
}
FRONT_MATTER_FIELDS = {"title", "date", "language", "status"}


@dataclass
class ReportIndexEntry:
    locale: str
    slug: str
    path: str
    title: str
    figure_count: int


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _read_manifest() -> list[dict[str, str]]:
    if not CENSUS_MANIFEST.exists():
        raise FileNotFoundError(f"Missing manifest: {_relative(CENSUS_MANIFEST)}")

    with CENSUS_MANIFEST.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    required = {"figure", "page", "image_index", "width", "height", "source_bytes", "file"}
    if not rows:
        raise ValueError(f"Manifest is empty: {_relative(CENSUS_MANIFEST)}")
    missing_columns = required - set(rows[0])
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Manifest missing columns: {missing}")
    return rows


def _report_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.parent.name


def _validate_census_report_indexes() -> list[ReportIndexEntry]:
    rows = _read_manifest()
    manifest_files = [row["file"] for row in rows]
    expected_files = {f"figure-{index:03d}.png" for index in range(1, len(rows) + 1)}
    actual_files = {path.name for path in CENSUS_ASSET_DIR.glob("figure-*.png")}

    errors: list[str] = []
    if set(manifest_files) != expected_files:
        missing = sorted(expected_files - set(manifest_files))
        extra = sorted(set(manifest_files) - expected_files)
        if missing:
            errors.append(f"Manifest missing figures: {', '.join(missing[:8])}")
        if extra:
            errors.append(f"Manifest has unexpected figures: {', '.join(extra[:8])}")

    missing_assets = sorted(set(manifest_files) - actual_files)
    extra_assets = sorted(actual_files - set(manifest_files))
    if missing_assets:
        errors.append(f"Missing figure files: {', '.join(missing_assets[:8])}")
    if extra_assets:
        errors.append(f"Unexpected figure files: {', '.join(extra_assets[:8])}")

    entries: list[ReportIndexEntry] = []
    report_paths = sorted(DOCS_DIR.glob(CENSUS_REPORT_GLOB))
    if not report_paths:
        errors.append("No census report pages found")

    for path in report_paths:
        relative_path = _relative(path)
        match = REPORT_PATTERN.match(relative_path)
        if not match:
            errors.append(f"Unexpected report path: {relative_path}")
            continue

        content = path.read_text(encoding="utf-8")
        figures = FIGURE_PATTERN.findall(content)
        unique_figures = {f"figure-{number}.png" for number in figures}
        if unique_figures != set(manifest_files):
            missing = sorted(set(manifest_files) - unique_figures)
            extra = sorted(unique_figures - set(manifest_files))
            if missing:
                errors.append(f"{relative_path} missing figures: {', '.join(missing[:8])}")
            if extra:
                errors.append(f"{relative_path} has unexpected figures: {', '.join(extra[:8])}")

        entries.append(
            ReportIndexEntry(
                locale=match.group("locale"),
                slug=match.group("slug"),
                path=relative_path,
                title=_report_title(path),
                figure_count=len(unique_figures),
            )
        )

    if errors:
        raise ValueError("\n".join(errors))
    return entries


def _front_matter(path: Path) -> tuple[dict[str, str], str]:
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{_relative(path)} has no YAML front matter")

    try:
        closing_index = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError(f"{_relative(path)} has unclosed YAML front matter") from exc

    metadata: dict[str, str] = {}
    for line in lines[1:closing_index]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{_relative(path)} has invalid front matter line: {line}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("'\"")
    return metadata, "\n".join(lines[closing_index + 1 :])


def _validate_archive_page(path: Path, locale: str, section: str, slug: str) -> list[str]:
    errors: list[str] = []
    try:
        metadata, body = _front_matter(path)
    except ValueError as exc:
        return [str(exc)]

    missing_fields = sorted(FRONT_MATTER_FIELDS - set(metadata))
    if missing_fields:
        errors.append(f"{_relative(path)} missing front matter: {', '.join(missing_fields)}")

    expected_languages = ARCHIVE_LOCALES[locale]
    if metadata.get("language") not in expected_languages:
        errors.append(
            f"{_relative(path)} language is {metadata.get('language')!r}; "
            f"expected one of {sorted(expected_languages)!r}"
        )

    try:
        date.fromisoformat(metadata.get("date", ""))
    except ValueError:
        errors.append(f"{_relative(path)} has invalid ISO date: {metadata.get('date')!r}")

    if not metadata.get("title", "").strip():
        errors.append(f"{_relative(path)} has an empty title")
    if not metadata.get("status", "").strip():
        errors.append(f"{_relative(path)} has an empty status")
    title = metadata.get("title", "")
    if section == "years" and slug not in title:
        errors.append(f"{_relative(path)} title does not include archive slug {slug}")
    if section == "digests" and slug[:4] not in title:
        errors.append(f"{_relative(path)} title does not include digest year {slug[:4]}")

    headings = re.findall(r"^#\s+\S.*$", body, flags=re.MULTILINE)
    if len(headings) != 1:
        errors.append(f"{_relative(path)} must contain exactly one Markdown H1; found {len(headings)}")
    if section == "years":
        obsolete_heading = re.compile(
            r"去重|重複(?:排除|除去|整理|表)|de-?duplicat|"
            r"(?:исключение|устранение|удаление) повторов", re.IGNORECASE
        )
        for heading in re.findall(r"^#{2,6} .+$", body, flags=re.MULTILINE):
            if obsolete_heading.search(heading):
                errors.append(f"{_relative(path)} has an obsolete comparison section: {heading}")
        for label in set(re.findall(r"\[\^([^\]]+)\](?!:)", body)):
            if not re.search(r"^\[\^" + re.escape(label) + r"\]:", body, flags=re.MULTILINE):
                errors.append(f"{_relative(path)} has an undefined footnote: {label}")
        for anchor in set(re.findall(r"\]\(#(s\d+)\)", body)):
            if f'id="{anchor}"' not in body:
                errors.append(f"{_relative(path)} has an undefined source anchor: {anchor}")
    return errors


def _index_contains(index_path: Path, section: str, slug: str) -> bool:
    content = index_path.read_text(encoding="utf-8")
    if section == "years" and index_path.parent.name == "chronicle":
        candidates = (f'href="../years/{slug}/"', f"(../years/{slug}/index.md)")
    else:
        candidates = (f'href="{slug}/"', f"({slug}/index.md)")
    return any(candidate in content for candidate in candidates)


def _validate_archive_locales() -> tuple[int, int, int]:
    errors: list[str] = []
    fallback_count = 0
    config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    totals: dict[str, int] = {}

    for section, slug_pattern in ARCHIVE_SECTIONS.items():
        default_slugs = {
            path.parent.name
            for path in (DOCS_DIR / "zh-Hans" / section).glob("*/index.md")
            if slug_pattern.fullmatch(path.parent.name)
        }
        if not default_slugs:
            errors.append(f"No default-language {section} pages found")
            continue
        totals[section] = len(default_slugs)

        for locale in ARCHIVE_LOCALES:
            locale_dir = DOCS_DIR / locale / section
            locale_slugs = {
                path.parent.name
                for path in locale_dir.glob("*/index.md")
                if slug_pattern.fullmatch(path.parent.name)
            }
            unexpected = sorted(locale_slugs - default_slugs)
            if unexpected:
                errors.append(f"{locale}/{section} has unexpected slugs: {', '.join(unexpected)}")

            for slug in sorted(default_slugs):
                page_path = locale_dir / slug / "index.md"
                if not page_path.exists():
                    fallback = (section, slug, locale)
                    if fallback in ARCHIVE_LOCALE_FALLBACKS:
                        fallback_count += 1
                        continue
                    errors.append(f"Missing localized archive page: {_relative(page_path)}")
                    continue
                errors.extend(_validate_archive_page(page_path, locale, section, slug))

                index_path = locale_dir / "index.md"
                if not _index_contains(index_path, section, slug):
                    errors.append(f"{_relative(index_path)} does not link to {slug}")
                if section == "years":
                    chronicle_index = DOCS_DIR / locale / "chronicle" / "index.md"
                    if not _index_contains(chronicle_index, section, slug):
                        errors.append(f"{_relative(chronicle_index)} does not link to {slug}")

        for slug in sorted(default_slugs):
            nav_path = f"{section}/{slug}/index.md"
            nav_count = config.count(nav_path)
            declared_fallbacks = sum(
                (section, slug, locale) in ARCHIVE_LOCALE_FALLBACKS for locale in ARCHIVE_LOCALES
            )
            expected_nav_count = len(ARCHIVE_LOCALES) + 1 - declared_fallbacks
            if nav_count != expected_nav_count:
                errors.append(
                    f"mkdocs.yml contains {nav_count} entries for {nav_path}; "
                    f"expected {expected_nav_count}"
                )

    if errors:
        raise ValueError("\n".join(errors))
    return totals.get("years", 0), totals.get("digests", 0), fallback_count


def _write_json_index(entries: list[ReportIndexEntry]) -> Path:
    output_path = DOCS_DIR / "assets" / "generated" / "source-report-index.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_by": "scripts/build_indexes.py",
        "reports": [asdict(entry) for entry in entries],
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and optionally generate archive helper indexes.")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write docs/assets/generated/source-report-index.json after validation.",
    )
    args = parser.parse_args()

    try:
        entries = _validate_census_report_indexes()
        print(f"Validated {len(entries)} census report pages and {len(_read_manifest())} figures.")
        year_count, digest_count, fallback_count = _validate_archive_locales()
        print(
            f"Validated {year_count} annual and {digest_count} monthly archive slugs across "
            f"{len(ARCHIVE_LOCALES)} locales ({fallback_count} declared fallbacks)."
        )
        if args.write:
            output_path = _write_json_index(entries)
            print(f"Wrote {_relative(output_path)}.")
    except Exception as exc:
        print(f"build_indexes.py: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
