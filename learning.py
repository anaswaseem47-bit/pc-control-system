from __future__ import annotations

import time
from datetime import datetime

import psutil


def _format_bytes(value: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{value} B"


def get_network_summary() -> dict:
    counters = psutil.net_io_counters(pernic=True)
    total_sent = 0
    total_received = 0
    for stats in counters.values():
        total_sent += stats.bytes_sent
        total_received += stats.bytes_recv

    return {
        "bytes_sent": total_sent,
        "bytes_received": total_received,
        "bytes_sent_human": _format_bytes(total_sent),
        "bytes_received_human": _format_bytes(total_received),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }


def monitor_internet_usage(duration: int = 10, interval: int = 1) -> dict:
    start = get_network_summary()
    samples = []
    steps = max(1, int(duration / max(1, interval)))

    for _ in range(steps):
        time.sleep(interval)
        current = get_network_summary()
        sent_delta = current["bytes_sent"] - start["bytes_sent"]
        received_delta = current["bytes_received"] - start["bytes_received"]
        samples.append({
            "timestamp": current["timestamp"],
            "sent_delta": sent_delta,
            "received_delta": received_delta,
            "sent_delta_human": _format_bytes(sent_delta),
            "received_delta_human": _format_bytes(received_delta),
        })

    return {
        "duration_seconds": duration,
        "interval_seconds": interval,
        "samples": samples,
        "total_sent_delta": sum(s["sent_delta"] for s in samples),
        "total_received_delta": sum(s["received_delta"] for s in samples),
        "total_sent_human": _format_bytes(sum(s["sent_delta"] for s in samples)),
        "total_received_human": _format_bytes(sum(s["received_delta"] for s in samples)),
    }


if __name__ == "__main__":
    print(get_network_summary())
    print(monitor_internet_usage(3, 1))
