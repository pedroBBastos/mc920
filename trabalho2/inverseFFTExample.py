import cv2
import numpy as np

# Read the image
image = cv2.imread('/home/pedrobastos/repositories/mc920/images/baboon.png', cv2.IMREAD_GRAYSCALE)

# Apply FFT
dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)

# Shift the zero frequency component to the center
dft_shift = np.fft.fftshift(dft)

# Compute the inverse FFT
inverse_fft_shift = np.fft.ifftshift(dft_shift)
inverse_fft = cv2.idft(inverse_fft_shift)
print("inverse_fft.shape -> ", inverse_fft.shape)

# Compute the magnitude spectrum (for visualization)
# magnitude_spectrum = cv2.magnitude(inverse_fft[:, :, 0], inverse_fft[:, :, 1])

# Convert the inverse FFT result to uint8 and take the real part
reconstructed_image = cv2.normalize(cv2.magnitude(inverse_fft[:, :, 0], inverse_fft[:, :, 1]), None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# Display the original and reconstructed images
cv2.imshow('Original Image', image)
cv2.imshow('Reconstructed Image', reconstructed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
