"""Prepare a reviewable patch for the 2026-09-09 annual-source revision."""
import difflib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = yaml.safe_load((Path(__file__).with_name("year-refresh.yml")).read_text())
DEDUP = re.compile(r"去重|重複(?:排除|除去|整理)|de-?duplicat|устранени[ея] повторов|удалени[ея] повторов|дублирующ", re.I)
LABELS = {
    "zh-Hans": ("资料与范围", "年度小结", "公开资料整理版", "本卷记录当年事件、作品与公开资料，按来源区分实际举办、活动预告和资料发表。"),
    "zh-Hant": ("資料與範圍", "年度小結", "公開資料整理版", "本卷記錄當年事件、作品與公開資料，依來源區分實際舉辦、活動預告和資料發表。"),
    "en": ("Scope and sources", "Annual summary", "Public-source chronicle", "This volume records events, works and publications from this year. Announcements and completed events are identified separately."),
    "ja": ("対象と資料", "年次まとめ", "公開資料に基づく編年", "本巻は当年の出来事、作品、公開資料を記録します。告知、開催記録、資料の発表を区別します。"),
    "ru": ("Границы и источники", "Итоги года", "Хроника по открытым источникам", "В томе собраны события, работы и публикации этого года. Анонсы отделены от подтверждённых записей о проведении."),
}


def sections(body):
    return re.split(r"(?=^## )", body, flags=re.M)


def heading(section):
    return section.split("\n", 1)[0]


def remove_editorial(body, year, locale):
    scope, summary, status, intro = LABELS[locale]
    result = []
    for section in sections(body):
        title = heading(section)
        if title.startswith("## ") and DEDUP.search(title):
            if re.search(r"结论|結論|conclusion|вывод", title, re.I):
                section = re.sub(r"^## .*", "## " + summary, section, count=1)
                # Mixed sections retain their substantive closing paragraphs.
                paragraphs = section.split("\n\n")
                section = "\n\n".join(p for p in paragraphs if not DEDUP.search(p) and not re.search(r"202[0-5].*(?:202[0-5]|后续|後續|later)", p))
            elif re.search(r"^## 0\.|Scope|границ", title, re.I):
                section = "## " + scope + "\n\n" + intro + "\n\n"
            else:
                continue
        if year == 2024 and re.match(r"## 8\.", title):
            continue
        if year == 2021 and re.search(r"Doll Weekend 1", title):
            continue
        result.append(section)
    body = "".join(result)
    # Remove batch-processing instructions and redundant comparison sentences.
    body = re.sub(r"^>[^\n]*(?:\n>[^\n]*)*\n*", "", body, count=1, flags=re.M)
    body = re.sub(r"(?m)^(# [^\n]+)\n", r"\1\n\n> " + intro + "\n", body, count=1)
    body = re.sub(r"(?m)^subtitle:.*$", 'subtitle: "' + status + '"', body)
    body = re.sub(r"(?m)^status:.*$", 'status: "' + status + '"', body)
    body = re.sub(r"(?:下一未整理年份为|下一未整理年份為)[^。]*。", "", body)
    body = re.sub(r"The next unfinished year is \d{4}\.", "", body)
    body = re.sub(r"Следующий неразобранный год[^.]*\.", "", body)
    return body


