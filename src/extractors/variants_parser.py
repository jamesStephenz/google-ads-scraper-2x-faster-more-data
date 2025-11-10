from __future__ import annotations

import re
from typing import Any, Dict, List

def extract_variants_from_html(html: str) -> List[Dict[str, Any]]:
    """
    Very small heuristic: extract the <title> and image tags as variants if no JSON is present.
    """
    variants: List[Dict[str, Any]] = []
    title = _first_or_none(re.findall(r"<title[^>]*>(.*?)</title>", html, flags=re.S | re.I))
    imgs = re.findall(r'<img[^>]+src=["\\\']([^"\\\']+)["\\\']', html, flags=re.I)

    if title or imgs:
        variants.append(
            {
                "textContent": title or "",
                "images": imgs or [],
                "imageStoreKeys": [],
            }
        )
    return variants

def _first_or_none(lst: List[str]) -> str:
    return lst[0].strip() if lst else ""