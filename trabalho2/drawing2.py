import cv2
import numpy as np

# Create a black image
image = 255*np.ones((300, 300), dtype=np.uint8)

# Circle parameters
center = (150, 150)  # Center of the circles (x, y)
outer_radius = 100  # Radius of the outer circle
inner_radius = 50   # Radius of the inner circle

# Draw the outer circle
cv2.circle(image, center, outer_radius, (0), -1)  # Outer circle (white)

# Draw the inner circle
cv2.circle(image, center, inner_radius, (255), -1)   # Inner circle (black)

# Display the image
cv2.imshow('Two Circles', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
