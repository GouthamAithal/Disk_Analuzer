class DiskPredictor:

    def __init__(self, drive):
        self.drive = drive

    def estimate_wear_rate(self):
        hours = int(self.drive["hours"]) if self.drive["hours"] else 0
        health = int(self.drive["health"]) if self.drive["health"] else 100

        if hours == 0:
            return 0

        years = hours / 8760
        wear_used = 100 - health

        return wear_used / years if years else 0

    def estimate_remaining_life(self):
        wear_rate = self.estimate_wear_rate()

        if wear_rate == 0:
            return "Unknown"

        remaining_percent = int(self.drive["health"])
        years_left = remaining_percent / wear_rate

        return round(years_left, 2)

    def risk_level(self):
        health = int(self.drive["health"])
        temp = int(self.drive["temp"])

        if health < 70 or temp > 70:
            return "High"

        if health < 85 or temp > 60:
            return "Medium"

        return "Low"

    def run(self):
        return {
            "wear_rate_per_year": round(self.estimate_wear_rate(), 2),
            "estimated_years_left": self.estimate_remaining_life(),
            "risk_level": self.risk_level()
        }
