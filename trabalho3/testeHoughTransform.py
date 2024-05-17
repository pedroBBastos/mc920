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
image = cv2.imread(args.inputImg, cv2.IMREAD_GRAYSCALE)

_, binary_image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)

# Convert the image to grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Sobel edge detection
sobel_x = cv2.Sobel(binary_image, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(binary_image, cv2.CV_64F, 0, 1, ksize=3)

# Compute gradient magnitude
gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

# Convert gradient magnitude to uint8
gradient_magnitude = np.uint8(255 * gradient_magnitude / np.max(gradient_magnitude))

_, edge_image = cv2.threshold(gradient_magnitude, 50, 255, cv2.THRESH_BINARY)

# Apply Hough Line Transform on the edge-detected image
lines = cv2.HoughLines(edge_image, 1, np.pi/180, threshold=200)  # Adjust the threshold as needed

# Draw detected lines on the original image
result_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
if lines is not None:
    thetaArray = []
    for rho, theta in lines[:, 0]:
        print("theta -> ", math.degrees(theta))
        thetaArray.append(math.degrees(theta))
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(result_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    thetaAverage = np.average(thetaArray)
    print("np.average(theta) -> ", thetaAverage)
    if thetaAverage < 90:
        print("Angulo final é ", 90 - thetaAverage)
    else:
        print("Angulo final é ", thetaAverage - 90)
else:
    print("lines is None.............. )=")

# Display the result
plt.imshow(result_image, cmap='gray')
plt.axis('off')
plt.show()