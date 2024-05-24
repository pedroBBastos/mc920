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

parser = argparse.ArgumentParser()
parser.add_argument('--inputImg', type=str, help='Image to be text aligned')

args = parser.parse_args()
if len(sys.argv[1:]) < 2:
    print(args._get_args())
    parser.print_help()
    exit()

# Load the image in grayscale
image_gray = cv2.imread(args.inputImg, cv2.IMREAD_GRAYSCALE)

# Display the binary image using Matplotlib
plt.imshow(image_gray, cmap='gray')
plt.axis('off')
plt.show()

currentRotatedImage = rotate_image(image_gray, 47)
cv2.imwrite('testeRotacao_47_.png', currentRotatedImage)

currentRotatedImage = rotate_image(image_gray, 144)
cv2.imwrite('testeRotacao_144_.png', currentRotatedImage)

currentRotatedImage = rotate_image(image_gray, 210)
cv2.imwrite('testeRotacao_210_.png', currentRotatedImage)

currentRotatedImage = rotate_image(image_gray, 311)
cv2.imwrite('testeRotacao_311_.png', currentRotatedImage)
