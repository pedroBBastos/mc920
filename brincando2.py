import random

print(random.randint(2, 55))

# Define a character
char = 'A'
# Get the ASCII value of the character
ascii_value = ord(char)
# Print the ASCII value
print("ASCII value of char '", char, "' is ", ascii_value)

# --------------------------------------

# Define an integer
integer_number = 42
# Get the binary representation of the integer
binary_representation = bin(integer_number)
# Print the binary representation
print("Binary value of integer ", integer_number, " is ", binary_representation)

# --------------------------------------

print("-------------------------------")
a = random.randint(0, 1000)
bin1 = bin(a)

b = random.randint(0, 1000)
bin2 = bin(b)

print("bin1: ", bin1)
print("bin2: ", bin2)

print("bin1 & bin2 = ", bin(a ^ b))

print("-------------------------------")

# --------------------------------------

print("Pegando os n (3 nesse caso) bits menos significativos de um numero")
print("Máscara -> ", bin(7))
c = random.randint(0, 1000)
print("c = ", c, " (", bin(c),"), c & 7 (0b111) => ", bin(c & 7))

print("Pegando os n (2 nesse caso) bits menos significativos de um numero")
print("Máscara -> ", bin(3))
d = random.randint(0, 1000)
print("d = ", d, " (", bin(d),"), d & 3 (0b11) => ", bin(d & 3))

# --------------------------------------

print("a -> ", ord('a'))

# --------------------------------------

