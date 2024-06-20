import numpy as np
import math
import interpolation_by_point as interpolation

def rotate_image(rotationFactor, inputImg, interpolation: interpolation.Interpolation):
    rotationFactorRadians = np.radians(-rotationFactor)
    image_height, image_width = inputImg.shape[:2]

    output_image = np.zeros(inputImg.shape, dtype=np.uint8)
    print("output_image.shape -> ", output_image.shape)

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

    outputRows, outptColumns = output_image.shape[:2]
    for row in range(outputRows):
        for column in range(outptColumns):
            currentOutputPixel = np.array([
                                          [column],
                                          [row],
                                          [1]
                                        ])
            inputImgPixel = inverse_matrix @ currentOutputPixel

            inputImgRow = int(inputImgPixel[1,0])
            inputImgColumn = int(inputImgPixel[0,0])

            inputImgRow = inputImgRow if inputImgRow < image_height and inputImgRow >= 0 else -1
            inputImgColumn = inputImgColumn if inputImgColumn < image_width and inputImgColumn >= 0 else -1

            if inputImgRow == -1 or inputImgColumn == -1:
                output_image[row, column] = 0
            else:
                # output_image[row, column] = inputImg[inputImgRow, inputImgColumn]
                output_image[row, column] = interpolation.interpolate(inputImgRow, inputImgColumn, inputImg)

    return output_image