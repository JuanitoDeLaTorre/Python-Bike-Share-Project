import numpy as np

array = np.random.randint(0, 5001, size=(1000, 20))
averages_col = np.average(array, axis = 0)
std_dev = np.std(array, axis = 0)

mean_normalized = (array - averages_col) / std_dev

overall_average = np.average(mean_normalized)


print(np.average(np.max(mean_normalized, axis=0)))


