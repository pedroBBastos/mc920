import numpy as np

string = "mais um teste aqui..."

print(type(string[:]))

ascii_array = [ord(char) for char in string]
print(ascii_array)

numpy_array = np.array(ascii_array)
print("NumPy array:", numpy_array)

numpy_array = np.reshape(numpy_array, (3,7))
print("NumPy array:")
print(numpy_array)