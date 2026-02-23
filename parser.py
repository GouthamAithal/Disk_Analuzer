import re
from analyzer import DiskAnalyzer
from predictor import DiskPredictor
from history import HistoryManager

class DiskParser:
    def __init__(self, filepath):
        with open(filepath, "r", encoding = "utf-8") as f:
            self.text = f.read()

    def split_drives(self):
        return self.text.split("-------------")

    def extract(self, pattern, text):
        match = re.search(pattern, text)
        return match.group(1).strip() if match else None

    def get_drives_blocks(self):
        blocks = self.split_drives()
        return [b for b in blocks if "Model :" in b]

    def parse_drive(self, block):
        return {
        "model": self.extract(r"Model\s+:\s+(.*)", block),
        "firmware": self.extract(r"Firmware\s+:\s+(.*)", block),
        "serial": self.extract(r"Serial Number\s+:\s+(.*)", block),
        "size": self.extract(r"Disk Size\s+:\s+(.*)", block),
        "temp": self.extract(r"Temperature\s+:\s+(\d+)", block),
        "health": self.extract(r"Health Status\s+:\s+.*\((\d+)", block),
        "hours": self.extract(r"Power On Hours\s+:\s+(\d+)", block),
        "reads": self.extract(r"Host Reads\s+:\s+(\d+)", block),
        "writes": self.extract(r"Host Writes\s+:\s+(\d+)", block),
    }

    def parse_all(self):
        drives = []
        for block in self.get_drives_blocks():
            drives.append(self.parse_drive(block))
        return drives
history = HistoryManager()
if __name__ == "__main__":
    parser = DiskParser("sample_log.txt")
    drives = parser.parse_all()

    for d in drives:
        analysis = DiskAnalyzer(d).run()
        prediction = DiskPredictor(d).run()
        report = {**d, **analysis, **prediction}
        history.add_record(report)
        print (report)