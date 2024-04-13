import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read the image
image = cv2.imread('/home/pedrobastos/repositories/mc920/images/baboon.png', cv2.IMREAD_GRAYSCALE)

# Convert the image to float32
image_float32 = np.float32(image)

# Apply FFT
dft = cv2.dft(image_float32, flags=cv2.DFT_COMPLEX_OUTPUT)

# Shift the zero frequency component to the center
dft_shift = np.fft.fftshift(dft)

# Compute the magnitude spectrum (logarithmic scale)
magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

# Display the original and magnitude spectrum
# plt.subplot(121), plt.imshow(image, cmap='gray')
# plt.title('Input Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray')
# plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
# plt.show()

print(image.shape)
print(magnitude_spectrum)

mask = np.ones((image.shape[0], image.shape[1], 1), dtype=np.uint8)
# Circle parameters
center = (int(image.shape[0]//2), int(image.shape[1]//2))  # Center of the circle (x, y)
radius = 30  # Radius of the circle
color = 0 # 255  # Color of the circle (in BGR format)
thickness = -1  # Thickness of the circle (-1 fills the circle)
cv2.circle(mask, center, radius, color, thickness)

# rows, cols = image.shape
# crow, ccol = rows // 2, cols // 2
# mask = np.zeros((rows, cols, 2), np.uint8)
# mask[crow - 30:crow + 30, ccol - 30:ccol + 30] = 1





# result = np.multiply(dft_shift, mask)
# result = dft_shift * mask[:, :, np.newaxis]
print("dft_shift.shape -> ", dft_shift.shape)
result = dft_shift * mask
print(result)

# Display the original and magnitude spectrum
# plt.subplot(121), plt.imshow(image, cmap='gray')
# plt.title('Input Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122), plt.imshow(result, cmap='gray')
# plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
# plt.show()

inverse_fft_shift = np.fft.ifftshift(result)
filtered_image = cv2.idft(inverse_fft_shift)
print("filtered_image.shape -> ", filtered_image.shape)

# Compute the magnitude spectrum of the filtered image
# filtered_magnitude_spectrum = cv2.magnitude(filtered_image[:, :, 0], filtered_image[:, :, 1])

# filtered_image_real = cv2.normalize(cv2.magnitude(filtered_image[:, :, 0], filtered_image[:, :, 1]), None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
filtered_image_real = cv2.normalize(filtered_image[:, :, 0], None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# Display the original and the filtered image
plt.subplot(121), plt.imshow(image, cmap='gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(filtered_image_real, cmap='gray')
plt.title('Filtered image'), plt.xticks([]), plt.yticks([])
plt.show()