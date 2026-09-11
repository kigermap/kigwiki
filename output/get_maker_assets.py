"""Cache the small set of public brand images selected during source review."""
import hashlib
import json
import mimetypes
from pathlib import Path
from types import SimpleNamespace

import requests
import yaml

root = Path(__file__).resolve().parents[1]
data = yaml.safe_load((root / "docs/assets/data/makers.yml").read_text())
dest = root / "docs/assets/images/makers"
dest.mkdir(parents=True, exist_ok=True)
manifest = []
for maker in data["makers"]:
    for kind in ("logo", "photo"):
        if not maker.get(kind):
            continue
        url = maker[kind]
        cached = list(dest.glob(f"{maker['id']}-{kind}.*"))
        try:
            if cached:
                response = SimpleNamespace(content=cached[0].read_bytes(), headers={"content-type": mimetypes.guess_type(cached[0])[0]})
            else:
                response = requests.get(url, timeout=25)
                response.raise_for_status()
        except requests.RequestException as exc:
            print("Image unavailable", maker["id"], kind, str(exc)[:100])
            manifest.append({"maker": maker["name"], "kind": kind, "source": url,
                             "checked": data["checked"], "error": "Remote asset unavailable; no replacement invented."})
            continue
        mime = response.headers.get("content-type", "").split(";")[0]
        extension = {"image/png": "png", "image/apng": "png", "image/jpeg": "jpg", "image/webp": "webp", "image/svg+xml": "svg", "image/avif": "avif", "image/gif": "gif"}.get(mime)
        if not extension:
            raise ValueError(f"Not an image: {url} {mime}")
        path = dest / f"{maker['id']}-{kind}.{extension}"
        path.write_bytes(response.content)
        manifest.append({"file": path.name, "maker": maker["name"], "kind": kind,
                         "source": url, "checked": data["checked"], "mime": mime,
                         "sha256": hashlib.sha256(response.content).hexdigest(),
                         "rights": "Third-party brand identification / product reference; no open license asserted."})
        print(path.name, len(response.content))
(dest / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
