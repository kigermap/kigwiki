from __future__ import annotations

import re
from html import escape
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
HIDE_TOC = "---\nhide:\n  - toc\n---\n\n"


LANGUAGES: dict[str, dict[str, Any]] = {
    "zh-Hans": {
        "fallback": "未分类",
        "search_label": "本页检索",
        "quick_filter": "快速筛选",
        "all": "全部",
        "uncertain_year": "未定年",
        "update_note": '修改结构化事件后，运行 <code>python scripts/build_indexes.py</code> 更新。',
        "events": {
            "kicker": "Chronicle Index",
            "title": "全量大事记",
            "summary": "本页由 `data/events.yml` 自动生成，集中展示已编目事件的时间、人物、地点、来源和可信度。",
            "panel_label": "结构化事件",
            "panel_summary": "按时间、类别、地点、来源与可信度扫描全部记录。",
            "placeholder": "筛选时间、事件、人物、地点或来源",
            "headers": ["时间", "事件", "类别", "人物", "地点", "来源", "可信度", "摘要"],
        },
        "events_by_year": {
            "kicker": "Yearly Chronicle",
            "title": "按年份",
            "summary": "本页由 `data/events.yml` 自动生成，把事件按年份分组，适合写年鉴、回顾和阶段性修订。",
            "panel_label": "年份分组",
            "panel_summary": "按年份拆分事件，便于回顾阶段变化和定位修订范围。",
            "placeholder": "筛选年份、事件、人物、地点或来源",
        },
        "people": {
            "kicker": "People Index",
            "title": "人物索引",
            "summary": "本页由 `data/people.yml` 和 `data/events.yml` 自动生成，用于核对公开身份、角色简介和关联事件数。",
            "panel_label": "公开人物",
            "panel_summary": "按公开身份、角色简介与关联事件数校对人物记录。",
            "placeholder": "筛选人物、类型或简介",
            "item_label": "人物",
            "headers": ["人物", "类型", "简介", "关联事件数"],
        },
        "places": {
            "kicker": "Place Index",
            "title": "地点索引",
            "summary": "本页由 `data/places.yml` 和 `data/events.yml` 自动生成，用于整理会馆、工坊、展陈空间和线上资料馆。",
            "panel_label": "地点条目",
            "panel_summary": "按空间类型与关联事件数整理线下据点、工坊、展陈空间和数字空间。",
            "placeholder": "筛选地点、类型或简介",
            "item_label": "地点",
            "headers": ["地点", "类型", "简介", "关联事件数"],
        },
        "sources": {
            "kicker": "Source Index",
            "title": "来源索引",
            "summary": "本页由 `data/sources.yml` 和 `data/events.yml` 自动生成，用于追踪来源类型、馆藏出处、引用格式和关联事件数。",
            "panel_label": "来源条目",
            "panel_summary": "按来源类型、年份、馆藏出处和引用格式追踪资料依据。",
            "placeholder": "筛选来源、年份、馆藏或引用格式",
            "headers": ["来源", "类型", "年份", "馆藏/出处", "关联事件数", "引用格式"],
        },
    },
    "zh-Hant": {
        "fallback": "未分類",
        "search_label": "本頁檢索",
        "quick_filter": "快速篩選",
        "all": "全部",
        "uncertain_year": "未定年",
        "update_note": '修改結構化事件後，執行 <code>python scripts/build_indexes.py</code> 更新。',
        "events": {
            "kicker": "Chronicle Index",
            "title": "全量大事記",
            "summary": "本頁由 `data/events.yml` 自動生成，集中展示已編目事件的時間、人物、地點、來源和可信度。",
            "panel_label": "結構化事件",
            "panel_summary": "按時間、類別、地點、來源與可信度掃描全部記錄。",
            "placeholder": "篩選時間、事件、人物、地點或來源",
            "headers": ["時間", "事件", "類別", "人物", "地點", "來源", "可信度", "摘要"],
        },
        "events_by_year": {
            "kicker": "Yearly Chronicle",
            "title": "按年份",
            "summary": "本頁由 `data/events.yml` 自動生成，把事件按年份分組，適合寫年鑑、回顧和階段性修訂。",
            "panel_label": "年份分組",
            "panel_summary": "按年份拆分事件，便於回顧階段變化和定位修訂範圍。",
            "placeholder": "篩選年份、事件、人物、地點或來源",
        },
        "people": {
            "kicker": "People Index",
            "title": "人物索引",
            "summary": "本頁由 `data/people.yml` 和 `data/events.yml` 自動生成，用於核對公開身份、角色簡介和關聯事件數。",
            "panel_label": "公開人物",
            "panel_summary": "按公開身份、角色簡介與關聯事件數校對人物記錄。",
            "placeholder": "篩選人物、類型或簡介",
            "item_label": "人物",
            "headers": ["人物", "類型", "簡介", "關聯事件數"],
        },
        "places": {
            "kicker": "Place Index",
            "title": "地點索引",
            "summary": "本頁由 `data/places.yml` 和 `data/events.yml` 自動生成，用於整理會館、工坊、展陳空間和線上資料館。",
            "panel_label": "地點條目",
            "panel_summary": "按空間類型與關聯事件數整理線下據點、工坊、展陳空間和數位空間。",
            "placeholder": "篩選地點、類型或簡介",
            "item_label": "地點",
            "headers": ["地點", "類型", "簡介", "關聯事件數"],
        },
        "sources": {
            "kicker": "Source Index",
            "title": "來源索引",
            "summary": "本頁由 `data/sources.yml` 和 `data/events.yml` 自動生成，用於追蹤來源類型、館藏出處、引用格式和關聯事件數。",
            "panel_label": "來源條目",
            "panel_summary": "按來源類型、年份、館藏出處和引用格式追蹤資料依據。",
            "placeholder": "篩選來源、年份、館藏或引用格式",
            "headers": ["來源", "類型", "年份", "館藏/出處", "關聯事件數", "引用格式"],
        },
    },
    "en": {
        "fallback": "Uncategorized",
        "search_label": "Search this page",
        "quick_filter": "Quick filters",
        "all": "All",
        "uncertain_year": "Unknown year",
        "update_note": 'After editing structured events, run <code>python scripts/build_indexes.py</code> to refresh these pages.',
        "events": {
            "kicker": "Chronicle Index",
            "title": "Event Index",
            "summary": "Generated from `data/events.yml`, this page lists cataloged events with dates, people, places, sources, and confidence notes.",
            "panel_label": "Structured events",
            "panel_summary": "Scan every record by date, category, place, source, and confidence.",
            "placeholder": "Filter by date, event, person, place, or source",
            "headers": ["Date", "Event", "Category", "People", "Places", "Sources", "Confidence", "Summary"],
        },
        "events_by_year": {
            "kicker": "Yearly Chronicle",
            "title": "By Year",
            "summary": "Generated from `data/events.yml`, this page groups events by year for annual reviews and staged revisions.",
            "panel_label": "Year groups",
            "panel_summary": "Split events by year to review phases and locate revision ranges.",
            "placeholder": "Filter by year, event, person, place, or source",
        },
        "people": {
            "kicker": "People Index",
            "title": "People Index",
            "summary": "Generated from `data/people.yml` and `data/events.yml`, this page checks public identities, role summaries, and related event counts.",
            "panel_label": "Public people",
            "panel_summary": "Review people records by public identity, role summary, and related event count.",
            "placeholder": "Filter by person, type, or summary",
            "item_label": "Person",
            "headers": ["Person", "Type", "Summary", "Related Events"],
        },
        "places": {
            "kicker": "Place Index",
            "title": "Places Index",
            "summary": "Generated from `data/places.yml` and `data/events.yml`, this page organizes halls, studios, exhibition spaces, and online archives.",
            "panel_label": "Place entries",
            "panel_summary": "Organize physical sites, studios, exhibition spaces, and digital spaces by type and related event count.",
            "placeholder": "Filter by place, type, or summary",
            "item_label": "Place",
            "headers": ["Place", "Type", "Summary", "Related Events"],
        },
        "sources": {
            "kicker": "Source Index",
            "title": "Sources Index",
            "summary": "Generated from `data/sources.yml` and `data/events.yml`, this page tracks source type, holding location, citation format, and related event count.",
            "panel_label": "Source entries",
            "panel_summary": "Track source evidence by type, year, holding location, and citation format.",
            "placeholder": "Filter by source, year, holding, or citation",
            "headers": ["Source", "Type", "Year", "Holding", "Related Events", "Citation"],
        },
    },
    "ja": {
        "fallback": "未分類",
        "search_label": "このページを検索",
        "quick_filter": "クイックフィルター",
        "all": "すべて",
        "uncertain_year": "年代未定",
        "update_note": '構造化イベントを編集した後は、<code>python scripts/build_indexes.py</code> を実行して更新してください。',
        "events": {
            "kicker": "Chronicle Index",
            "title": "事件索引",
            "summary": "`data/events.yml` から自動生成され、編目済みの事件を日時、人物、場所、出典、信頼度とともに一覧します。",
            "panel_label": "構造化イベント",
            "panel_summary": "日時、分類、場所、出典、信頼度で全記録を確認できます。",
            "placeholder": "日時、事件、人物、場所、出典で絞り込み",
            "headers": ["日時", "事件", "分類", "人物", "場所", "出典", "信頼度", "概要"],
        },
        "events_by_year": {
            "kicker": "Yearly Chronicle",
            "title": "年別",
            "summary": "`data/events.yml` から自動生成され、事件を年ごとにまとめます。年鑑、回顧、段階的な改訂に適しています。",
            "panel_label": "年別グループ",
            "panel_summary": "年ごとに事件を分け、時期ごとの変化と改訂範囲を確認します。",
            "placeholder": "年、事件、人物、場所、出典で絞り込み",
        },
        "people": {
            "kicker": "People Index",
            "title": "人物索引",
            "summary": "`data/people.yml` と `data/events.yml` から自動生成され、公開名、役割概要、関連事件数を確認します。",
            "panel_label": "公開人物",
            "panel_summary": "公開名、役割概要、関連事件数で人物記録を確認します。",
            "placeholder": "人物、種別、概要で絞り込み",
            "item_label": "人物",
            "headers": ["人物", "種別", "概要", "関連事件数"],
        },
        "places": {
            "kicker": "Place Index",
            "title": "場所索引",
            "summary": "`data/places.yml` と `data/events.yml` から自動生成され、会館、工房、展示空間、オンライン資料館を整理します。",
            "panel_label": "場所項目",
            "panel_summary": "場所の種別と関連事件数で、拠点、工房、展示空間、デジタル空間を整理します。",
            "placeholder": "場所、種別、概要で絞り込み",
            "item_label": "場所",
            "headers": ["場所", "種別", "概要", "関連事件数"],
        },
        "sources": {
            "kicker": "Source Index",
            "title": "出典索引",
            "summary": "`data/sources.yml` と `data/events.yml` から自動生成され、出典種別、所蔵、引用形式、関連事件数を追跡します。",
            "panel_label": "出典項目",
            "panel_summary": "出典の種別、年、所蔵、引用形式から資料根拠を追跡します。",
            "placeholder": "出典、年、所蔵、引用形式で絞り込み",
            "headers": ["出典", "種別", "年", "所蔵", "関連事件数", "引用形式"],
        },
    },
    "ru": {
        "fallback": "Без категории",
        "search_label": "Поиск по странице",
        "quick_filter": "Быстрые фильтры",
        "all": "Все",
        "uncertain_year": "Год не указан",
        "update_note": 'После изменения структурированных событий запустите <code>python scripts/build_indexes.py</code>, чтобы обновить страницы.',
        "events": {
            "kicker": "Chronicle Index",
            "title": "Индекс событий",
            "summary": "Страница создается из `data/events.yml` и показывает каталогизированные события с датами, людьми, местами, источниками и уровнем доверия.",
            "panel_label": "Структурированные события",
            "panel_summary": "Просматривайте записи по дате, категории, месту, источнику и уровню доверия.",
            "placeholder": "Фильтр по дате, событию, человеку, месту или источнику",
            "headers": ["Дата", "Событие", "Категория", "Люди", "Места", "Источники", "Доверие", "Кратко"],
        },
        "events_by_year": {
            "kicker": "Yearly Chronicle",
            "title": "По годам",
            "summary": "Страница создается из `data/events.yml` и группирует события по годам для обзоров и поэтапных правок.",
            "panel_label": "Группы по годам",
            "panel_summary": "Разделяйте события по годам, чтобы видеть этапы и области правки.",
            "placeholder": "Фильтр по году, событию, человеку, месту или источнику",
        },
        "people": {
            "kicker": "People Index",
            "title": "Индекс людей",
            "summary": "Страница создается из `data/people.yml` и `data/events.yml` и помогает сверять публичные имена, роли и число связанных событий.",
            "panel_label": "Публичные люди",
            "panel_summary": "Проверяйте записи людей по публичному имени, роли и числу связанных событий.",
            "placeholder": "Фильтр по человеку, типу или описанию",
            "item_label": "Человек",
            "headers": ["Человек", "Тип", "Описание", "Связанные события"],
        },
        "places": {
            "kicker": "Place Index",
            "title": "Индекс мест",
            "summary": "Страница создается из `data/places.yml` и `data/events.yml` и организует залы, мастерские, выставочные пространства и онлайн-архивы.",
            "panel_label": "Записи мест",
            "panel_summary": "Организуйте места по типу и числу связанных событий.",
            "placeholder": "Фильтр по месту, типу или описанию",
            "item_label": "Место",
            "headers": ["Место", "Тип", "Описание", "Связанные события"],
        },
        "sources": {
            "kicker": "Source Index",
            "title": "Индекс источников",
            "summary": "Страница создается из `data/sources.yml` и `data/events.yml` и отслеживает тип источника, место хранения, формат цитирования и связанные события.",
            "panel_label": "Записи источников",
            "panel_summary": "Отслеживайте источники по типу, году, месту хранения и формату цитирования.",
            "placeholder": "Фильтр по источнику, году, месту хранения или цитате",
            "headers": ["Источник", "Тип", "Год", "Хранение", "Связанные события", "Цитирование"],
        },
    },
}


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


