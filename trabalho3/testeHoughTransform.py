import cv2
import numpy as np
import argparse
import sys
import matplotlib.pyplot as plt
import math

parser = argparse.ArgumentParser()
parser.add_argument('--inputImg', type=str, help='Image to be text aligned')

args = parser.parse_args()
if len(sys.argv[1:]) < 2:
    print(args._get_args())
    parser.print_help()
    exit()

# Load the image
image = cv2.imread(args.inputImg)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Sobel edge detection
sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

# Compute gradient magnitude
gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

# Convert gradient magnitude to uint8
gradient_magnitude = np.uint8(255 * gradient_magnitude / np.max(gradient_magnitude))

# Apply Hough Line Transform on the edge-detected image
lines = cv2.HoughLines(gradient_magnitude, 1, np.pi/180, threshold=460)  # Adjust the threshold as needed

# Draw detected lines on the original image
if lines is not None:
    for rho, theta in lines[:, 0]:
        print("theta -> ", math.degrees(theta))
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Display the result
plt.imshow(image, cmap='gray')
plt.axis('off')
plt.show()