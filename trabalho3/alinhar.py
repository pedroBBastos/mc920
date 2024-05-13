import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys
import os

def rotate_image(image, angle):
    # Get image dimensions
    rows, cols = image.shape[:2]
    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    # Perform the rotation
    rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))
    return rotated_image

def funcao_objetivo(binaryImage):
    histograma = np.sum(binaryImage, axis=1)
    diff_squared = np.diff(histograma) ** 2
    sum_of_squares = np.sum(diff_squared)
    return sum_of_squares

parser = argparse.ArgumentParser()
parser.add_argument('--inputImg', type=str, help='Image to be text aligned')

args = parser.parse_args()
if len(sys.argv[1:]) < 2:
    print(args._get_args())
    parser.print_help()
    exit()

# Load the image in grayscale
image_gray = cv2.imread(args.inputImg, cv2.IMREAD_GRAYSCALE)

# Apply thresholding
_, binary_image = cv2.threshold(image_gray, 127, 1, cv2.THRESH_BINARY)

print(binary_image.shape)

# Display the binary image using Matplotlib
plt.imshow(binary_image, cmap='gray')
plt.axis('off')
plt.show()

# rotated_binary_image = rotate_image(binary_image, -14.9)

# # Display the binary image using Matplotlib
# plt.imshow(rotated_binary_image, cmap='gray')
# plt.axis('off')
# plt.show()


rotationPace = -0.2
currentRotation = -0.2
i = 0

melhorValorFuncObj = float('-inf')
melhorRotacaoParaAlinhamento = None

while currentRotation >= -90:
    currentRotatedImage = rotate_image(binary_image, currentRotation)
    valorFuncaoObjetivo = funcao_objetivo(currentRotatedImage)

    if valorFuncaoObjetivo > melhorValorFuncObj:
        melhorValorFuncObj = valorFuncaoObjetivo
        melhorRotacaoParaAlinhamento = currentRotation

    # print(i, "- currentRotation -> ", currentRotation, " - valorFuncaoObjetivo -> ", valorFuncaoObjetivo)
    currentRotation += rotationPace
    i += 1

print("Melhor angulo para rotação -> ", melhorRotacaoParaAlinhamento)