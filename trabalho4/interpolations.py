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
                # if resized_image[row, column] <= 0 or resized_image[row, column] >= 255:
                #     # print("---------------------------------")
                #     # print("On try body -> ", resized_image[row, column])
                #     # print("upperLeftNeighborWeighedValue -> ", upperLeftNeighborWeighedValue)
                #     # print("upperRightNeighborWeighedValue -> ", upperRightNeighborWeighedValue)
                #     # print("lowerLeftNeighborWeighedValue -> ", lowerLeftNeighborWeighedValue)
                #     # print("lowerRightNeighborWeighedValue -> ", lowerRightNeighborWeighedValue)
                #     # print("---------------------------------")
            except IndexError as e:
                # print("IndexError")
                resized_image[row, column] = image[y%inputRows, x%inputColumns]
                # TODO: verificar se fazer o mod, como o acima, é a melhor forma 
                # de contornar o BO de IndexError quando a img de saida é maior que a de entrada...
                # resized_image[row, column] = image[y, x]
                # if resized_image[row, column] <= 0 or resized_image[row, column] >= 255:
                #     print("---------------------------------")
                #     print("On IndexError -> ", resized_image[row, column])
                #     print("---------------------------------")

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
                    sum += image[(y+n)%inputRows,(x+m)%inputColumns]*R(m-dx)*R(dy-n)
            resized_image[row, column] = sum

def L(n, x, y, dx, image, inputRows, inputColumns):
    return (-dx*(dx-1)*(dx-2)*image[(y+n-2)%inputRows,(x-1)%inputColumns])/6 + \
           ((dx+1)*(dx-1)*(dx-2)*image[(y+n-2)%inputRows, x%inputColumns])/2 + \
           (-dx*(dx+1)*(dx-2)*image[(y+n-2)%inputRows, (x+1)%inputColumns])/2 + \
           (dx*(dx+1)*(dx-1)*image[(y+n-2)%inputRows, (x+2)%inputColumns])/6

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

            resized_image[row, column] = -dy*(dy-1)*(dy-2)*L(1, x, y, dx, image, inputRows, inputColumns)/6 + \
                                         (dy+1)*(dy-1)*(dy-2)*L(2, x, y, dx, image, inputRows, inputColumns)/2 + \
                                         -dy*(dy+1)*(dy-2)*L(3, x, y, dx, image, inputRows, inputColumns)/2 + \
                                         dy*(dy+1)*(dy-1)*L(4, x, y, dx, image, inputRows, inputColumns)/6