from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
CENSUS_ASSET_DIR = DOCS_DIR / "assets" / "images" / "kigurumi-census-2017"
CENSUS_MANIFEST = CENSUS_ASSET_DIR / "manifest.tsv"
CENSUS_REPORT_GLOB = "*/sources/survey-reports/kigurumi-census-2017/index.md"
FIGURE_PATTERN = re.compile(r"figure-(\d{3})\.png")
REPORT_PATTERN = re.compile(r"^docs/(?P<locale>[^/]+)/sources/survey-reports/(?P<slug>[^/]+)/index\.md$")


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
        if args.write:
            output_path = _write_json_index(entries)
            print(f"Wrote {_relative(output_path)}.")
    except Exception as exc:
        print(f"build_indexes.py: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
