import tkinter as tk
from tkinter import ttk, messagebox

from task_manager import TaskManager
from analytics import TaskAnalytics
from charts import show_bar_chart, show_graph
from utils import valid_task_name, valid_date


manager = TaskManager()
manager.load_tasks()

root = tk.Tk()
root.title("Task Productivity Analyzer - Semester 5")
root.geometry("1100x680")
root.configure(bg="#eef4f7")

# Simple colours for the GUI
BG = "#eef4f7"
FRAME_BG = "#ffffff"
TEXT = "#1f2937"
ADD_COLOR = "#2e7d32"
APPLY_COLOR = "#1976d2"
CLEAR_COLOR = "#757575"
COMPLETE_COLOR = "#388e3c"
DELETE_COLOR = "#d32f2f"
STAT_COLOR = "#6a1b9a"
CHART_COLOR = "#ef6c00"
GRAPH_COLOR = "#00838f"
REPORT_COLOR = "#455a64"


def refresh_table():
    try:
        for row in table.get_children():
            table.delete(row)

        tasks = manager.search_filter(search_var.get(), category_filter_var.get(), status_filter_var.get())
        for item in tasks:
            table.insert("", "end", values=(
                item["id"], item["task"], item["category"], item["priority"],
                item["created_at"], item["due_date"], item["status"], item["completed_at"]
            ))

        total = len(manager.tasks)
        completed = sum(item["status"] == "Completed" for item in manager.tasks)
        summary.config(text=f"Total: {total}    Completed: {completed}    Pending: {total - completed}")
    except Exception as error:
        messagebox.showerror("Error", str(error))


def add_task():
    try:
        if not valid_task_name(task_var.get()):
            messagebox.showwarning("Validation", "Task name cannot be empty.")
            return

        if not valid_date(due_var.get()):
            messagebox.showwarning("Validation", "Use date format YYYY-MM-DD.")
            return

        manager.add_task(task_var.get(), category_var_add.get(), priority_var.get(), due_var.get())
        manager.save_tasks()
        task_var.set("")
        due_var.set("")
        refresh_table()
        messagebox.showinfo("Success", "Task added successfully.")
    except Exception as error:
        messagebox.showerror("Error", str(error))


def get_selected_id():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("Select Task", "Please select a task first.")
        return None
    return table.item(selected[0])["values"][0]


def complete_task():
    try:
        task_id = get_selected_id()
        if task_id is not None:
            if manager.complete_task(task_id):
                manager.save_tasks()
                refresh_table()
                messagebox.showinfo("Success", "Task marked as completed.")
    except Exception as error:
        messagebox.showerror("Error", str(error))


def delete_task():
    try:
        task_id = get_selected_id()
        if task_id is not None and messagebox.askyesno("Delete", "Delete selected task?"):
            manager.delete_task(task_id)
            manager.save_tasks()
            refresh_table()
    except Exception as error:
        messagebox.showerror("Error", str(error))


def show_statistics():
    try:
        stats = TaskAnalytics(manager.tasks).statistics()
        peak = "No data" if stats["peak_hour"] is None else f"{stats['peak_hour']:02d}:00"
        messagebox.showinfo(
            "Productivity Statistics",
            f"Total Tasks: {stats['total']}\n"
            f"Completed: {stats['completed']}\n"
            f"Pending: {stats['pending']}\n"
            f"Average Completion Time: {stats['average']:.2f} hours\n"
            f"Fastest Completion: {stats['fastest']:.2f} hours\n"
            f"Slowest Completion: {stats['slowest']:.2f} hours\n"
            f"Most Common Completion Hour: {peak}"
        )
    except Exception as error:
        messagebox.showerror("Error", str(error))


def open_bar_chart():
    try:
        show_bar_chart(TaskAnalytics(manager.tasks))
    except Exception as error:
        messagebox.showerror("Chart Error", str(error))


def open_graph():
    try:
        show_graph(TaskAnalytics(manager.tasks))
    except Exception as error:
        messagebox.showerror("Graph Error", str(error))


def show_report():
    try:
        analytics = TaskAnalytics(manager.tasks)
        stats = analytics.statistics()
        report = (
            "TASK PRODUCTIVITY REPORT\n"
            "=========================\n\n"
            f"Total Tasks: {stats['total']}\n"
            f"Completed: {stats['completed']}\n"
            f"Pending: {stats['pending']}\n"
            f"Average Completion Time: {stats['average']:.2f} hours\n\n"
            "Average Time by Category:\n"
        )
        for category, hours in analytics.category_comparison().items():
            report += f"- {category}: {hours:.2f} hours\n"

        report += "\nCompleted Tasks by Date:\n"
        for date, count in analytics.period_comparison().items():
            report += f"- {date}: {count}\n"

        win = tk.Toplevel(root)
        win.title("Text Report")
        win.geometry("600x500")
        text_box = tk.Text(win, font=("Arial", 11))
        text_box.pack(fill="both", expand=True, padx=10, pady=10)
        text_box.insert("1.0", report)
        text_box.config(state="disabled")
    except Exception as error:
        messagebox.showerror("Report Error", str(error))


