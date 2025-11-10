from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests

class MediaStore:
    """
    Lightweight media downloader. Stores images/videos referenced in the creative
    under deterministic keys (sha1 of URL basename).
    """

    def __init__(self, media_dir: Path):
        self.media_dir = media_dir
        self.media_dir.mkdir(parents=True, exist_ok=True)

    def _key_for_url(self, url: str) -> str:
        parsed = urlparse(url)
        name = Path(parsed.path).name or "media"
        base = name.split("?")[0]
        digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
        return f"{digest}_{base}"

    def capture_media(self, record: Dict) -> List[str]:
        keys: List[str] = []
        preview_url: Optional[str] = record.get("previewUrl")
        if preview_url:
            key = self._key_for_url(preview_url)
            if self._download(preview_url, key):
                record["previewStoreKey"] = key
                keys.append(key)

        for v in record.get("variants") or []:
            for img in v.get("images") or []:
                key = self._key_for_url(img)
                if self._download(img, key):
                    keys.append(key)
                    v.setdefault("imageStoreKeys", []).append(key)
        return keys

    def _download(self, url: str, key: str) -> bool:
        try:
            path = self.media_dir / key
            if path.exists():
                return True
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            path.write_bytes(resp.content)
            return True
        except Exception as e:
            logging.debug("Media download failed for %s: %s", url, e)
            return False