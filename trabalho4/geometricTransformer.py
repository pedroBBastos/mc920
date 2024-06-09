import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse

def nearest_neighbor_interpolation(image, resized_image):
    inputRows, inputColumns = image.shape[:2]
    outputRows, outptColumns = resized_image.shape[:2]

    rowsScaleFactor = outputRows / inputRows
    columnsScaleFactor = outptColumns / inputColumns

    for row in range(outputRows):
        for column in range(outptColumns):
            mappedInputRow = round(row / rowsScaleFactor)
            mappedInputColumn = round(column / columnsScaleFactor)
            resized_image[row, column] = image[mappedInputRow, mappedInputColumn]

def bilinear_interpolation(image, resized_image):
    inputRows, inputColumns = image.shape[:2]
    outputRows, outptColumns = resized_image.shape[:2]

    rowsScaleFactor = outputRows / inputRows
    columnsScaleFactor = outptColumns / inputColumns

    for row in range(outputRows):
        for column in range(outptColumns):
            y = round(row / rowsScaleFactor)
            x = round(column / columnsScaleFactor)

            dy = abs((row / rowsScaleFactor) - y)
            dx = abs((column / columnsScaleFactor) - x)

            try:
                upperLeftNeighborWeighedValue = abs((1-dx))*abs((1-dy))*image[y,x]
                upperRightNeighborWeighedValue = dx*abs((1-dy))*image[y,x+1]
                lowerLeftNeighborWeighedValue = abs((1-dx))*dy*image[y+1, x]
                lowerRightNeighborWeighedValue = dx*dy*image[y+1, x+1]

                resized_image[row, column] = upperLeftNeighborWeighedValue + \
                                            upperRightNeighborWeighedValue + \
                                            lowerLeftNeighborWeighedValue + \
                                            lowerRightNeighborWeighedValue
                if resized_image[row, column] <= 0 or resized_image[row, column] >= 255:
                    print("---------------------------------")
                    print("On try body -> ", resized_image[row, column])
                    print("upperLeftNeighborWeighedValue -> ", upperLeftNeighborWeighedValue)
                    print("upperRightNeighborWeighedValue -> ", upperRightNeighborWeighedValue)
                    print("lowerLeftNeighborWeighedValue -> ", lowerLeftNeighborWeighedValue)
                    print("lowerRightNeighborWeighedValue -> ", lowerRightNeighborWeighedValue)
                    print("---------------------------------")
            except IndexError as e:
                # print("IndexError")
                resized_image[row, column] = image[y%512, x%512]
                # TODO: verificar se fazer o mod, como o acima, é a melhor forma 
                # de contornar o BO de IndexError quando a img de saida é maior que a de entrada...
                # resized_image[row, column] = image[y, x]
                if resized_image[row, column] <= 0 or resized_image[row, column] >= 255:
                    print("---------------------------------")
                    print("On IndexError -> ", resized_image[row, column])
                    print("---------------------------------")

def P(t):
    return t if t > 0 else 0

def R(s):
    return (1/6)*(P(s+2)**3 - 4*P(s+1)**3 + 6*P(s)**3 - 4*P(s-1)**3)

def bicubic_interpolation(image, resized_image):
    inputRows, inputColumns = image.shape[:2]
    outputRows, outptColumns = resized_image.shape[:2]

    rowsScaleFactor = outputRows / inputRows
    columnsScaleFactor = outptColumns / inputColumns

    for row in range(outputRows):
        for column in range(outptColumns):
            y = round(row / rowsScaleFactor)
            x = round(column / columnsScaleFactor)

            dy = abs((row / rowsScaleFactor) - y)
            dx = abs((column / columnsScaleFactor) - x)

            sum = 0
            for m in [-1, 0, 1, 2]:
                for n in [-1, 0, 1, 2]:
                    sum += image[(y+n)%512,(x+m)%512]*R(m-dx)*R(dy-n)
            resized_image[row, column] = sum

def L(n, x, y, dx, image):
    return (-dx*(dx-1)*(dx-2)*image[(y+n-2)%512,(x-1)%512])/6 + \
           ((dx+1)*(dx-1)*(dx-2)*image[(y+n-2)%512, x%512])/2 + \
           (-dx*(dx+1)*(dx-2)*image[(y+n-2)%512, (x+1)%512])/2 + \
           (dx*(dx+1)*(dx-1)*image[(y+n-2)%512, (x+2)%512])/6

def lagrange_interpolation(image, resized_image):
    inputRows, inputColumns = image.shape[:2]
    outputRows, outptColumns = resized_image.shape[:2]

    rowsScaleFactor = outputRows / inputRows
    columnsScaleFactor = outptColumns / inputColumns

    for row in range(outputRows):
        for column in range(outptColumns):
            y = round(row / rowsScaleFactor)
            x = round(column / columnsScaleFactor)

            dy = abs((row / rowsScaleFactor) - y)
            dx = abs((column / columnsScaleFactor) - x)

            resized_image[row, column] = -dy*(dy-1)*(dy-2)*L(1, x, y, dx, image)/6 + \
                                         (dy+1)*(dy-1)*(dy-2)*L(2, x, y, dx, image)/2 + \
                                         -dy*(dy+1)*(dy-2)*L(3, x, y, dx, image)/2 + \
                                         dy*(dy+1)*(dy-1)*L(4, x, y, dx, image)/6

def scale_image(outputImg, scaleFactor):
    outputRows, outptColumns = outputImg.shape[:2]
    scaleMatrix = np.array([
                        [scaleFactor, 0, 0],
                        [0, scaleFactor, 0],
                        [0, 0, 1]
                    ], dtype=np.uint8)
    for row in range(outputRows):
        for column in range(outptColumns):
            mappedInputRow = round(row / scaleFactor)
            mappedInputColumn = round(column / scaleFactor)
            outputImg[row, column] = outputImg[mappedInputRow, mappedInputColumn]
    return


parser = argparse.ArgumentParser()
parser.add_argument('-a', action='store', dest='angle', help='Rotation angle')
parser.add_argument('-e', action='store', dest='scale_factor', help='Scale factor')
parser.add_argument('-he', action='store', type=int, dest='height', help='Output image height')
parser.add_argument('-w', action='store', type=int, dest='width', help='Output image width')
parser.add_argument('-m', action='store', type=str, dest='interpolation', help='Interpolation method to be used')
parser.add_argument('-i', action='store', dest='input_image', help='Input image file path')
parser.add_argument('-o', action='store', dest='output_image', help='Output image file path')

args = parser.parse_args()

image = cv2.imread(args.input_image, cv2.IMREAD_GRAYSCALE)
print(image.shape)

output_image = np.zeros((args.height, args.width), dtype=np.uint8)
if args.interpolation == 'NEAREST':
    nearest_neighbor_interpolation(image, output_image)
    cv2.imwrite('resized_image-nearest.png', output_image)
elif args.interpolation == 'BILINEAR':
    bilinear_interpolation(image, output_image)
    cv2.imwrite('resized_image-bilinear.png', output_image)
elif args.interpolation == 'BICUBIC':
    bicubic_interpolation(image, output_image)
    cv2.imwrite('resized_image-bicubic.png', output_image)
elif args.interpolation == 'LAGRANGE':
    lagrange_interpolation(image, output_image)
    cv2.imwrite('resized_image-lagrange.png', output_image)
else:
    print("No interpolation method provided... Aborting..")