def first_year(value: str, fallback: str) -> str:
    match = re.search(r"(?<!\d)(-?\d{1,4})(?!\d)", value or "")
    if not match:
        return fallback
    year = int(match.group(1))
    return f"{year:04d}" if year >= 0 else str(year)


def event_year(event: dict[str, Any], language: dict[str, Any]) -> str:
    return first_year(str(event.get("sort_date") or event.get("date") or ""), language["uncertain_year"])


def event_sort_key(event: dict[str, Any], language: dict[str, Any]) -> tuple[str, str]:
    sort_date = str(event.get("sort_date") or event.get("date") or "")
    year = event_year(event, language)
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
    next_body = body.rstrip() + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == next_body:
        return
    path.write_text(next_body, encoding="utf-8")


def page_intro(kicker: str, title: str, summary: str) -> str:
    return "\n".join(
        [
            '<section class="archive-page-intro" markdown>',
            f'  <p class="archive-kicker">{kicker}</p>',
            f"  <h1>{title}</h1>",
            f"  <p>{summary}</p>",
            "</section>",
            "",
        ]
    )


def unique_values(items: list[dict[str, Any]], field: str, fallback: str = "未分类") -> list[str]:
    values = {str(item.get(field) or fallback).strip() for item in items}
    return sorted(value for value in values if value)


