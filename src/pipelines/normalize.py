from __future__ import annotations

import hashlib
import logging
from typing import Any, Dict, List, Optional

from utils.timefmt import to_iso_utc, to_epoch_str

class Normalizer:
    """
    Converts extracted creative items into a normalized schema suitable for
    analytics (mirroring the README's example).
    """

    def __init__(self, origin_url: str):
        self.origin_url = origin_url

    def normalize_record(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        # Defensive access
        creative_id = raw.get("creativeId") or raw.get("id") or self._guess_id(raw)
        advertiser_id = raw.get("advertiserId") or "AR_UNKNOWN"
        advertiser_name = raw.get("advertiserName") or "Unknown"
        fmt = raw.get("format") or self._guess_format(raw)
        url = raw.get("url") or self.origin_url
        preview = raw.get("previewUrl") or self._first_image(raw)

        first_ts = to_epoch_str(raw.get("firstShownAt"))
        last_ts = to_epoch_str(raw.get("lastShownAt"))

        country_stats = self._normalize_country_stats(raw.get("countryStats") or [])
        shown_countries = list({c.get("name") for c in country_stats if c.get("name")}) or raw.get("shownCountries") or []

        variants = raw.get("variants") or []
        audience = raw.get("audienceSelections") or []

        record = {
            "id": str(creative_id),
            "advertiserId": str(advertiser_id),
            "creativeId": str(creative_id),
            "advertiserName": advertiser_name,
            "format": fmt,
            "url": url,
            "previewUrl": preview,
            "previewStoreKey": "",
            "firstShownAt": first_ts,
            "lastShownAt": last_ts,
            "impressions": str((raw.get("impressions") or "0")),
            "shownCountries": shown_countries,
            "countryStats": country_stats,
            "platformStats": self._flatten_platforms(country_stats),
            "audienceSelections": audience,
            "variants": variants,
            "originUrl": self.origin_url,
            "mediaStoreKeys": [],
        }
        logging.debug("Normalized record %s", record.get("id"))
        return record

    def _normalize_country_stats(self, stats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        norm = []
        for s in stats:
            norm.append(
                {
                    "code": s.get("code"),
                    "name": s.get("name"),
                    "firstShownAt": to_iso_utc(s.get("firstShownAt")),
                    "lastShownAt": to_iso_utc(s.get("lastShownAt")),
                    "impressions": {
                        "lowerBound": str(((s.get("impressions") or {}).get("lowerBound") or "0")),
                        "upperBound": str(((s.get("impressions") or {}).get("upperBound") or "0")),
                    },
                    "platformStats": [
                        {
                            "name": p.get("name"),
                            "code": p.get("code"),
                            "impressions": {
                                "lowerBound": str(((p.get("impressions") or {}).get("lowerBound") or "0")),
                                "upperBound": str(((p.get("impressions") or {}).get("upperBound") or "0")),
                            },
                        }
                        for p in (s.get("platformStats") or [])
                    ],
                }
            )
        return norm

    def _flatten_platforms(self, stats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Build per-country platform stats in a single list
        out: List[Dict[str, Any]] = []
        for s in stats:
            for p in s.get("platformStats", []):
                out.append(
                    {
                        "country": s.get("name"),
                        "countryCode": s.get("code"),
                        "name": p.get("name"),
                        "code": p.get("code"),
                        "impressions": p.get("impressions"),
                    }
                )
        return out

    @staticmethod
    def _guess_id(raw: Dict[str, Any]) -> str:
        # Create a stable id hash from content
        h = hashlib.sha1(repr(sorted(raw.items())).encode("utf-8")).hexdigest()
        return f"CR_{h[:12]}"

    @staticmethod
    def _guess_format(raw: Dict[str, Any]) -> str:
        imgs = []
        for v in raw.get("variants") or []:
            imgs.extend(v.get("images") or [])
        return "IMAGE" if imgs else "TEXT"

    @staticmethod
    def _first_image(raw: Dict[str, Any]) -> Optional[str]:
        for v in raw.get("variants") or []:
            imgs = v.get("images") or []
            if imgs:
                return imgs[0]
        return None