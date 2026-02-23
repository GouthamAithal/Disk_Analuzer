import json
import matplotlib.pyplot as plt
from datetime import datetime

class GraphEngine:

    def __init__(self, history_file="history.json"):
        with open(history_file) as f:
            self.data = json.load(f)

    def plot_metric(self, model, metric):
        if model not in self.data:
            return None

        records = self.data[model]

        times = [datetime.fromisoformat(r["time"]) for r in records]
        values = [float(r[metric]) for r in records if r[metric] is not None]

        fig, ax = plt.subplots()
        ax.plot(times, values, marker="o")
        ax.set_title(f"{metric.upper()} Trend — {model}")
        ax.set_xlabel("Time")
        ax.set_ylabel(metric)
        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

