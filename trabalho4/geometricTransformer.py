import cv2
import numpy as np
import argparse
import interpolations
import scaling
import rotation

parser = argparse.ArgumentParser()
parser.add_argument('-r', action='store', type=float, dest='rotation_factor', help='Rotation angle')
parser.add_argument('-e', action='store', type=float, dest='scale_factor', help='Scale factor')
parser.add_argument('-he', action='store', type=int, dest='height', help='Output image height')
parser.add_argument('-w', action='store', type=int, dest='width', help='Output image width')
parser.add_argument('-m', action='store', type=str, dest='interpolation', help='Interpolation method to be used')
parser.add_argument('-i', action='store', dest='input_image', help='Input image file path')
parser.add_argument('-o', action='store', type=str, dest='output_image', help='Output image file path')

args = parser.parse_args()

image = cv2.imread(args.input_image, cv2.IMREAD_GRAYSCALE)
print(image.shape)

transformedImg = None

if args.scale_factor:
    transformedImg = scaling.scale_image(args.scale_factor, image)
elif args.rotation_factor:
    transformedImg = rotation.rotate_image(args.rotation_factor, image)

output_image = np.zeros((args.height, args.width), dtype=np.uint8)
if args.interpolation == 'NEAREST':
    interpolations.nearest_neighbor_interpolation(transformedImg, output_image)
    cv2.imwrite('resized_image-nearest.png', output_image)
elif args.interpolation == 'BILINEAR':
    interpolations.bilinear_interpolation(transformedImg, output_image)
    cv2.imwrite('resized_image-bilinear.png', output_image)
elif args.interpolation == 'BICUBIC':
    interpolations.bicubic_interpolation(transformedImg, output_image)
    cv2.imwrite('resized_image-bicubic.png', output_image)
elif args.interpolation == 'LAGRANGE':
    interpolations.lagrange_interpolation(transformedImg, output_image)
    cv2.imwrite('resized_image-lagrange.png', output_image)
else:
    print("No interpolation method provided... Aborting..")