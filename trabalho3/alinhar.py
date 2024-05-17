import argparse
import sys
import projecaoHorizontal
import transformadaHough
import utils
import matplotlib.pyplot as plt
import cv2

parser = argparse.ArgumentParser()
parser.add_argument('--inputImg', type=str, help='Image to be text aligned')
parser.add_argument('--outputImg', type=str, help='Aligned image to be saved')
parser.add_argument('--mode', type=str, help='Alignment mode to be used: PROJECTION or HOUGH')
parser.add_argument('--houghThreshold', type=str, help='Threshold to be used on HOUGH transform. If not provided, the execution will use the default value of 400')

args = parser.parse_args()
if len(sys.argv[1:]) < 6:
    print(args._get_args())
    parser.print_help()
    exit()

image = cv2.imread(args.inputImg, cv2.IMREAD_GRAYSCALE)
finalAngle = None

if args.mode == 'PROJECTION':
    finalAngle = projecaoHorizontal.alinhar(image)
elif args.mode == 'HOUGH':
    if args.houghThreshold is not None:
        finalAngle = transformadaHough.alinhar(image, int(args.houghThreshold))
    else:
        finalAngle = transformadaHough.alinhar(image)
    if finalAngle is None:
        exit()
else:
    print("Unknown mode '", args.mode, "'. Aborting...")

rotatedImg = utils.rotate_image(image, finalAngle)
plt.imshow(rotatedImg, cmap='gray')
plt.axis('off')
plt.show()
cv2.imwrite(args.outputImg, rotatedImg)