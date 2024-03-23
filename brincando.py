import cv2 as cv
import numpy as np

img = cv.imread('images/baboon.png')
print("size -> ", img.size)
print("shape -> ", img.shape)
print("type -> ", type(img))

# fazendo a transposta para separar a imagem por banda de cor na primeira dimensao
img2 = np.transpose(img, (2,1,0))

print("size -> ", img2.size)
print("shape -> ", img2.shape)
print("type -> ", type(img2))

# print(img2[-1])
# print(img2[-1].shape)
print(img)
print(img2)

print(img2[-1].shape)
print(img2[-1].ravel()[-3*200:]) # pegando os ultimos 3 bytes da ultima banda de cor


# cv.imshow('asdads', img)
# cv.waitKey(0)