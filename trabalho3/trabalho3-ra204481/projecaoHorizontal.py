import cv2
import numpy as np
import matplotlib.pyplot as plt
import utils

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
        currentRotatedImage = utils.rotate_image(binary_image, currentRotation)
        valorFuncaoObjetivo = funcao_objetivo(currentRotatedImage)
        if valorFuncaoObjetivo > melhorValorFuncObj:
            melhorValorFuncObj = valorFuncaoObjetivo
            melhorRotacaoParaAlinhamento = currentRotation
            melhorImagemRotacionada = currentRotatedImage
        currentRotation += rotationPace
    return melhorRotacaoParaAlinhamento, melhorValorFuncObj, melhorImagemRotacionada

def alinhar(inputImg):
    # Apply thresholding
    _, binary_image = cv2.threshold(inputImg, 200, 1, cv2.THRESH_BINARY)

    plt.imshow(binary_image, cmap='gray')
    plt.axis('off')
    plt.show()

    melhorRotacaoClockwise, valorFObjCW, imgRotatedCW = verifica_projecao_horizontal(binary_image, 0, -90, -0.2)
    print("Melhor angulo para rotação clockwise (negative degress) -> ", melhorRotacaoClockwise)

    melhorRotacaoNonClockwise, valorFObjNCW, imgRotatedNCW = verifica_projecao_horizontal(binary_image, 0, 90, 0.2)
    print("Melhor angulo para rotação non-clockwise (positive degress) -> ", melhorRotacaoNonClockwise)

    if valorFObjCW > valorFObjNCW:
        print("Angulo final é ", melhorRotacaoClockwise)
        plt.imshow(imgRotatedCW, cmap='gray')
        plt.axis('off')
        plt.show()
        return melhorRotacaoClockwise
    else:
        print("Angulo final é ", melhorRotacaoNonClockwise)
        plt.imshow(imgRotatedNCW, cmap='gray')
        plt.axis('off')
        plt.show()
        return melhorRotacaoNonClockwise