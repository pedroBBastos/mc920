import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys
import os

def getFiltroPassaBaixa(shape):
    mask = np.zeros((shape[0], shape[1], 1), dtype=np.uint8)
    # Circle parameters
    center = (int(shape[0]//2), int(shape[1]//2))  # Center of the circle (x, y)
    radius = 30  # Radius of the circle
    color = 255  # Color of the circle (in BGR format)
    thickness = -1  # Thickness of the circle (-1 fills the circle)
    cv2.circle(mask, center, radius, color, thickness)
    return mask

def getFiltroPassaAlta(shape):
    mask = np.ones((shape[0], shape[1], 1), dtype=np.uint8)
    # Circle parameters
    center = (int(shape[0]//2), int(shape[1]//2))  # Center of the circle (x, y)
    radius = 30  # Radius of the circle
    color = 0 # 255  # Color of the circle (in BGR format)
    thickness = -1  # Thickness of the circle (-1 fills the circle)
    cv2.circle(mask, center, radius, color, thickness)
    return mask

def getFiltroPassaFaixa(shape):
    mask = np.zeros((shape[0], shape[1], 1), dtype=np.uint8)

    # Outter Circle parameters
    out_center = (int(shape[0]//2), int(shape[1]//2))  # Center of the circle (x, y)
    out_radius = 30  # Radius of the circle
    out_color = 255  # Color of the circle (in BGR format)
    out_thickness = -1  # Thickness of the circle (-1 fills the circle)
    cv2.circle(mask, out_center, out_radius, out_color, out_thickness)

    # Inner Circle parameters
    inner_center = (int(shape[0]//2), int(shape[1]//2))  # Center of the circle (x, y)
    inner_radius = 10  # Radius of the circle
    inner_color = 0  # Color of the circle (in BGR format)
    inner_thickness = -1  # Thickness of the circle (-1 fills the circle)
    cv2.circle(mask, inner_center, inner_radius, inner_color, inner_thickness)

    return mask

def getFiltroRejeitaFaixa(shape):
    mask = np.ones((shape[0], shape[1], 1), dtype=np.uint8)

    # Outter Circle parameters
    out_center = (int(shape[0]//2), int(shape[1]//2))  # Center of the circle (x, y)
    out_radius = 30  # Radius of the circle
    out_color = 0  # Color of the circle (in BGR format)
    out_thickness = -1  # Thickness of the circle (-1 fills the circle)
    cv2.circle(mask, out_center, out_radius, out_color, out_thickness)

    # Inner Circle parameters
    inner_center = (int(shape[0]//2), int(shape[1]//2))  # Center of the circle (x, y)
    inner_radius = 10  # Radius of the circle
    inner_color = 255  # Color of the circle (in BGR format)
    inner_thickness = -1  # Thickness of the circle (-1 fills the circle)
    cv2.circle(mask, inner_center, inner_radius, inner_color, inner_thickness)

    return mask


parser = argparse.ArgumentParser()
parser.add_argument('--inputImg', type=str, help='Image to apply all types of filters')

args = parser.parse_args()
if len(sys.argv[1:]) < 1:
    print(args._get_args())
    parser.print_help()
    exit()

if not os.path.exists(args.inputImg):
    print("File '", args.inputImg, "' does not exist... Aborting")
    exit()


# Getting FFT image from inputImg
image = cv2.imread(args.inputImg, cv2.IMREAD_GRAYSCALE)
dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)

filtersList = [getFiltroPassaBaixa(image.shape), getFiltroPassaAlta(image.shape), getFiltroPassaFaixa(image.shape), getFiltroRejeitaFaixa(image.shape)]
labelsArray = ['Filtro Passa Baixa', 'Filtro Passa Alta', 'Filtro Passa Faixa', 'Filtro Rejeita Faixa']

filteredImages = dft_shift * filtersList

results = []
for filteredImage in filteredImages:
    inverse_fft_shift = np.fft.ifftshift(filteredImage)
    inverse_fft_image = cv2.idft(inverse_fft_shift)
    filtered_image_real = cv2.normalize(inverse_fft_image[:, :, 0], None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    results.append(filtered_image_real)

# Display the original and the filtered images

for i in range(0, len(results)):
    plt.subplot(121), plt.imshow(image, cmap='gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(results[i], cmap='gray')
    plt.title(labelsArray[i]), plt.xticks([]), plt.yticks([])
    plt.show()

# Passa faixa = filtragem de bordas de uma certa espessura???