def chinese_volume(original, year, item):
    front, body = original[4:].split("---", 1)
    for before, after in item.get("replace", {}).items():
        body = body.replace(before, after)
    front = re.sub(r'(?m)^date:.*$', 'date: "2026-09-09"', front)
    front = re.sub(r'(?m)^status:.*$', 'status: "公开资料增补版；按事件发生及资料发表年份归档"', front)
    front = re.sub(r'(?m)^subtitle:.*$', 'subtitle: "年度重点与资料纪事"', front)
    original_sections = sections(body)
    kept = []
    for section in original_sections:
        title = heading(section)
        if re.search(r"^## (?:\d+\. )?(?:可核验节点|主要纪事|主要紀事|\d{4} 年编年史|2\. 编年史正文)", title):
            kept.append(section)
    if year == 2025:
        kept = [s for s in original_sections if heading(s).startswith("## 2. 编年史正文")]
    assert len(kept) == 1, (year, [heading(s) for s in kept])
    events = []
    for part in re.split(r"(?=^### )", kept[0], flags=re.M)[1:]:
        title = heading(part)
        if any(key in title for key in item.get("drop", [])):
            continue
        paragraphs = part.rstrip().split("\n\n")
        clean = []
        for para in paragraphs:
            if para.strip() == "---":
                continue
            if not para.startswith("###") and (DEDUP.search(para) or re.search(r"已(?:经)?完成|已经记录|下一未整理|后续专题站|後續專題站", para)):
                continue
            # Comparisons with other volumes belong outside an annual event record.
            if not para.startswith("###") and re.search(r"(?<![\w/])(?:19|20)\d{2}(?![\w/])", para):
                dates = set(re.findall(r"(?<![\w/])(?:19|20)\d{2}(?![\w/])", para))
                if any(int(n) != year for n in dates):
                    continue
            clean.append(para)
        event = "\n\n".join(clean).strip()
        for before, after in item.get("replace", {}).items():
            event = event.replace(before, after)
        if len(clean) > 1:
            events.append(event)
    for new in item.get("events", []):
        anchor = new.get("before")
        entry = "### " + new["title"] + "\n\n" + new["body"].strip()
        if new.get("replace_event"):
            index = next(i for i, event in enumerate(events) if new["replace_event"] in heading(event))
            events[index] = entry
        elif anchor:
            index = next((i for i, event in enumerate(events) if anchor in heading(event)), None)
            assert index is not None, (year, anchor)
            events.insert(index, entry)
        else:
            events.append(entry)
    if "ordered_titles" in item:
        events.sort(key=lambda event: next(i for i, key in enumerate(item["ordered_titles"]) if key in heading(event)))
    refs = next(s for s in original_sections if re.match(r"## (?:\d+\. )?(?:参考资料|资料来源|来源)", heading(s)))
    refs = re.sub(r"^## .*", "## 参考资料", refs, count=1).strip()
    refs += "\n\n" + item.get("sources", "").strip()
    content = ("---\n" + front.strip() + "\n---\n\n# " + str(year) + " 年 Kigurumi 编年史\n\n"
               + item["intro"].strip() + "\n\n## 年度重点\n\n" + item["highlights"].strip()
               + "\n\n## 年度纪事\n\n" + "\n\n".join(events)
               + "\n\n## 年度小结\n\n" + item["summary"].strip() + "\n\n" + refs + "\n")
    # Footnotes for removed cross-year discussions do not belong in the source list.
    used = set(re.findall(r"\[\^([^\]]+)\](?!:)", content))
    content = re.sub(r"^\[\^([^\]]+)\]:[^\n]*\n?", lambda m: m[0] if m[1] in used else "", content, flags=re.M)
    used_html = set(re.findall(r'\]\(#(s\d+)\)', content))
    content = re.sub(r'<a id="(s\d+)"></a>.*?(?=\n\n<a id=|\n\n\[\^|\Z)', lambda m: m[0] if m[1] in used_html else "", content, flags=re.S)
    return re.sub(r"\n{3,}", "\n\n", content).rstrip() + "\n"


changes = []
for path in sorted(DOCS.glob("*/years/*/index.md")):
    year = int(path.parent.name)
    locale = path.parts[-4]
    if "--locale" in sys.argv and locale != sys.argv[sys.argv.index("--locale") + 1]:
        continue
    old = path.read_text()
    new = chinese_volume(old, year, DATA[year]) if locale == "zh-Hans" else remove_editorial(old, year, locale)
    if old != new:
        changes.append((path, old, new))

if "--patch" in sys.argv:
    print("*** Begin Patch")
    for path, old, new in changes:
        print("*** Update File: " + str(path.relative_to(ROOT)))
        lines = list(difflib.unified_diff(old.splitlines(), new.splitlines(), n=3, lineterm=""))[2:]
        for line in lines:
            print("@@" if line.startswith("@@") else line)
    print("*** End Patch")
else:
    print(json.dumps([{"path": str(p.relative_to(ROOT)), "before": len(o), "after": len(n)} for p, o, n in changes], ensure_ascii=False))
