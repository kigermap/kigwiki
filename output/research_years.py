"""Capture dated public source text for the annual archive revision."""
import hashlib
import json
import sys
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent / "year-evidence"
ROOT.mkdir(exist_ok=True)

urls = sys.argv[1:]
if urls == ["--sigma-archive"]:
    archive = json.loads((ROOT / "b04228bca9bc.json").read_text())
    urls = [urljoin(archive["url"], a["href"]) for a in archive["links"] if a["href"].endswith(".htm")]

for url in urls:
    try:
        response = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        if response.encoding == "ISO-8859-1":
            response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")
        links = [{"text": a.get_text(" ", strip=True), "href": a["href"]} for a in soup.select("a[href]")]
        for node in soup.select("script, style, nav, footer, header"):
            node.decompose()
        record = {"url": url, "final_url": response.url, "accessed": "2026-09-09", "text": soup.get_text("\n", strip=True), "links": links}
        target = ROOT / (hashlib.sha256(url.encode()).hexdigest()[:12] + ".json")
        target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"url": url, "file": str(target), "chars": len(record["text"]), "preview": record["text"][:450]}, ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"url": url, "error": str(error)}, ensure_ascii=False))
