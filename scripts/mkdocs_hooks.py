from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_indexes import build  # noqa: E402


def on_pre_build(config, **kwargs):
    build(ROOT)

