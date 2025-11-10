from __future__ import annotations

from typing import Dict, Optional

def build_requests_proxy(proxy_url: Optional[str]) -> Optional[Dict[str, str]]:
    """
    Convert a proxy URL into requests' proxies mapping.
    Example: http://user:pass@host:port or socks5://host:port
    """
    if not proxy_url:
        return None
    return {"http": proxy_url, "https": proxy_url}