def index_panel(
    language: dict[str, Any],
    label: str,
    count: int,
    summary: str,
    chips: list[str],
    placeholder: str,
) -> str:
    chip_items = "\n".join(
        f'    <button type="button" class="archive-chip" data-archive-filter-chip="{escape(chip)}">{escape(chip)}</button>'
        for chip in chips[:10]
    )
    return "\n".join(
        [
            '<section class="archive-index-panel" data-archive-filter>',
            '  <div class="archive-index-panel__summary">',
            f'    <span class="archive-index-panel__label">{escape(label)}</span>',
            f'    <strong>{count}</strong>',
            f'    <p>{escape(summary)}</p>',
            "  </div>",
            '  <div class="archive-index-panel__tools">',
            f'    <label class="archive-index-search"><span>{escape(language["search_label"])}</span><input type="search" data-archive-filter-input placeholder="{escape(placeholder)}"></label>',
            f'    <div class="archive-chip-list" aria-label="{escape(language["quick_filter"])}">',
            f'    <button type="button" class="archive-chip archive-chip--active" data-archive-filter-reset>{escape(language["all"])}</button>',
            chip_items,
            "    </div>",
            "  </div>",
            "</section>",
            "",
        ]
    ) + "\n"


def events_table(
    language: dict[str, Any],
    events: list[dict[str, Any]],
    people_lookup: dict[str, dict[str, Any]],
    place_lookup: dict[str, dict[str, Any]],
    source_lookup: dict[str, dict[str, Any]],
) -> str:
    headers = language["events"]["headers"]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for event in sorted(events, key=lambda item: event_sort_key(item, language)):
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

    for locale, language in LANGUAGES.items():
        build_language(
            locale,
            language,
            events,
            people,
            places,
            sources,
            people_lookup,
            place_lookup,
            source_lookup,
        )


