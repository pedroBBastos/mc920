import numpy as np

random_array = np.random.rand(20)
print(random_array)

# print(np.sum(random_array, axis=1).shape)
horizontal_diff = np.diff(random_array)
print(horizontal_diff)