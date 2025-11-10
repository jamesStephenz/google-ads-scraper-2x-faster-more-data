from __future__ import annotations

import datetime as dt
from typing import Optional

def utc_now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def to_epoch_str(value: Optional[str]) -> str:
    """
    Accepts epoch string / int or ISO and returns epoch (seconds) as string.
    """
    if value is None:
        return "0"
    try:
        # epoch (already)
        return str(int(float(value)))
    except Exception:
        pass
    try:
        # ISO -> epoch
        iso = parse_iso(value)
        return str(int(iso.timestamp()))
    except Exception:
        return "0"

def to_iso_utc(value: Optional[str]) -> str:
    """
    Accepts epoch or ISO and returns ISO UTC with Z.
    """
    if value is None:
        return "1970-01-01T00:00:00.000Z"
    try:
        # epoch seconds
        ts = int(float(value))
        return dt.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    except Exception:
        pass
    try:
        iso = parse_iso(value)
        return iso.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    except Exception:
        return "1970-01-01T00:00:00.000Z"

def parse_iso(s: str) -> dt.datetime:
    # handle Z and fractional seconds
    s = s.strip().replace("Z", "+00:00")
    return dt.datetime.fromisoformat(s).astimezone(dt.timezone.utc).replace(tzinfo=None)