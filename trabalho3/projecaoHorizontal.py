import cv2
import numpy as np
import matplotlib.pyplot as plt

def rotate_image(image, angle):
    # Get image dimensions
    rows, cols = image.shape[:2]
    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    # Perform the rotation
    rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))
    return rotated_image

def funcao_objetivo(binaryImage):
    histograma = np.sum(binaryImage, axis=1)
    diff_squared = np.diff(histograma) ** 2
    sum_of_squares = np.sum(diff_squared)
    return sum_of_squares

def verifica_projecao_horizontal(binary_image, start_angle, end_angle, rotationPace):
    currentRotation = start_angle
    melhorValorFuncObj = float('-inf')
    melhorRotacaoParaAlinhamento = None
    melhorImagemRotacionada = None

    while abs(currentRotation) <= abs(end_angle):
        currentRotatedImage = rotate_image(binary_image, currentRotation)
        valorFuncaoObjetivo = funcao_objetivo(currentRotatedImage)
        if valorFuncaoObjetivo > melhorValorFuncObj:
            melhorValorFuncObj = valorFuncaoObjetivo
            melhorRotacaoParaAlinhamento = currentRotation
            melhorImagemRotacionada = currentRotatedImage
        currentRotation += rotationPace
    return melhorRotacaoParaAlinhamento, melhorValorFuncObj, melhorImagemRotacionada

def alinhar(inputImgPath):
    # Load the image in grayscale
    image_gray = cv2.imread(inputImgPath, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding
    _, binary_image = cv2.threshold(image_gray, 200, 1, cv2.THRESH_BINARY)

    plt.imshow(binary_image, cmap='gray')
    plt.axis('off')
    plt.show()

    melhorRotacaoClockwise, valorFObjCW, imgRotated = verifica_projecao_horizontal(binary_image, 0, -90, -0.2)
    print("Melhor angulo para rotação clockwise (negative degress) -> ", melhorRotacaoClockwise)

    plt.imshow(imgRotated, cmap='gray')
    plt.axis('off')
    plt.show()

    melhorRotacaoNonClockwise, valorFObjNCW, imgRotated = verifica_projecao_horizontal(binary_image, 0, 90, 0.2)
    print("Melhor angulo para rotação non-clockwise (positive degress) -> ", melhorRotacaoNonClockwise)

    plt.imshow(imgRotated, cmap='gray')
    plt.axis('off')
    plt.show()

    if valorFObjCW > valorFObjNCW:
        print("Angulo final é ", melhorRotacaoClockwise)
    else:
        print("Angulo final é ", melhorRotacaoNonClockwise)