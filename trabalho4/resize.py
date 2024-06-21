import interpolation_by_point as interpolation

def resize(image, resized_image, interpolation: interpolation.Interpolation):
    inputRows, inputColumns = image.shape[:2]
    outputRows, outptColumns = resized_image.shape[:2]

    rowsScaleFactor = outputRows / inputRows
    columnsScaleFactor = outptColumns / inputColumns

    for row in range(outputRows):
        for column in range(outptColumns):
            resized_image[row, column] = interpolation.interpolate(row / rowsScaleFactor, column / columnsScaleFactor, image)