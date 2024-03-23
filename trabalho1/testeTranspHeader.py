import pickle
import cv2 as cv
import numpy as np

# -----------------------------------

array1 = np.array([1, 2, 3])
array2 = np.array([4, 5, 6])
array3 = np.array([7, 8, 9])

# Vertically stack the arrays to create a matrix
result_matrix = np.vstack((array1, array2, array3))

# Print the resulting matrix
print("Resulting matrix:")
print(result_matrix.shape)

result_matrix_T = np.transpose(result_matrix, (1,0))
print(result_matrix_T)

# ---------------------------------------------------------
print("------------------")

my_dict = {'key1': 'value1', 'key2': 'value2'}
serialized_bytes = pickle.dumps(my_dict)
np_array = np.frombuffer(serialized_bytes, dtype=np.uint8)
print(np_array)

mask3LastBits = 7 # 0b111
myArray = np.empty((3), dtype=np.uint8)

for n in np_array:
    copy = n
    intoRed = copy & mask3LastBits
    copy >>= 3
    intoGreen = copy & mask3LastBits
    copy >>= 3
    intoBlue = copy
    current = np.array([intoRed, intoGreen, intoBlue])
    myArray = np.vstack((myArray, current))

print(myArray[1:])
resultHeader = np.transpose(myArray[1:], (1,0))
print(resultHeader)
print(resultHeader.shape)

# -------------------------
print("-------------------------")

def move3LastBits(x, y):
  masc = 1 << 3
  masc -= 1
  masc = ~masc

  auxX = x & masc

  mascaraParaPegarNUltimosBits = 2**3 - 1
  bitsToBePlaced = y & mascaraParaPegarNUltimosBits
  return auxX ^ bitsToBePlaced

def move2LastBits(x, y):
  masc = 1 << 2
  masc -= 1
  masc = ~masc

  auxX = x & masc

  mascaraParaPegarNUltimosBits = 2**2 - 1
  bitsToBePlaced = y & mascaraParaPegarNUltimosBits
  return auxX ^ bitsToBePlaced


img = cv.imread('../images/baboon.png')
img = np.transpose(img, (2,1,0))
print(img.shape)

aux = img[:, :, :resultHeader.shape[1]]
print(aux.shape)

myMove3 = np.frompyfunc(move3LastBits, 2, 1)
myMove2 = np.frompyfunc(move2LastBits, 2, 1)

# print(myMove3(aux[0], resultHeader[0]))
# print(myMove3(aux[1], resultHeader[1]))
# print(myMove2(aux[2], resultHeader[2]))

final = myMove3(aux[0], resultHeader[0])
final = np.vstack((final, myMove3(aux[1], resultHeader[1])))
final = np.vstack((final, myMove2(aux[2], resultHeader[2])))
print(final.shape)
final = np.reshape(final, (3, 512, 48))
print(final.shape)

img[:, :, :resultHeader.shape[1]] = final
img = np.transpose(img, (2,1,0))
cv.imshow('image with a header hidden in it', img)
cv.waitKey(0)
cv.imwrite('output.png', img)