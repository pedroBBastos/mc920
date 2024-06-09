import cv2
import numpy as np

def scale_image(inputImg, outputImg, inverseScaleMatrix):
    outputRows, outptColumns = outputImg.shape[:2]
    for row in range(outputRows):
        for column in range(outptColumns):
            currentOutputPixel = np.array([
                                          [column],
                                          [row],
                                          [1]
                                        ])
            inputImgPixel = inverseScaleMatrix @ currentOutputPixel
            outputImg[row, column] = inputImg[int(inputImgPixel[1,0])%512, int(inputImgPixel[0,0])%512]

image = cv2.imread('./images/baboon.png', cv2.IMREAD_GRAYSCALE)
print(image.shape)

scaleFactor = 2.4

output_image = np.zeros((int(image.shape[0]*scaleFactor), 
                         int(image.shape[1]*scaleFactor)), dtype=np.uint8)
print("output_image.shape -> ", output_image.shape)

scaleMatrix = np.array([
                        [scaleFactor, 0, 0],
                        [0, scaleFactor, 0],
                        [0, 0, 1]
                    ])
inverse_matrix = np.linalg.inv(scaleMatrix)
scale_image(image, output_image, inverse_matrix)
cv2.imwrite('scaled_img.png', output_image)
print(scaleMatrix)
print(inverse_matrix)
print(inverse_matrix @ scaleMatrix)