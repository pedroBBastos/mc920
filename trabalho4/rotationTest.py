import cv2
import numpy as np
import math

def rotate_image(inputImg, outputImg, inverseScaleMatrix):
    outputRows, outptColumns = outputImg.shape[:2]
    for row in range(outputRows):
        for column in range(outptColumns):
            currentOutputPixel = np.array([
                                          [column],
                                          [row],
                                          [1]
                                        ])
            inputImgPixel = inverseScaleMatrix @ currentOutputPixel

            inputImgRow = int(inputImgPixel[1,0])
            inputImgColumn = int(inputImgPixel[0,0])

            inputImgRow = inputImgRow if inputImgRow < 512 and inputImgRow >= 0 else -1
            inputImgColumn = inputImgColumn if inputImgColumn < 512 and inputImgColumn >= 0 else -1

            if inputImgRow == -1 or inputImgColumn == -1:
                outputImg[row, column] = 0
            else:
                outputImg[row, column] = inputImg[inputImgRow, inputImgColumn]


image = cv2.imread('./images/baboon.png', cv2.IMREAD_GRAYSCALE)
print(image.shape)
image_height, image_width = image.shape[:2]



rotationFactor = -80
rotationFactorRadians = np.radians(rotationFactor)

output_image = np.zeros(image.shape, dtype=np.uint8)

rotationMatrix = np.array([
                        [math.cos(rotationFactorRadians), -math.sin(rotationFactorRadians), 0],
                        [math.sin(rotationFactorRadians), math.cos(rotationFactorRadians), 0],
                        [0, 0, 1]
                    ])
translationToOriginMatrix = np.array([
                        [1, 0, -(image_width // 2)],
                        [0, 1, -(image_height // 2)],
                        [0, 0, 1]
                    ])
translationBackMatrix = np.array([
                        [1, 0, (image_width // 2)],
                        [0, 1, (image_height // 2)],
                        [0, 0, 1]
                    ])

resultingTransformation = translationBackMatrix @ rotationMatrix @ translationToOriginMatrix
inverse_matrix = np.linalg.inv(resultingTransformation)

rotate_image(image, output_image, inverse_matrix)
cv2.imwrite('rotated_img.png', output_image)
print(resultingTransformation)
print(inverse_matrix)
print(inverse_matrix @ resultingTransformation)