class DiskAnalyzer:

    def __init__(self, drive_data):
        self.drive = drive_data
        self.warnings = []
        self.score = 100

    def analyze_temperature(self):
        temp = int(self.drive["temp"]) if self.drive["temp"] else None

        if temp:
            if temp > 70:
                self.warnings.append("Critical temperature")
                self.score -= 30
            elif temp > 60:
                self.warnings.append("High temperature")
                self.score -= 15

    def analyze_health(self):
        health = int(self.drive["health"]) if self.drive["health"] else None

        if health:
            if health < 70:
                self.warnings.append("Health critical")
                self.score -= 40
            elif health < 90:
                self.warnings.append("Health degraded")
                self.score -= 20

    def analyze_power_on_hours(self):
        power_on_hours = int(self.drive["hours"])
        print (power_on_hours)
        if power_on_hours > 30000:

            self.warnings.append("Drive is old")

    def final_status(self):
        if self.score >= 90:
            return "Excellent"
        elif self.score >= 75:
            return "Good"
        elif self.score >= 50:
            return "Warning"
        else:
            return "Critical"

    def run(self):
        self.analyze_temperature()
        self.analyze_health()
        self.analyze_power_on_hours()

        return {
            "model": self.drive["model"],
            "score": self.score,
            "status": self.final_status(),
            "warnings": self.warnings
        }
