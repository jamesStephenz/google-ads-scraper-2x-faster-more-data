from __future__ import annotations

import logging
from typing import Any, Dict, Iterator

from clients.transparency_center_client import TransparencyCenterClient

class Paginator:
    """
    Iterates over pages from the Transparency Center until max items obtained
    or the source reports no next page.
    """

    def __init__(self, client: TransparencyCenterClient, max_items: int):
        self.client = client
        self.max_items = max_items

    def iter_pages(self, origin_url: str) -> Iterator[Dict[str, Any]]:
        page = 1
        fetched = 0

        while True:
            page_doc = self.client.fetch_page(url=origin_url, page=page)
            yield page_doc

            # Determine whether more pages exist. In mock mode, the payload indicates it.
            if page_doc.get("mode") == "mock":
                payload = page_doc.get("payload", {})
                items_count = len(payload.get("items", []))
                fetched += items_count
                has_next = bool(payload.get("hasNext"))
                logging.debug("Paginator (mock): page=%s items=%s fetched=%s", page, items_count, fetched)
                if fetched >= self.max_items or not has_next:
                    break
                page += 1
            else:
                # In HTML mode we can't reliably detect; stop when we have enough.
                # The caller will break based on item count.
                page += 1
                if fetched >= self.max_items or page > 50:
                    break