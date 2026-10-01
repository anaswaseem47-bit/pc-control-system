from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


def _chrome_history_candidates() -> list[Path]:
    home = Path.home()
    candidates = [
        home / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "History",
        home / "AppData" / "Local" / "Google" / "Chrome SxS" / "User Data" / "Default" / "History",
        home / "AppData" / "Local" / "Chromium" / "User Data" / "Default" / "History",
        home / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data" / "Default" / "History",
        home / "AppData" / "Local" / "BraveSoftware" / "Brave-Browser" / "User Data" / "Default" / "History",
    ]
    return [p for p in candidates if p.exists()]


def _chrome_time_to_iso(value: int | float | None) -> str:
    if value in (None, 0):
        return "N/A"
    try:
        epoch = datetime(1601, 1, 1)
        unix_seconds = float(value) / 10_000_000
        return (epoch.timestamp() + unix_seconds)
    except Exception:
        return "N/A"


def get_recent_chrome_history(limit: int = 10) -> list[dict]:
    results: list[dict] = []
    for history_file in _chrome_history_candidates():
        try:
            conn = sqlite3.connect(str(history_file))
            rows = conn.execute(
                "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT ?",
                (limit,),
            ).fetchall()
            conn.close()

            for url, title, last_visit_time in rows:
                parsed = urlparse(url)
                results.append({
                    "url": url,
                    "title": title or "Untitled",
                    "domain": parsed.netloc or "unknown",
                    "visited_at": _chrome_time_to_iso(last_visit_time),
                })
            if results:
                return results[:limit]
        except Exception:
            continue
    return results[:limit]


if __name__ == "__main__":
    print(get_recent_chrome_history(5))