def build_language(
    locale: str,
    language: dict[str, Any],
    events: list[dict[str, Any]],
    people: list[dict[str, Any]],
    places: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    people_lookup: dict[str, dict[str, Any]],
    place_lookup: dict[str, dict[str, Any]],
    source_lookup: dict[str, dict[str, Any]],
) -> None:
    generated_dir = DOCS_DIR / locale / "generated"
    event_copy = language["events"]
    events_by_year_copy = language["events_by_year"]
    people_copy = language["people"]
    places_copy = language["places"]
    sources_copy = language["sources"]

    write(
        generated_dir / "events.md",
        HIDE_TOC
        + page_intro(
            event_copy["kicker"],
            event_copy["title"],
            event_copy["summary"],
        )
        + index_panel(
            language,
            event_copy["panel_label"],
            len(events),
            event_copy["panel_summary"],
            unique_values(events, "category", language["fallback"]),
            event_copy["placeholder"],
        )
        + f'<p class="archive-update-note">{language["update_note"]}</p>\n\n'
        + events_table(language, events, people_lookup, place_lookup, source_lookup),
    )

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        grouped[event_year(event, language)].append(event)
    year_sections = [
        HIDE_TOC
        + page_intro(
            events_by_year_copy["kicker"],
            events_by_year_copy["title"],
            events_by_year_copy["summary"],
        )
        + index_panel(
            language,
            events_by_year_copy["panel_label"],
            len(grouped),
            events_by_year_copy["panel_summary"],
            sorted(grouped),
            events_by_year_copy["placeholder"],
        )
    ]
    for year in sorted(grouped):
        year_sections.append(f"\n## {year}\n")
        year_sections.append(events_table(language, grouped[year], people_lookup, place_lookup, source_lookup))
    write(generated_dir / "events-by-year.md", "\n".join(year_sections))

    write(
        generated_dir / "people-index.md",
        HIDE_TOC
        + page_intro(
            people_copy["kicker"],
            people_copy["title"],
            people_copy["summary"],
        )
        + index_panel(
            language,
            people_copy["panel_label"],
            len(people),
            people_copy["panel_summary"],
            unique_values(people, "type", language["fallback"]),
            people_copy["placeholder"],
        )
        + index_table(people, people_copy, events, "people"),
    )

    write(
        generated_dir / "places-index.md",
        HIDE_TOC
        + page_intro(
            places_copy["kicker"],
            places_copy["title"],
            places_copy["summary"],
        )
        + index_panel(
            language,
            places_copy["panel_label"],
            len(places),
            places_copy["panel_summary"],
            unique_values(places, "type", language["fallback"]),
            places_copy["placeholder"],
        )
        + index_table(places, places_copy, events, "places"),
    )

    write(
        generated_dir / "sources-index.md",
        HIDE_TOC
        + page_intro(
            sources_copy["kicker"],
            sources_copy["title"],
            sources_copy["summary"],
        )
        + index_panel(
            language,
            sources_copy["panel_label"],
            len(sources),
            sources_copy["panel_summary"],
            unique_values(sources, "type", language["fallback"]),
            sources_copy["placeholder"],
        )
        + source_table(sources_copy, sources, events),
    )


def index_table(items: list[dict[str, Any]], copy: dict[str, Any], events: list[dict[str, Any]], field: str) -> str:
    headers = copy["headers"]
    lines = [
        "| " + " | ".join(headers) + " |",
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


def source_table(copy: dict[str, Any], sources: list[dict[str, Any]], events: list[dict[str, Any]]) -> str:
    headers = copy["headers"]
    lines = [
        "| " + " | ".join(headers) + " |",
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
