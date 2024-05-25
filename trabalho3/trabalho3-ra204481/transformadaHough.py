import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def alinhar(inputImg, houghThreshold=400):
    _, binary_image = cv2.threshold(inputImg, 200, 255, cv2.THRESH_BINARY)

    sobel_x = cv2.Sobel(binary_image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(binary_image, cv2.CV_64F, 0, 1, ksize=3)

    gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    gradient_magnitude = np.uint8(255 * gradient_magnitude / np.max(gradient_magnitude))

    _, edge_image = cv2.threshold(gradient_magnitude, 50, 255, cv2.THRESH_BINARY)
    lines = cv2.HoughLines(edge_image, 1, np.pi/180, threshold=houghThreshold)

    result_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
    finalAngle = None
    if lines is not None:
        thetaArray = []
        for rho, theta in lines[:, 0]:
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

        # Display the result
        plt.imshow(result_image, cmap='gray')
        plt.axis('off')
        plt.show()
        
        if thetaAverage < 90:
            finalAngle = -(90 - thetaAverage)
            print("Angulo final é ", finalAngle)
        else:
            finalAngle = thetaAverage - 90
            print("Angulo final é ", finalAngle)
    else:
        plt.imshow(binary_image, cmap='gray')
        plt.axis('off')
        plt.show()
        print("No Hough lines found using hough threshold ", houghThreshold, ".......... )=")

    return finalAngle