import matplotlib.pyplot as plt


def show_bar_chart(analytics):
    """Bar chart: average completion time for each category."""
    data = analytics.category_comparison()
    if not data:
        show_empty("No completed task data for Bar Chart")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(data.keys(), data.values())
    plt.title("Average Completion Time by Category")
    plt.xlabel("Category")
    plt.ylabel("Average Hours")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.show()


def show_graph(analytics):
    """Line graph: number of completed tasks at each hour."""
    data = analytics.completion_by_hour()
    if not data:
        show_empty("No completed task data for Graph")
        return

    hours = list(range(24))
    values = [data.get(hour, 0) for hour in hours]

    plt.figure(figsize=(9, 5))
    plt.plot(hours, values, marker="o")
    plt.title("Task Completion by Time of Day")
    plt.xlabel("Hour of Day")
    plt.ylabel("Number of Completed Tasks")
    plt.xticks(hours)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def show_empty(message):
    plt.figure(figsize=(7, 4))
    plt.text(0.5, 0.5, message, ha="center", va="center")
    plt.axis("off")
    plt.show()
