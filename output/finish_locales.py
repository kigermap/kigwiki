"""Prepare citation repair and readable headings for existing translations."""
import difflib
import re
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
print("*** Begin Patch")
for locale in ("en", "ja", "ru"):
    for path in sorted((root / f"docs/{locale}/years").glob("*/index.md")):
        old = path.read_text()
        new = re.sub(r"(?m)^(## )\d+\. ", r"\1", old)
        if path.parent.name == "2025":
            new = re.sub(r"^\| декабрь \| итог года[^\n]*\n", "", new, flags=re.M)
            labels = {"3rd Kigurumi Party!": "kigupa", "第3回・きぐるみパーティ!": "kigupa", "Kigurumi Daikoushin! 3": "kigdai", "着ぐるみ大行進!3": "kigdai", "Kigurumi Daikoushin! 4": "kigdai4", "着ぐるみ大行進!4": "kigdai4", "World Cosplay Summit 2025": "wcs-rule", "Anime Expo 2025": "ax-aniplex"}
            original = subprocess.check_output(["git", "show", "HEAD:" + str(path.relative_to(root))], cwd=root, text=True)
            for name, label in labels.items():
                definition = re.search(r"^\[\^" + re.escape(label) + r"\]:[^\n]+", original, re.M)
                if not definition:
                    continue
                new = re.sub(r"^\|[^\n]*" + re.escape(name) + r"[^\n]*$", lambda m: m[0].replace(name, name + f"[^{label}]"), new, flags=re.M)
                if f"[^{label}]" in new and f"[^{label}]:" not in new:
                    new = new.rstrip() + "\n" + definition[0] + "\n"
            if locale == "ja":
                new = new.replace("5月23日頃", "5月23日19時（告知）")
                new = new.replace("5月の Anime North では Kigurumi Online が製面ワークショップを行い、歴史、makers、目の形、ウィッグ、内装、装着調整を新人向けの教育プロセスへ変換した。", "Kigurumi Online は Anime North で5月23日19時からの製面ワークショップを告知した。目、眉、まつ毛、ウィッグ、内装を選び、装着に合わせて調整する内容で、見学は無料と案内された。")
            if locale == "ru":
                new = new.replace("около 23 мая", "23 мая, 19:00 (анонс)")
                new = new.replace("В мае Kigurumi Online на Anime North превратил знания о масках, makers, глазах, париках, внутренней посадке и ношении в образовательную форму для новичков.", "Kigurumi Online анонсировал мастерскую на Anime North на 23 мая, 19:00: выбор глаз, бровей, ресниц, парика и подкладки, сборка и подгонка маски. Наблюдение было объявлено бесплатным.")
        if old != new:
            print("*** Update File: " + str(path.relative_to(root)))
            for line in list(difflib.unified_diff(old.splitlines(), new.splitlines(), n=3, lineterm=""))[2:]:
                print("@@" if line.startswith("@@") else line)
print("*** End Patch")
