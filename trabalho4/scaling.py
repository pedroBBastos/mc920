import numpy as np
import interpolation_by_point as interpolation

def scale_image(scaleFactor, inputImg, interpolation: interpolation.Interpolation):
    outputImage = np.zeros((int(inputImg.shape[0]*scaleFactor), 
                            int(inputImg.shape[1]*scaleFactor)), dtype=np.uint8)
    # Sx 0 0
    # 0 Sy 0
    # 0 0  1
    scaleMatrix = np.array([
                        [scaleFactor, 0, 0],
                        [0, scaleFactor, 0],
                        [0, 0, 1]
                    ])
    inverseScaleMatrix = np.linalg.inv(scaleMatrix)
    print("inverseScaleMatrix -> ", inverseScaleMatrix)

    outputRows, outptColumns = outputImage.shape[:2]
    for row in range(outputRows):
        for column in range(outptColumns):
            # Px
            # Py
            # 1
            currentOutputPixel = np.array([
                                          [column],
                                          [row],
                                          [1]
                                        ])
            # | Sx 0 0 |-1  *  | Px | 
            # | 0 Sy 0 |       | Py |
            # | 0 0  1 |       |  1 |
            inputImgPixel = inverseScaleMatrix @ currentOutputPixel
            # print("inputImgPixel[1,0] -> ", inputImgPixel[1,0])
            # print("inputImgPixel[0,0] -> ", inputImgPixel[0,0])
            # outputImage[row, column] = inputImg[int(inputImgPixel[1,0])%outputRows, int(inputImgPixel[0,0])%outptColumns]
            outputImage[row, column] = interpolation.interpolate(inputImgPixel[1,0], inputImgPixel[0,0], inputImg)
    
    return outputImage