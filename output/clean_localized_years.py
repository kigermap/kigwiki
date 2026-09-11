"""Prepare removal of cross-year commentary from existing translated volumes."""
import difflib
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
locale = sys.argv[1]


def displayed_years(text):
    text = re.sub(r"https?://[^\s<>]+|\]\([^)]*\)|\[\^[^]]+\]", "", text)
    return set(re.findall(r"(?<![\w/])(?:19|20)\d{2}(?![\w/])", text))


print("*** Begin Patch")
for path in sorted((root / f"docs/{locale}/years").glob("*/index.md")):
    if len(sys.argv) > 2 and path.parent.name != sys.argv[2]:
        continue
    old = path.read_text()
    year = path.parent.name
    blocks = re.split(r"(?=^## )", old, flags=re.M)
    intro = blocks[0]
    # Keep the actual chronology; generic domain ledgers and repeated analyses
    # are not additional annual events.
    if locale == "ja" and year == "2020":
        chronology = next(b for b in blocks if b.startswith("## 1. 確認できた経過"))
    else:
        chronology = next(b for b in blocks if re.match(r"^## (?:2\.|Verified chronology|確認でき|Проверенная хронология|Границы и подтвержденная хронология)", b))
    refs = next(b for b in blocks if re.match(r"^## (?:\d+\. )?(Source|Reference|出典|参考|ソース|Источник|Ссылки)", b))
    clean = []
    for part in re.split(r"(?=^### )", chronology, flags=re.M):
        title = part.split("\n", 1)[0]
        if title.startswith("###") and (displayed_years(title) - {year} or "Special 2" in title):
            continue
        paragraphs = []
        for para in part.rstrip().split("\n\n"):
            if para == "---":
                continue
            if para.startswith("|"):
                rows = []
                for line in para.splitlines():
                    if displayed_years(line) - {year}:
                        continue
                    if year == "2025" and re.search(r"BlackCat|Inthemask|KaoKig|Japan Expo|Lagucos|^\| (?:1月頃|9-10月|11月下旬|12月|около января|сентябрь|ноябрь.*аноним)|匿名|аноним|年末総括|Итоги года", line, re.I):
                        continue
                    rows.append(line)
                para = "\n".join(rows)
            elif not para.startswith("##") and (displayed_years(para) - {year} or re.search(r"去重|重複排除|de-?duplicat|SP2", para, re.I)):
                continue
            if year == "2025" and not para.startswith("|") and re.search(r"BlackCat|Inthemask|KaoKig|Japan Expo|Lagucos|匿名|аноним|risk_governance|\[\^note-term\]|\[\^note-harass\]", para, re.I):
                continue
            if para:
                paragraphs.append(para)
        if len(paragraphs) == 1 and paragraphs[0].startswith("###"):
            continue
        clean.append("\n\n".join(paragraphs))
    # Remove obsolete overview illustrations and manual table of contents.
    intro = re.sub(r"!\[[^\n]+\n", "", intro)
    intro = intro.rstrip().removesuffix("---").rstrip()
    new = intro + "\n\n" + "\n\n".join(clean) + "\n\n" + refs
    used = set(re.findall(r"\[\^([^]]+)\](?!:)", new))
    new = re.sub(r"^\[\^([^]]+)\]:[^\n]*\n?", lambda m: m[0] if m[1] in used else "", new, flags=re.M)
    used_html = set(re.findall(r"\]\(#(s\d+)\)", new))
    new = re.sub(r'<a id="(s\d+)"></a>.*?(?=\n\n<a id=|\n\n\[\^|\Z)', lambda m: m[0] if m[1] in used_html else "", new, flags=re.S)
    new = re.sub(r"\n{3,}", "\n\n", new).rstrip() + "\n"
    if old != new:
        print("*** Update File: " + str(path.relative_to(root)))
        for line in list(difflib.unified_diff(old.splitlines(), new.splitlines(), n=3, lineterm=""))[2:]:
            print("@@" if line.startswith("@@") else line)
print("*** End Patch")
