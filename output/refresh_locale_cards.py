"""Keep translated directory cards consistent with their retained chronologies."""
import difflib
import html
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
print("*** Begin Patch")
for locale in ("en", "ja", "ru"):
    for section in ("years", "chronicle"):
        path = root / f"docs/{locale}/{section}/index.md"
        old = path.read_text()
        def card(match):
            text = match[0]
            year = re.search(r'href="(?:\.\./years/)?(\d{4})/"', text)
            if not year:
                return text
            volume = root / f"docs/{locale}/years/{year[1]}/index.md"
            if not volume.exists():
                return text
            headings = re.findall(r"^### (.+)", volume.read_text(), re.M)[:2]
            if not headings:
                return text
            summary = " · ".join(re.sub(r"\s*\{#[^}]+\}|[*`]", "", h).rstrip("。.") for h in headings)
            return re.sub(r"<p>.*?</p>", "<p>" + html.escape(summary) + "</p>", text, count=1, flags=re.S)
        new = re.sub(r'<article class="archive-feature">.*?</article>', card, old, flags=re.S)
        if locale == "ja":
            new = new.replace("出典確認と重複排除", "出典と日付の確認")
        if old != new:
            print("*** Update File: " + str(path.relative_to(root)))
            for line in list(difflib.unified_diff(old.splitlines(), new.splitlines(), n=3, lineterm=""))[2:]:
                print("@@" if line.startswith("@@") else line)
print("*** End Patch")
