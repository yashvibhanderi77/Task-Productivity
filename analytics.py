import pandas as pd
import numpy as np


class TaskAnalytics:
    """Uses Pandas and NumPy to calculate productivity information."""

    def __init__(self, tasks):
        self.data = pd.DataFrame(tasks)
        self.completed = pd.DataFrame()

        if not self.data.empty:
            self.data["created_at"] = pd.to_datetime(self.data["created_at"], errors="coerce")
            self.data["completed_at"] = pd.to_datetime(self.data["completed_at"], errors="coerce")
            self.completed = self.data[self.data["status"] == "Completed"].copy()

            if not self.completed.empty:
                self.completed["hours"] = (
                    self.completed["completed_at"] - self.completed["created_at"]
                ).dt.total_seconds() / 3600

    def statistics(self):
        total = len(self.data)
        completed = len(self.completed)
        pending = total - completed

        # NumPy Array: completion times are stored and calculated numerically.
        times = np.array(self.completed["hours"].dropna(), dtype=float)

        if len(times) > 0:
            average = float(np.mean(times))
            fastest = float(np.min(times))
            slowest = float(np.max(times))
            peak_hour = int(self.completed["completed_at"].dt.hour.mode().iloc[0])
        else:
            average = fastest = slowest = 0
            peak_hour = None

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "average": average,
            "fastest": fastest,
            "slowest": slowest,
            "peak_hour": peak_hour,
            "completion_array": times
        }

    def category_comparison(self):
        if self.completed.empty:
            return {}
        return self.completed.groupby("category")["hours"].mean().round(2).to_dict()

    def period_comparison(self):
        if self.completed.empty:
            return {}
        dates = self.completed["completed_at"].dt.strftime("%Y-%m-%d")
        return dates.value_counts().sort_index().to_dict()

    def completion_by_hour(self):
        if self.completed.empty:
            return {}
        hours = self.completed["completed_at"].dt.hour
        return hours.value_counts().sort_index().to_dict()
