from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict, List

from .variants_parser import extract_variants_from_html

def parse_creatives(page_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Convert a page document (mock or raw HTML) into a list of creative dicts
    ready for normalization.
    """
    mode = page_doc.get("mode")
    payload = page_doc.get("payload")

    if mode == "mock":
        items = payload.get("items", [])
        logging.debug("Extractor (mock): %d items", len(items))
        return items

    if mode == "html" and isinstance(payload, str):
        html = payload
        # Attempt to find JSON objects embedded in the page (common in SPAs)
        json_blobs = _extract_json_blobs(html)
        items: List[Dict[str, Any]] = []
        for blob in json_blobs:
            if isinstance(blob, dict) and "creativeId" in blob:
                items.append(blob)
            elif isinstance(blob, list):
                for inner in blob:
                    if isinstance(inner, dict) and "creativeId" in inner:
                        items.append(inner)
        if items:
            logging.debug("Extractor (html): %d JSON-backed items", len(items))
            return items

        # As a fallback, create a minimal item for demo purposes.
        variants = extract_variants_from_html(html)
        logging.debug("Extractor (html): found %d variants as fallback", len(variants))
        return [
            {
                "id": "CR_FALLBACK_1",
                "advertiserId": "AR_FALLBACK",
                "creativeId": "CR_FALLBACK_1",
                "advertiserName": "Unknown Advertiser",
                "format": "TEXT",
                "url": "",
                "previewUrl": "",
                "firstShownAt": "0",
                "lastShownAt": "0",
                "impressions": "0",
                "shownCountries": [],
                "countryStats": [],
                "audienceSelections": [],
                "variants": variants,
                "originUrl": "",
            }
        ]

    logging.warning("Unsupported page document type; returning empty list.")
    return []

def _extract_json_blobs(html: str) -> List[Any]:
    """
    Greedy but useful: find <script> tags that look like JSON, then parse.
    """
    blobs: List[Any] = []
    for match in re.finditer(r"<script[^>]*>(.*?)</script>", html, flags=re.S | re.I):
        content = match.group(1).strip()
        content = _strip_html_comments(content)
        content = content.strip()
        if not content:
            continue
        # Identify JSON-like content
        if content.startswith("{") or content.startswith("["):
            try:
                blobs.append(json.loads(content))
            except Exception:
                continue
    return blobs

def _strip_html_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)