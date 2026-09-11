"""Fetch public sources and retain dated evidence for the maker directory."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import base64

import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("targets", nargs="+")
parser.add_argument("--search", action="store_true")
parser.add_argument("--summary", action="store_true", help="Print compact findings; retain full evidence on disk")
args = parser.parse_args()
for target in args.targets:
    try:
        response = requests.get("https://www.bing.com/search" if args.search else target,
                                params={"q": target} if args.search else None,
                                timeout=25, headers={"User-Agent": "Mozilla/5.0"})
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")
        if args.search:
            items = []
            for node in soup.select("li.b_algo"):
                a = node.select_one("h2 a")
                if not a:
                    continue
                url = a.get("href", "")
                encoded = parse_qs(urlparse(url).query).get("u", [""])[0]
                if encoded.startswith("a1"):
                    url = base64.urlsafe_b64decode(encoded[2:] + "=" * (-len(encoded[2:]) % 4)).decode()
                items.append({"url": url, "text": node.get_text(" ", strip=True)})
            result = {"query": target, "results": items}
        else:
            links = [{"text": a.get_text(" ", strip=True), "url": a.get("href")} for a in soup.select("a[href]")]
            images = [{"alt": a.get("alt"), "src": a.get("src")} for a in soup.select("img")]
            for node in soup.select("script,style,noscript"):
                node.decompose()
            result = {"url": response.url, "status": response.status_code,
                      "text": soup.get_text(" ", strip=True), "links": links, "images": images}
        result["fetched_at"] = datetime.now(timezone.utc).isoformat()
        dest = Path("output/shop-evidence")
        dest.mkdir(parents=True, exist_ok=True)
        name = hashlib.sha256(target.encode()).hexdigest()[:12] + ".json"
        (dest / name).write_text(json.dumps(result, ensure_ascii=False, indent=2))
        shown = {"url": result.get("url"), "status": result.get("status"), "text": result.get("text", "")[:4500]} if args.summary else result
        print(json.dumps({"file": str(dest / name), **shown}, ensure_ascii=False), flush=True)
    except Exception as exc:
        print(json.dumps({"target": target, "error": str(exc)}))
