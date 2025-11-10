from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

def load_cookies(path: Path) -> Dict[str, str]:
    """
    Accepts cookies from common export formats (array of {name, value}) or
    a simple key-value dict.
    """
    if not path.exists():
        raise FileNotFoundError(str(path))
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        return {str(k): str(v) for k, v in data.items()}

    if isinstance(data, list):
        jar = {}
        for c in data:
            name = c.get("name")
            val = c.get("value")
            if name is not None and val is not None:
                jar[str(name)] = str(val)
        return jar

    raise ValueError("Unsupported cookies file format.")