import cv2
import numpy as np
import argparse
import interpolation_by_point
import scaling
import rotation
import resize

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

interpolation = None
outputName = None

if args.interpolation == 'NEAREST':
    interpolation = interpolation_by_point.NearestNeighborInterpolation()
    outputName = 'nearest.png'
elif args.interpolation == 'BILINEAR':
    interpolation = interpolation_by_point.BilinearInterpolation()
    outputName = 'bilinear.png'
elif args.interpolation == 'BICUBIC':
    interpolation = interpolation_by_point.BicubicInterpolation()
    outputName = 'bicubic.png'
elif args.interpolation == 'LAGRANGE':
    interpolation = interpolation_by_point.LagrangeInterpolation()
    outputName = 'lagrange.png'
else:
    print("No interpolation method provided... Aborting..")
    exit()

transformedImg = None

if args.scale_factor:
    transformedImg = scaling.scale_image(args.scale_factor, image, interpolation)
    # cv2.imwrite(outputName, transformedImg)
elif args.rotation_factor:
    transformedImg = rotation.rotate_image(args.rotation_factor, image, interpolation)
    # cv2.imwrite(outputName, transformedImg)

output_image = np.zeros((args.height, args.width), dtype=np.uint8)
resize.resize(transformedImg, output_image, interpolation)
cv2.imwrite(outputName, output_image)