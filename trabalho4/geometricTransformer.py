import cv2
import numpy as np
import argparse
import interpolation_by_point
import scaling
import rotation
import resize
import utils

parser = argparse.ArgumentParser()
parser.add_argument('-r', action='store', type=float, dest='rotation_factor', help='Rotation angle')
parser.add_argument('-e', action='store', type=float, dest='scale_factor', help='Scale factor')
parser.add_argument('-he', action='store', type=int, dest='height', help='Output image height')
parser.add_argument('-w', action='store', type=int, dest='width', help='Output image width')
parser.add_argument('-m', action='store', type=str, dest='interpolation', help='Interpolation method to be used')
parser.add_argument('-i', action='store', dest='input_image', help='Input image file path')
parser.add_argument('-o', action='store', type=str, dest='output_image', help='Output image file path')

args = parser.parse_args()

if not args.input_image:
    print("No input name provided... Aborting..")
    exit()

image = cv2.imread(args.input_image, cv2.IMREAD_GRAYSCALE)

interpolation = None
outputName = None
if args.output_image:
    outputName = args.output_image
else:
    print("No output name provided... Aborting..")
    exit()

if args.interpolation == 'NEAREST':
    interpolation = interpolation_by_point.NearestNeighborInterpolation()
elif args.interpolation == 'BILINEAR':
    interpolation = interpolation_by_point.BilinearInterpolation()
elif args.interpolation == 'BICUBIC':
    interpolation = interpolation_by_point.BicubicInterpolation()
elif args.interpolation == 'LAGRANGE':
    interpolation = interpolation_by_point.LagrangeInterpolation()
else:
    print("No interpolation method provided... Aborting..")
    exit()

transformedImg = None

if args.scale_factor:
    print("Realizando escala por fator ", args.scale_factor, ". Pode levar alguns segundos....")
    transformedImg = scaling.scale_image(args.scale_factor, image, interpolation)
elif args.rotation_factor:
    print("Realizando rotação em ", args.rotation_factor, " graus em sentido anti-horário. Pode levar alguns segundos....")
    pad_width, pad_height = utils.calculate_padding(image.shape[1], image.shape[0], args.rotation_factor)
    padded_image = utils.pad_image(image, pad_width, pad_height)
    transformedImg = rotation.rotate_image(args.rotation_factor, padded_image, interpolation)

output_image = np.zeros((args.height, args.width), dtype=np.uint8)
resize.resize(transformedImg, output_image, interpolation)
cv2.imwrite(outputName, output_image)

print("Transformações realizadas!")