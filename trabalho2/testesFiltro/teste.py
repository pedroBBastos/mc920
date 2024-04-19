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
plt.subplot(121), plt.imshow(image, cmap='gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()










# mask = np.zeros((image.shape[0], image.shape[1], 1), dtype=np.uint8)
mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
# Circle parameters
center = (int(image.shape[0]//2), int(image.shape[1]//2))  # Center of the circle (x, y)
radius = 30  # Radius of the circle
color = 255 # 255  # Color of the circle (in BGR format)
thickness = -1  # Thickness of the circle (-1 fills the circle)
cv2.circle(mask, center, radius, color, thickness)

result = np.multiply(magnitude_spectrum, mask)
# result = dft_shift * mask[:, :, np.newaxis]
print("dft_shift.shape -> ", dft_shift.shape)
# result = dft_shift * mask
print(result)

# Display the original and magnitude spectrum
plt.subplot(121), plt.imshow(image, cmap='gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(result, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()