import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys
import os

#################################################
## Métodos para obtenção das máscaras para os filtros
#################################################

def getFiltroPassaBaixa(shape, radius):
    mask = np.zeros((shape[0], shape[1], 1), dtype=np.uint8)
    # Circle parameters
    center = (int(shape[0]//2), int(shape[1]//2))
    color = 255
    thickness = -1
    cv2.circle(mask, center, radius, color, thickness)
    return mask

def getFiltroPassaAlta(shape, radius):
    mask = 255*np.ones((shape[0], shape[1], 1), dtype=np.uint8)
    # Circle parameters
    center = (int(shape[0]//2), int(shape[1]//2))
    color = 0
    thickness = -1
    cv2.circle(mask, center, radius, color, thickness)
    return mask

def getFiltroPassaFaixa(shape, out_radius, inner_radius):
    mask = np.zeros((shape[0], shape[1], 1), dtype=np.uint8)

    # Outter Circle parameters
    out_center = (int(shape[0]//2), int(shape[1]//2))
    out_color = 255
    out_thickness = -1
    cv2.circle(mask, out_center, out_radius, out_color, out_thickness)

    # Inner Circle parameters
    inner_center = (int(shape[0]//2), int(shape[1]//2))
    inner_color = 0
    inner_thickness = -1
    cv2.circle(mask, inner_center, inner_radius, inner_color, inner_thickness)

    return mask

def getFiltroRejeitaFaixa(shape, out_radius, inner_radius):
    mask = 255*np.ones((shape[0], shape[1], 1), dtype=np.uint8)

    # Outter Circle parameters
    out_center = (int(shape[0]//2), int(shape[1]//2))
    out_color = 0
    out_thickness = -1
    cv2.circle(mask, out_center, out_radius, out_color, out_thickness)

    # # Inner Circle parameters
    inner_center = (int(shape[0]//2), int(shape[1]//2))
    inner_color = 255
    inner_thickness = -1
    cv2.circle(mask, inner_center, inner_radius, inner_color, inner_thickness)

    return mask

#################################################
## Parsing entrada
#################################################

parser = argparse.ArgumentParser()
parser.add_argument('--inputImg', type=str, help='Image to apply all types of filters')
parser.add_argument('--r1', type=str, help='Filtering outer circle radius')
parser.add_argument('--r2', type=str, help='Filtering inner circle radius')
parser.add_argument('--compressThreashold', type=str, help='Threashold to be considered when compresing image')

args = parser.parse_args()
if len(sys.argv[1:]) < 8:
    print(args._get_args())
    parser.print_help()
    exit()

if not os.path.exists(args.inputImg):
    print("File '", args.inputImg, "' does not exist... Aborting")
    exit()

if not args.r1.isdigit() or not args.r2.isdigit():
    print("Provided radius not a number... Aborting")
    exit()

r1 = int(args.r1)
r2 = int(args.r2)

if r1 <= r2:
    print("Inner radius ", r2, " is greater than ", r1, "... Aborting")
    exit()


#################################################
## Efetuando a FFT e a filtragem das imagens a partir das máscaras definidas
#################################################

image = cv2.imread(args.inputImg, cv2.IMREAD_GRAYSCALE)
dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)
magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

filtersList = [getFiltroPassaBaixa(image.shape, r1), getFiltroPassaAlta(image.shape, r1), getFiltroPassaFaixa(image.shape, r1, r2), getFiltroRejeitaFaixa(image.shape, r1, r2)]
labelsArray = ['Filtro Passa Baixa, r1 = ' + str(r1), 'Filtro Passa Alta, r1 = ' + str(r1), 'Filtro Passa Faixa, r1 = ' + str(r1) + ', r2 = ' + str(r2), 'Filtro Rejeita Faixa, r1 = ' + str(r1) + ', r2 = ' + str(r2)]

filteredImages = dft_shift * filtersList

magnitude_spectrum_filters = []
for f in filtersList:
    magnitude_spectrum_filters.append(np.multiply(magnitude_spectrum, f[:, :, 0]))


results = []
for i in range(0, len(filteredImages)):
    inverse_fft_shift = np.fft.ifftshift(filteredImages[i])
    inverse_fft_image = cv2.idft(inverse_fft_shift)
    filtered_image_real = cv2.normalize(inverse_fft_image[:, :, 0], None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    results.append((magnitude_spectrum_filters[i], filtered_image_real))

# Mostrando filtro realizado e imagem de resultado da aplicação do filtro
for i in range(0, len(results)):
    plt.figure(figsize=(11, 6))
    plt.subplot(121), plt.imshow(results[i][0], cmap='gray')
    plt.title(labelsArray[i]), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(results[i][1], cmap='gray')
    plt.title('Resultado ' + labelsArray[i]), plt.xticks([]), plt.yticks([])
    plt.show()

#################################################
## Compressão a partir da remoção dos coeficientes
#################################################

# mexendo em ambas magnitude e fase, o resultado fica mais parecido com a imagem
# de exemplo no enunciado do relatório...
compressThreashold = int(args.compressThreashold)
dft_shift[np.abs(dft_shift) < compressThreashold] = 0

inverse_fft_shift = np.fft.ifftshift(dft_shift)
inverse_fft_image = cv2.idft(inverse_fft_shift)
compressed_image_real = cv2.normalize(inverse_fft_image[:, :, 0], None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

plt.figure(figsize=(11, 6)) 
plt.subplot(121), plt.imshow(image, cmap='gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(compressed_image_real, cmap='gray')
plt.title('Compressed Image - Threashold ' + str(compressThreashold)), plt.xticks([]), plt.yticks([])
plt.show()

cv2.imwrite('compressed-threshold_'+ str(compressThreashold) +'.png', compressed_image_real)


#################################################
## Calculando histograma 
#################################################

# Calculate histogram
histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
# Plot histogram
plt.figure(figsize=(11, 6)) 
plt.plot(histogram, color='gray')
plt.xlabel('Intensidade')
plt.ylabel('Frequência')
plt.title('Histograma imagem original')
plt.xlim([0, 256])
plt.show()

histogram = cv2.calcHist([compressed_image_real], [0], None, [256], [0, 256])
plt.figure(figsize=(11, 6)) 
plt.plot(histogram, color='gray')
plt.xlabel('Intensidade')
plt.ylabel('Frequência')
plt.title('Histograma Imagem comprimida com limiar ' + str(compressThreashold))
plt.xlim([0, 256])
plt.show()