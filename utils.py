from datetime import datetime


def valid_task_name(name):
    return bool(name.strip())


def valid_date(date_text):
    if date_text.strip() == "":
        return True
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False
