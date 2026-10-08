import csv
import os
from datetime import datetime

FIELDS = ["id", "task", "category", "priority", "created_at", "due_date", "status", "completed_at"]

class TaskManager:
    def __init__(self, file_name="tasks.csv"):
        # Always keep the CSV file in the same folder as this Python file.
        if not os.path.isabs(file_name):
            file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        self.file_name = file_name
        self.tasks = []

    def load_tasks(self):
        try:
            with open(self.file_name, "r", newline="", encoding="utf-8") as file:
                self.tasks = list(csv.DictReader(file))
        except FileNotFoundError:
            self.tasks = []
        except (OSError, csv.Error) as error:
            print("File reading error:", error)
            self.tasks = []

    def save_tasks(self):
        try:
            with open(self.file_name, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(self.tasks)
        except OSError as error:
            print("File saving error:", error)

    def add_task(self, task, category, priority, due_date):
        try:
            new_id = 1
            if self.tasks:
                new_id = max(int(item["id"]) for item in self.tasks) + 1

            new_task = {
                "id": str(new_id),
                "task": task.strip(),
                "category": category,
                "priority": priority,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "due_date": due_date.strip(),
                "status": "Pending",
                "completed_at": ""
            }
            self.tasks.append(new_task)
            return True
        except (ValueError, TypeError, KeyError) as error:
            print("Add task error:", error)
            return False

    def complete_task(self, task_id):
        try:
            for item in self.tasks:
                if int(item["id"]) == int(task_id):
                    item["status"] = "Completed"
                    item["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    return True
        except (ValueError, TypeError, KeyError) as error:
            print("Complete task error:", error)
        return False

    def delete_task(self, task_id):
        try:
            old_count = len(self.tasks)
            self.tasks = [item for item in self.tasks if int(item["id"]) != int(task_id)]
            return len(self.tasks) < old_count
        except (ValueError, TypeError, KeyError) as error:
            print("Delete task error:", error)
            return False

    def search_filter(self, search_text, category, status):
        result = []
        try:
            search_text = search_text.lower().strip()
            for item in self.tasks:
                search_ok = (search_text == "" or
                             search_text in item["task"].lower() or
                             search_text in item["category"].lower())
                category_ok = category == "All" or item["category"] == category
                status_ok = status == "All" or item["status"] == status
                if search_ok and category_ok and status_ok:
                    result.append(item)
        except (AttributeError, KeyError) as error:
            print("Search/filter error:", error)
        return result
