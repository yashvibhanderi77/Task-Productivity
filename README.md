# Task Productivity Analyzer - Semester 5

A simple Python project made for Semester 5. It uses Tkinter, CSV, Pandas, NumPy and Matplotlib.

## Main Features

1. Add task details: task name, category, priority and due date.
2. Store task status as Pending or Completed.
3. Record the completion date and time.
4. Search tasks by task name or category.
5. Filter tasks by category and status.
6. Calculate total, completed, pending, average, fastest and slowest completion time.
7. Compare average completion time by category.
8. Compare completed tasks by date/period.
9. Find the most common completion hour to identify a pattern.
10. Show two separate Matplotlib reports: Bar Chart and Graph.
11. Save all data permanently in `tasks.csv`.

## Modules

- `main.py` - Tkinter GUI and program control.
- `task_manager.py` - task operations and CSV file handling.
- `analytics.py` - Pandas and NumPy analysis.
- `charts.py` - Matplotlib visualizations.
- `utils.py` - input validation.

There are 5 user-defined modules, so the 3-module requirement is covered.

## Required Technologies

### Python functions and data structures
Functions, classes, lists, dictionaries and loops are used throughout the project.

### File handling
`tasks.csv` is used for permanent storage. The program reads the file when it starts and saves changes after add, complete or delete operations.

### NumPy Array
`analytics.py` creates a real NumPy array of completion times. `np.mean()`, `np.min()` and `np.max()` are used for calculations.

### Pandas
Pandas DataFrame is used to organize task records, convert dates and compare categories/periods.

### Tkinter GUI
The complete application is made using Tkinter and ttk widgets.

### Matplotlib
Two meaningful visualizations are provided with separate buttons:

- **Bar Chart:** Average Completion Time by Category.
- **Graph:** Task Completion by Time of Day.

### Input validation
- Task name cannot be empty.
- Due date must be `YYYY-MM-DD` or can be blank.

### Exception handling
`try-except` is used for file handling, task operations, filtering, analysis, GUI operations and charts.

### Testing
Run:

```text
python -m unittest test_task_manager.py
```

## How to Run

1. Install Python 3.
2. Open Command Prompt in this folder.
3. Install libraries:

```text
pip install -r requirements.txt
```

4. Run the project:

```text
python main.py
```

## Requirement Checklist

- Maintain task details and status: YES
- Search/filter: YES
- Record completion information: YES
- Completion statistics: YES
- Category comparison: YES
- Period/date comparison: YES
- Pattern identification: YES
- At least two visual reports: YES
- Python functions/data structures: YES
- Persistent file handling: YES
- Minimum 3 user-defined modules: YES (5 modules)
- Meaningful NumPy/Pandas use: YES
- Tkinter GUI: YES
- At least 2 Matplotlib visualizations: YES
- Input validation: YES
- Exception handling: YES
- Documentation/testing: YES
