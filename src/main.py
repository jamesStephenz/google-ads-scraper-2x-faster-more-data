import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

# Ensure imports work when running this file directly
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from utils.timefmt import utc_now_iso  # noqa: E402
from utils.cookies import load_cookies  # noqa: E402
from utils.proxies import build_requests_proxy  # noqa: E402
from storage.dataset_writer import DatasetWriter  # noqa: E402
from storage.media_store import MediaStore  # noqa: E402
from clients.transparency_center_client import TransparencyCenterClient, ClientSettings  # noqa: E402
from pipelines.pagination import Paginator  # noqa: E402
from pipelines.normalize import Normalizer  # noqa: E402
from extractors.ad_parser import parse_creatives  # noqa: E402

def load_settings(example_settings_path: Path) -> Dict[str, Any]:
    if example_settings_path.exists():
        with example_settings_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def resolve_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Google Ads Transparency Center scraper (fast, normalized)."
    )
    parser.add_argument(
        "--input",
        default=str(CURRENT_DIR.parent / "data" / "sample_input.json"),
        help="Path to input JSON containing originUrl / maxItems / downloadMedia flags.",
    )
    parser.add_argument(
        "--settings",
        default=str(CURRENT_DIR / "config" / "settings.example.json"),
        help="Path to settings JSON (cookiesFile, proxy, userAgent, mock).",
    )
    parser.add_argument(
        "--out-jsonl",
        default=str(Path.cwd() / f"ads_{utc_now_iso().replace(':', '').replace('-', '')}.jsonl"),
        help="Output JSON Lines file path.",
    )
    parser.add_argument(
        "--out-csv",
        default=str(Path.cwd() / f"ads_{utc_now_iso().replace(':', '').replace('-', '')}.csv"),
        help="Output CSV file path.",
    )
    parser.add_argument(
        "--media-dir",
        default=str(Path.cwd() / "media"),
        help="Directory to store downloaded media if enabled.",
    )
    parser.add_argument(
        "--real-http",
        action="store_true",
        help="Force real HTTP mode even if settings.mock=true.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity.",
    )
    return parser.parse_args()

def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s | %(levelname)-8s | %(message)s",
    )

def run() -> None:
    args = resolve_args()
    setup_logging(args.log_level)

    input_path = Path(args.input)
    settings_path = Path(args.settings)
    media_dir = Path(args.media_dir)
    media_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Input JSON not found at: {input_path}")

    # Load inputs & settings
    input_payload = read_json(input_path)
    settings_raw = load_settings(settings_path)

    cookies = None
    if settings_raw.get("cookiesFile"):
        try:
            cookies = load_cookies(Path(settings_raw["cookiesFile"]))
        except FileNotFoundError:
            logging.warning("cookiesFile not found; continuing without cookies")

    proxies = build_requests_proxy(settings_raw.get("proxy")) if settings_raw.get("proxy") else None
    user_agent = settings_raw.get("userAgent") or (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    )
    mock_mode = settings_raw.get("mock", True) and not args.real_http

    client_settings = ClientSettings(
        user_agent=user_agent,
        cookies=cookies,
        proxies=proxies,
        mock=mock_mode,
        timeout_sec=int(settings_raw.get("timeoutSec") or 30),
    )
    client = TransparencyCenterClient(client_settings)

    origin_url = input_payload.get("originUrl") or input_payload.get("url")
    if not origin_url:
        raise ValueError("Input must include 'originUrl' (Transparency Center search/detail URL).")

    max_items = int(input_payload.get("maxItems") or 100)
    download_media = bool(input_payload.get("downloadMedia") or False)

    logging.info(
        "Starting scrape | originUrl=%s | maxItems=%s | downloadMedia=%s | mock=%s",
        origin_url,
        max_items,
        download_media,
        client_settings.mock,
    )

    paginator = Paginator(client=client, max_items=max_items)
    normalizer = Normalizer(origin_url=origin_url)
    media_store = MediaStore(media_dir=media_dir)

    writer = DatasetWriter(jsonl_path=Path(args.out_jsonl), csv_path=Path(args.out_csv))
    total = 0

    # Fetch -> Extract -> Normalize -> Store
    for page_idx, page_content in enumerate(paginator.iter_pages(origin_url), start=1):
        logging.debug("Processing page %d", page_idx)
        raw_creatives = parse_creatives(page_content)
        logging.debug("Raw creatives on page %d: %d", page_idx, len(raw_creatives))
        normalized: Iterable[Dict[str, Any]] = map(normalizer.normalize_record, raw_creatives)

        for rec in normalized:
            if download_media:
                media_keys = media_store.capture_media(rec)
                if media_keys:
                    rec["mediaStoreKeys"] = media_keys

            writer.write(rec)
            total += 1
            if total >= max_items:
                break

        if total >= max_items:
            break

    writer.close()
    logging.info("Finished. Wrote %d records to %s and %s", total, writer.jsonl_path, writer.csv_path)

if __name__ == "__main__":
    run()