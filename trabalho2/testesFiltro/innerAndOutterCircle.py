import cv2
import numpy as np

# Create a black image
image = np.zeros((300, 300), dtype=np.uint8)

# Circle parameters
center = (150, 150)  # Center of the circles (x, y)
outer_radius = 100  # Radius of the outer circle
inner_radius = 50   # Radius of the inner circle

# Create masks for the circles
outer_circle_mask = np.zeros_like(image)
inner_circle_mask = np.zeros_like(image)

# Draw the outer and inner circles on their respective masks
cv2.circle(outer_circle_mask, center, outer_radius, (255), -1)  # Outer circle (white)
cv2.circle(inner_circle_mask, center, inner_radius, (255), -1)  # Inner circle (white)

# Subtract the inner circle mask from the outer circle mask to get the area between the circles
area_between_circles = cv2.subtract(outer_circle_mask, inner_circle_mask)

# Paint the area between the circles in black
image = cv2.bitwise_and(image, image, mask=area_between_circles)

# Display the image
cv2.imshow('Area Between Circles', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
