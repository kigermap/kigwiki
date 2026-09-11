"""Prepare Traditional Chinese annual documents from the revised Chinese source."""
import difflib
import re
import sys
from pathlib import Path
from opencc import OpenCC

root = Path(__file__).resolve().parents[1]
converter = OpenCC("s2t")
print("*** Begin Patch")
paths = list((root / "docs/zh-Hans/years").glob("*/index.md"))
paths += [root / f"docs/zh-Hans/{section}/index.md" for section in ("years", "chronicle", "sources")]
for source in paths:
    if len(sys.argv) > 1 and source.parent.name != sys.argv[1]:
        continue
    target = Path(str(source).replace("/zh-Hans/", "/zh-Hant/"))
    old = target.read_text()
    # Protect source URLs, asset paths, identifiers and inline technical names.
    tokens = []
    def protect(match):
        tokens.append(match[0])
        return f"ZZPROTECTED{len(tokens)-1}ZZ"
    text = re.sub(r"https?://[^\s<>\)]+|`[^`]+`|(?<=\]\()[^\)]+|(?<=href=\")[^\"]+", protect, source.read_text())
    new = converter.convert(text)
    for index, token in enumerate(tokens):
        new = new.replace(f"ZZPROTECTED{index}ZZ", token)
    new = new.replace('language: "zh-CN"', 'language: "zh-Hant"')
    if old == new:
        continue
    print("*** Update File: " + str(target.relative_to(root)))
    for line in list(difflib.unified_diff(old.splitlines(), new.splitlines(), n=3, lineterm=""))[2:]:
        print("@@" if line.startswith("@@") else line)
print("*** End Patch")
