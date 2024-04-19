import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read the input image
image = cv2.imread('/home/pedrobastos/repositories/mc920/images/baboon.png', cv2.IMREAD_GRAYSCALE)

# Compute the Fourier Transform
dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)

# Shift the zero frequency component to the center
dft_shift = np.fft.fftshift(dft)

# Compute the magnitude spectrum
magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

# Create a filter (e.g., high-pass filter)
rows, cols = image.shape
crow, ccol = rows // 2, cols // 2
mask = np.ones((rows, cols, 2), np.uint8)
mask[crow - 30:crow + 30, ccol - 30:ccol + 30] = 0

# Apply the filter to the magnitude spectrum
# filtered_spectrum = dft_shift * mask
filtered_spectrum = dft_shift * mask

# Inverse transform the filtered spectrum
inverse_fft_shift = np.fft.ifftshift(filtered_spectrum)
filtered_image = cv2.idft(inverse_fft_shift)

# Take the real part of the filtered image and convert it to uint8
filtered_image_real = cv2.normalize(filtered_image[:, :, 0], None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# Display the original and the filtered image
plt.subplot(121), plt.imshow(image, cmap='gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(filtered_image_real, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()