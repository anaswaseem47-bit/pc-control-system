from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


class UsageLearner:
    def __init__(self, file_name: str = "usage_data.json"):
        self.file_path = Path(file_name)
        self.history = self._load()

    def _load(self) -> dict:
        if not self.file_path.exists():
            return {"commands": [], "sites": []}
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return {
                        "commands": data.get("commands", []),
                        "sites": data.get("sites", []),
                    }
        except Exception:
            pass
        return {"commands": [], "sites": []}

    def _save(self) -> None:
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2)

    def record_command(self, command: str) -> None:
        cmd = command.strip().lower()
        if cmd:
            self.history.setdefault("commands", []).append(cmd)
            self._save()

    def record_site(self, site: str) -> None:
        value = site.strip().lower()
        if value:
            self.history.setdefault("sites", []).append(value)
            self._save()

    def generate_summary(self) -> dict:
        commands = Counter(self.history.get("commands", []))
        sites = Counter(self.history.get("sites", []))
        return {
            "top_commands": [item for item, _ in commands.most_common(5)],
            "top_sites": [item for item, _ in sites.most_common(5)],
            "total_commands": sum(commands.values()),
            "total_sites": sum(sites.values()),
        }


if __name__ == "__main__":
    learner = UsageLearner()
    learner.record_command("lock pc")
    learner.record_site("github.com")
    print(learner.generate_summary())
