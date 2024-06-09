import numpy as np

def scale_image(scaleFactor, inputImg):
    outputImage = np.zeros((int(inputImg.shape[0]*scaleFactor), 
                            int(inputImg.shape[1]*scaleFactor)), dtype=np.uint8)
    scaleMatrix = np.array([
                        [scaleFactor, 0, 0],
                        [0, scaleFactor, 0],
                        [0, 0, 1]
                    ])
    inverseScaleMatrix = np.linalg.inv(scaleMatrix)

    outputRows, outptColumns = outputImage.shape[:2]
    for row in range(outputRows):
        for column in range(outptColumns):
            currentOutputPixel = np.array([
                                          [column],
                                          [row],
                                          [1]
                                        ])
            inputImgPixel = inverseScaleMatrix @ currentOutputPixel
            outputImage[row, column] = inputImg[int(inputImgPixel[1,0])%outputRows, int(inputImgPixel[0,0])%outptColumns]
    
    return outputImage