def clear_filter():
    search_var.set("")
    category_filter_var.set("All")
    status_filter_var.set("All")
    refresh_table()


# ---------- GUI ----------
tk.Label(root, text="TASK PRODUCTIVITY ANALYZER", font=("Arial", 22, "bold"), bg=BG, fg="#0d47a1").pack(pady=10)
tk.Label(root, text="Semester 5 Python Project - Manage and Analyze Tasks", bg=BG, fg=TEXT).pack()

input_frame = tk.LabelFrame(root, text="Add Task", padx=10, pady=10, bg=FRAME_BG, fg="#0d47a1")
input_frame.pack(fill="x", padx=15, pady=10)

task_var = tk.StringVar()
category_var_add = tk.StringVar(value="Study")
priority_var = tk.StringVar(value="Medium")
due_var = tk.StringVar()

fields = ["Task Name", "Category", "Priority", "Due Date (YYYY-MM-DD)"]
for i, label in enumerate(fields):
    tk.Label(input_frame, text=label, bg=FRAME_BG, fg=TEXT).grid(row=0, column=i, padx=5)

tk.Entry(input_frame, textvariable=task_var, width=25).grid(row=1, column=0, padx=5)
ttk.Combobox(input_frame, textvariable=category_var_add,
             values=["Study", "Work", "Personal", "Health", "Project", "Other"],
             state="readonly", width=14).grid(row=1, column=1, padx=5)
ttk.Combobox(input_frame, textvariable=priority_var,
             values=["Low", "Medium", "High"], state="readonly", width=12).grid(row=1, column=2, padx=5)
tk.Entry(input_frame, textvariable=due_var, width=18).grid(row=1, column=3, padx=5)
tk.Button(input_frame, text="Add Task", command=add_task, width=12, bg=ADD_COLOR, fg="white", activebackground="#1b5e20", activeforeground="white").grid(row=1, column=4, padx=10)

filter_frame = tk.LabelFrame(root, text="Search and Filter", padx=10, pady=8, bg=FRAME_BG, fg="#0d47a1")
filter_frame.pack(fill="x", padx=15)

search_var = tk.StringVar()
category_filter_var = tk.StringVar(value="All")
status_filter_var = tk.StringVar(value="All")

tk.Label(filter_frame, text="Search:", bg=FRAME_BG, fg=TEXT).pack(side="left")
tk.Entry(filter_frame, textvariable=search_var, width=20).pack(side="left", padx=5)
ttk.Combobox(filter_frame, textvariable=category_filter_var,
             values=["All", "Study", "Work", "Personal", "Health", "Project", "Other"],
             state="readonly", width=12).pack(side="left")
ttk.Combobox(filter_frame, textvariable=status_filter_var,
             values=["All", "Pending", "Completed"], state="readonly", width=12).pack(side="left", padx=5)
tk.Button(filter_frame, text="Apply", command=refresh_table, width=10, bg=APPLY_COLOR, fg="white", activebackground="#0d47a1", activeforeground="white").pack(side="left", padx=5)
tk.Button(filter_frame, text="Clear", command=clear_filter, width=10, bg=CLEAR_COLOR, fg="white", activebackground="#424242", activeforeground="white").pack(side="left")

# Task table
table_frame = tk.Frame(root, bg=BG)
table_frame.pack(fill="both", expand=True, padx=15, pady=10)

columns = ("ID", "Task", "Category", "Priority", "Created", "Due", "Status", "Completed At")
table = ttk.Treeview(table_frame, columns=columns, show="headings")
for column in columns:
    table.heading(column, text=column)
    table.column(column, width=120)
table.column("Task", width=220)
table.pack(side="left", fill="both", expand=True)

scroll = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
scroll.pack(side="right", fill="y")
table.configure(yscrollcommand=scroll.set)

button_frame = tk.Frame(root, bg=BG)
button_frame.pack(pady=5)

buttons = [
    ("Mark Complete", complete_task, COMPLETE_COLOR),
    ("Delete", delete_task, DELETE_COLOR),
    ("Statistics", show_statistics, STAT_COLOR),
    ("Bar Chart", open_bar_chart, CHART_COLOR),
    ("Graph", open_graph, GRAPH_COLOR),
    ("Text Report", show_report, REPORT_COLOR),
]
for text, command, color in buttons:
    tk.Button(button_frame, text=text, command=command, width=14, bg=color, fg="white", activebackground=color, activeforeground="white").pack(side="left", padx=4)

summary = tk.Label(root, font=("Arial", 11, "bold"), bg=BG, fg="#0d47a1")
summary.pack(pady=6)

refresh_table()
root.mainloop()
