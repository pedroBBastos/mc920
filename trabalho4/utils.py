import cv2
import numpy as np

def calculate_padding(width, height, angle):
    # Convert angle to radians
    angle_rad = np.deg2rad(angle)

    # Calculate new width and height
    new_width = int(width * abs(np.cos(angle_rad)) + height * abs(np.sin(angle_rad)))
    new_height = int(width * abs(np.sin(angle_rad)) + height * abs(np.cos(angle_rad)))

    # Calculate the padding needed
    pad_width = (new_width - width) // 2
    pad_height = (new_height - height) // 2

    return pad_width, pad_height

def pad_image(image, pad_width, pad_height):
    # Pad the image with the calculated padding
    padded_image = cv2.copyMakeBorder(image, pad_height, pad_height, pad_width, pad_width, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    return padded_image