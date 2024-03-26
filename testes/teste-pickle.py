import pickle
import numpy as np

# Define a dictionary
my_dict = {'key1': 'value1', 'key2': 'value2'}

# Serialize the dictionary into bytes
serialized_bytes = pickle.dumps(my_dict)

# Print the serialized bytes
print("Serialized bytes:", serialized_bytes)
print("Type -> ", type(serialized_bytes))

# Convert bytes to NumPy array of np.uint8
np_array = np.frombuffer(serialized_bytes, dtype=np.uint8)

# Print the NumPy array
print("NumPy array:", np_array)
print("NumPy array size:", np_array.size)