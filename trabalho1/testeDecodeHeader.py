import pickle
import cv2 as cv
import numpy as np

img = cv.imread('output.png')
img = np.transpose(img, (2,1,0))
print(img.shape)

aux = img[:, :, :48]
print(aux.shape)

