import json
import os
from datetime import datetime


class HistoryManager:

    def __init__(self, file="history.json"):
        self.file = file
        self.data = self.load()

    def load(self):
        if not os.path.exists(self.file):
            return {}
        with open(self.file, "r") as f:
            return json.load(f)

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=4)

    def add_record(self, drive_report):
        model = drive_report["model"]
        timestamp = datetime.now().isoformat()

        entry = {
            "time": timestamp,
            "health": drive_report.get("health"),
            "score": drive_report.get("score"),
            "temp": drive_report.get("temp"),
            "writes": drive_report.get("writes"),
        }

        if model not in self.data:
            self.data[model] = []

        self.data[model].append(entry)
        self.save()

    def get_history(self, model):
        return self.data.get(model, [])
