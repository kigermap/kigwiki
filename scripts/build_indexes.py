from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
GENERATED_DIR = DOCS_DIR / "generated"


def load_yaml(name: str) -> list[dict[str, Any]]:
    path = DATA_DIR / name
    if not path.exists():
        return []
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    if isinstance(value, dict):
        value = value.get("items", [])
    if not isinstance(value, list):
        raise TypeError(f"{path} must contain a list or an items list")
    return value


def by_id(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in items if item.get("id")}


def clean_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(clean_cell(item) for item in value)
    text = str(value).strip()
    return text.replace("\n", "<br>").replace("|", "\\|")


def first_year(value: str) -> str:
    match = re.search(r"(?<!\d)(-?\d{1,4})(?!\d)", value or "")
    if not match:
        return "未定年"
    year = int(match.group(1))
    return f"{year:04d}" if year >= 0 else str(year)


def event_year(event: dict[str, Any]) -> str:
    return first_year(str(event.get("sort_date") or event.get("date") or ""))


def event_sort_key(event: dict[str, Any]) -> tuple[str, str]:
    sort_date = str(event.get("sort_date") or event.get("date") or "")
    year = event_year(event)
    normalized = sort_date if re.match(r"^-?\d{1,4}(-\d{2}){0,2}$", sort_date) else year
    return normalized, str(event.get("title") or "")


def display_ref(
    item_id: str,
    lookup: dict[str, dict[str, Any]],
    fallback_field: str,
) -> str:
    item = lookup.get(item_id)
    if not item:
        return item_id
    label = item.get("name") or item.get("title") or item_id
    file_path = item.get("file")
    if file_path:
        return f"[{label}](../{file_path})"
    return str(label)


def display_refs(
    item_ids: list[str] | None,
    lookup: dict[str, dict[str, Any]],
    fallback_field: str = "name",
) -> str:
    if not item_ids:
        return ""
    return ", ".join(display_ref(item_id, lookup, fallback_field) for item_id in item_ids)


def source_refs(source_ids: list[str] | None, source_lookup: dict[str, dict[str, Any]]) -> str:
    if not source_ids:
        return ""
    labels = []
    for source_id in source_ids:
        source = source_lookup.get(source_id)
        labels.append(source.get("short_title") or source.get("title") or source_id if source else source_id)
    return ", ".join(labels)


def write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.rstrip() + "\n", encoding="utf-8")


def events_table(
    events: list[dict[str, Any]],
    people_lookup: dict[str, dict[str, Any]],
    place_lookup: dict[str, dict[str, Any]],
    source_lookup: dict[str, dict[str, Any]],
) -> str:
    lines = [
        "| 时间 | 事件 | 类别 | 人物 | 地点 | 来源 | 可信度 | 摘要 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for event in sorted(events, key=event_sort_key):
        lines.append(
            "| {date} | {title} | {category} | {people} | {places} | {sources} | {confidence} | {summary} |".format(
                date=clean_cell(event.get("date")),
                title=clean_cell(event.get("title")),
                category=clean_cell(event.get("category")),
                people=clean_cell(display_refs(event.get("people"), people_lookup)),
                places=clean_cell(display_refs(event.get("places"), place_lookup)),
                sources=clean_cell(source_refs(event.get("sources"), source_lookup)),
                confidence=clean_cell(event.get("confidence")),
                summary=clean_cell(event.get("summary")),
            )
        )
    return "\n".join(lines)


def build(root: Path = ROOT) -> None:
    del root
    events = load_yaml("events.yml")
    people = load_yaml("people.yml")
    places = load_yaml("places.yml")
    sources = load_yaml("sources.yml")

    people_lookup = by_id(people)
    place_lookup = by_id(places)
    source_lookup = by_id(sources)

    write(
        GENERATED_DIR / "events.md",
        "# 全量大事记\n\n"
        "本页由 `data/events.yml` 自动生成。修改结构化事件后，运行 `python scripts/build_indexes.py` 更新。\n\n"
        + events_table(events, people_lookup, place_lookup, source_lookup),
    )

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        grouped[event_year(event)].append(event)
    year_sections = ["# 按年份\n\n本页由 `data/events.yml` 自动生成。\n"]
    for year in sorted(grouped):
        year_sections.append(f"\n## {year}\n")
        year_sections.append(events_table(grouped[year], people_lookup, place_lookup, source_lookup))
    write(GENERATED_DIR / "events-by-year.md", "\n".join(year_sections))

    write(
        GENERATED_DIR / "people-index.md",
        "# 人物索引\n\n"
        "本页由 `data/people.yml` 和 `data/events.yml` 自动生成。\n\n"
        + index_table(people, "人物", events, "people"),
    )

    write(
        GENERATED_DIR / "places-index.md",
        "# 地点索引\n\n"
        "本页由 `data/places.yml` 和 `data/events.yml` 自动生成。\n\n"
        + index_table(places, "地点", events, "places"),
    )

    write(
        GENERATED_DIR / "sources-index.md",
        "# 来源索引\n\n"
        "本页由 `data/sources.yml` 和 `data/events.yml` 自动生成。\n\n"
        + source_table(sources, events),
    )


def index_table(items: list[dict[str, Any]], label: str, events: list[dict[str, Any]], field: str) -> str:
    lines = [
        f"| {label} | 类型 | 简介 | 关联事件数 |",
        "| --- | --- | --- | --- |",
    ]
    for item in sorted(items, key=lambda value: str(value.get("name") or value.get("title") or "")):
        item_id = item.get("id")
        event_count = sum(1 for event in events if item_id in (event.get(field) or []))
        name = item.get("name") or item.get("title") or item_id
        if item.get("file"):
            name = f"[{name}](../{item['file']})"
        lines.append(
            f"| {clean_cell(name)} | {clean_cell(item.get('type'))} | {clean_cell(item.get('summary'))} | {event_count} |"
        )
    return "\n".join(lines)


def source_table(sources: list[dict[str, Any]], events: list[dict[str, Any]]) -> str:
    lines = [
        "| 来源 | 类型 | 年份 | 馆藏/出处 | 关联事件数 | 引用格式 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for source in sorted(sources, key=lambda value: str(value.get("title") or "")):
        source_id = source.get("id")
        event_count = sum(1 for event in events if source_id in (event.get("sources") or []))
        lines.append(
            "| {title} | {type} | {year} | {holder} | {count} | {citation} |".format(
                title=clean_cell(source.get("title")),
                type=clean_cell(source.get("type")),
                year=clean_cell(source.get("year")),
                holder=clean_cell(source.get("holder")),
                count=event_count,
                citation=clean_cell(source.get("citation")),
            )
        )
    return "\n".join(lines)


if __name__ == "__main__":
    build()

