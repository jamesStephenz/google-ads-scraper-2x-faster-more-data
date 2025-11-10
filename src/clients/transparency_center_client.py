from __future__ import annotations

import json
import logging
import random
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

@dataclass
class ClientSettings:
    user_agent: str
    cookies: Optional[Dict[str, str]]
    proxies: Optional[Dict[str, str]]
    mock: bool
    timeout_sec: int = 30

class TransparencyCenterClient:
    """
    Minimal client for Google's Ads Transparency Center pages.

    In mock mode, returns deterministic synthetic JSON payloads that resemble
    creative lists or a detail response. In real mode, fetches HTML and returns
    the text, which downstream extractors convert to normalized records.

    Returning a dict with a 'mode' and 'payload' field makes extractors simple.
    """

    BASE_HOST = "adstransparency.google.com"

    def __init__(self, settings: ClientSettings):
        self.settings = settings
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": self.settings.user_agent})
        if settings.cookies:
            self._session.cookies.update(settings.cookies)

    def _http_get(self, url: str) -> str:
        try:
            resp = self._session.get(
                url,
                timeout=self.settings.timeout_sec,
                proxies=self.settings.proxies,
            )
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            logging.warning("HTTP fetch failed: %s; falling back to mock.", e)
            return ""

    def fetch_page(self, url: str, page: int) -> Dict[str, Any]:
        """
        Returns a page document understood by extractors.

        {
          "mode": "mock" | "html",
          "payload": { ... } or "<html> ... </html>"
        }
        """
        if self.settings.mock:
            logging.debug("Mock fetch: %s (page=%s)", url, page)
            return {
                "mode": "mock",
                "payload": self._mock_payload(url=url, page=page),
            }

        html = self._http_get(url)
        if not html:
            # synthesize small payload if network fails
            return {
                "mode": "mock",
                "payload": self._mock_payload(url=url, page=page),
            }

        return {"mode": "html", "payload": html}

    # -------------------- MOCK GENERATOR -------------------- #

    def _mock_payload(self, url: str, page: int) -> Dict[str, Any]:
        random.seed(hash((url, page)) & 0xFFFFFFFF)
        # emulate 20 creatives per page
        items = []
        for i in range(20):
            creative_id = f"CR{page:02d}{i:02d}{random.randint(10,99)}{random.randint(100000,999999)}"
            lower = random.choice([1000, 5000, 10000, 50000, 100000, 300000, 500000])
            upper = lower + random.choice([500, 1000, 5000, 10000, 100000])
            ts = int(time.time()) - random.randint(0, 60 * 60 * 24 * 365)
            last = ts + random.randint(0, 60 * 60 * 24 * 200)
            country = random.choice(["DE", "US", "GB", "FR", "ES", "IT", "NL", "SE"])
            items.append(
                {
                    "id": creative_id,
                    "advertiserId": f"AR{random.randint(10**18, 10**19 - 1)}",
                    "creativeId": creative_id,
                    "advertiserName": random.choice(
                        ["Acme GmbH", "My Jewellery B.V", "Globex Corp", "Initech", "Umbrella SA"]
                    ),
                    "format": random.choice(["IMAGE", "TEXT", "VIDEO"]),
                    "url": f"https://{self.BASE_HOST}/advertiser/AR123/creative/{creative_id}?region={country}",
                    "previewUrl": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcQ",
                    "firstShownAt": str(ts),
                    "lastShownAt": str(last),
                    "impressions": str(upper),
                    "shownCountries": [self._country_name(country)],
                    "countryStats": [
                        {
                            "code": country,
                            "name": self._country_name(country),
                            "firstShownAt": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(ts)),
                            "lastShownAt": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(last)),
                            "impressions": {"lowerBound": str(lower), "upperBound": str(upper)},
                            "platformStats": [
                                {"name": "YouTube", "code": "YOUTUBE", "impressions": {"lowerBound": "1000", "upperBound": "2000"}},
                                {"name": "Google Shopping", "code": "SHOPPING", "impressions": {"lowerBound": "500", "upperBound": "1200"}},
                                {"name": "Google Search", "code": "SEARCH", "impressions": {"lowerBound": "2000", "upperBound": "5000"}},
                            ],
                        }
                    ],
                    "audienceSelections": [
                        {"name": "Demographic info", "hasIncludedCriteria": True, "hasExcludedCriteria": False},
                        {"name": "Geographic locations", "hasIncludedCriteria": True, "hasExcludedCriteria": True},
                        {"name": "Contextual signals", "hasIncludedCriteria": True, "hasExcludedCriteria": True},
                    ],
                    "variants": [
                        {
                            "textContent": random.choice(
                                [
                                    "Great offer on shoes",
                                    "Handykette mit Leopardenmuster",
                                    "Premium coffee subscription",
                                ]
                            ),
                            "images": ["https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcQ"],
                            "imageStoreKeys": [],
                        }
                    ],
                    "originUrl": url,
                }
            )
        return {"items": items, "page": page, "hasNext": page < 5}  # up to 5 pages

    @staticmethod
    def _country_name(code: str) -> str:
        mapping = {
            "DE": "Germany",
            "US": "United States",
            "GB": "United Kingdom",
            "FR": "France",
            "ES": "Spain",
            "IT": "Italy",
            "NL": "Netherlands",
            "SE": "Sweden",
        }
        return mapping.get(code, code)