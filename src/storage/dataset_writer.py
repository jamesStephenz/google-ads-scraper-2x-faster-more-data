from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

@dataclass
class DatasetWriter:
    jsonl_path: Path
    csv_path: Path

    def __post_init__(self):
        self._jsonl_f = self.jsonl_path.open("w", encoding="utf-8")
        self._csv_f = self.csv_path.open("w", encoding="utf-8", newline="")
        self._csv_writer = None
        self._csv_fields = None

    def write(self, rec: Dict[str, Any]) -> None:
        # JSONL
        self._jsonl_f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        # CSV - flatten nested fields into JSON strings
        flat = {k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v) for k, v in rec.items()}
        if self._csv_writer is None:
            self._csv_fields = list(flat.keys())
            self._csv_writer = csv.DictWriter(self._csv_f, fieldnames=self._csv_fields)
            self._csv_writer.writeheader()
        self._csv_writer.writerow(flat)

    def close(self) -> None:
        try:
            self._jsonl_f.close()
        finally:
            self._csv_f.close()