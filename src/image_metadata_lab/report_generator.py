import csv
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

def _to_jsonable(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat(sep=" ", timespec="seconds")
    
    return value

def summaries_to_rows(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for item in items:
        row = {k: _to_jsonable(v) for k, v in item.items()}
        rows.append(row)
    
    return rows

def write_json(output_path: str, rows: List[Dict[str, Any]]) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2, default=_to_jsonable())

def write_csv(output_path: str, rows: List[Dict[str, Any]]) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            f.write("filename,date_time_original,latitude,longitude\n")
            return
        
    fieldnames = ["filename", "date_time_original", "latitude", "longitude"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)