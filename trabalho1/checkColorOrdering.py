import cv2

# Read the image
image = cv2.imread('../images/baboon.png')

# Convert the image from BGR to RGB
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Compare the first pixel values
bgr_pixel = image[0, 0]
rgb_pixel = rgb_image[0, 0]

# Print the first pixel values
print("BGR Pixel:", bgr_pixel)
print("RGB Pixel:", rgb_pixel)

# Display the images
cv2.imshow('BGR Image', image)
cv2.imshow('RGB Image', rgb_image)
cv2.waitKey(0)
cv2.destroyAllWindows()