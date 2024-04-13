import cv2
import numpy as np

# Image dimensions
width = 400
height = 300

# Create a black image
image = np.zeros((height, width), dtype=np.uint8)

# Circle parameters
center = (200, 150)  # Center of the circle (x, y)
radius = 50  # Radius of the circle
color = 255  # Color of the circle (in BGR format)
thickness = -1  # Thickness of the circle (-1 fills the circle)

# Draw the circle on the image
cv2.circle(image, center, radius, color, thickness)

# Display the image
cv2.imshow('Black Circle', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
