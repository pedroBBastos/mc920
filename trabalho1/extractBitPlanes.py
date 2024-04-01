import numpy as np
import cv2 as cv
import argparse
import json
import sys
import utils

parser = argparse.ArgumentParser()
parser.add_argument('--imgFile', type=str, help='Image to extract bit planes')

args = parser.parse_args()
if len(sys.argv[1:]) < 1:
    print(args._get_args())
    parser.print_help()
    exit()

imgFileToDecode = cv.imread(args.imgFile)
imgFileToDecode = np.transpose(imgFileToDecode, (2,1,0))

for i in range(0, 3):
    bit0Plane = utils.vectorizedGetBit0Number(imgFileToDecode[i]).astype(np.uint8)
    bit1Plane = utils.vectorizedGetBit1Number(imgFileToDecode[i]).astype(np.uint8)
    bit2Plane = utils.vectorizedGetBit2Number(imgFileToDecode[i]).astype(np.uint8)
    bit7Plane = utils.vectorizedGetBit7Number(imgFileToDecode[i]).astype(np.uint8)

    # Create named windows for each image
    cv.namedWindow('Bit 0 Plane', cv.WINDOW_NORMAL)
    cv.namedWindow('Bit 1 Plane', cv.WINDOW_NORMAL)
    cv.namedWindow('Bit 2 Plane', cv.WINDOW_NORMAL)
    cv.namedWindow('Bit 7 Plane', cv.WINDOW_NORMAL)

    # Show each image in its respective window
    cv.imshow('Bit 0 Plane', bit0Plane.T)
    cv.imshow('Bit 1 Plane', bit1Plane.T)
    cv.imshow('Bit 2 Plane', bit2Plane.T)
    cv.imshow('Bit 7 Plane', bit7Plane.T)

    cv.waitKey(0)
    cv.destroyAllWindows()