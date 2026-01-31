import csv
import json
from pathlib import Path
from typing import Any


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def save_json(results: list[dict[str, Any]], path: str | Path) -> None:
    out_path = Path(path)
    _ensure_parent(out_path)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def save_csv(results: list[dict[str, Any]], path: str | Path) -> None:
    out_path = Path(path)
    _ensure_parent(out_path)

    fieldnames = ["url", "depth", "status", "title", "word_count", "error"]

    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in results:
            data = item.get("data") or {}
            writer.writerow(
                {
                    "url": item.get("url"),
                    "depth": item.get("depth"),
                    "status": item.get("status"),
                    "title": data.get("title"),
                    "word_count": data.get("word_count"),
                    "error": item.get("error"),
                }
            )
