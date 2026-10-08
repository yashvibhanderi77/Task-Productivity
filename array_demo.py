import numpy as np

# Simple NumPy Array example used in the project.
completion_times = np.array([2.0, 1.5, 3.0, 2.5])

print("Completion Time Array:", completion_times)
print("Average:", np.mean(completion_times))
print("Fastest:", np.min(completion_times))
print("Slowest:", np.max(completion_times))
