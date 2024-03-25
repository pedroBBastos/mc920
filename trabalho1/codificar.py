import numpy as np
import cv2 as cv
import argparse
import sys
import utils
import json

# header size in 1 byte
# header
# content


def createHeader(size):
    """
    The header will have the output file extension and the file bytes size...
    The header will be a serialized python dictionary
    """
    headerDict = {"extension": ".png", "content-size": size}
    json_string = json.dumps(headerDict)
    serialized_bytes = bytes(json_string, 'utf-8')
    return np.frombuffer(serialized_bytes, dtype=np.uint8)

def writeHeaderIntoHostFile(transposedImageMatrix, header):
    # print("header -> ", header)
    headerSize = header.size

    # Producing the 3 block bits from the header size byte
    parsedHeaderSizeBits = utils.extractBitsFromByte(headerSize)
    firstPixel = transposedImageMatrix[:, 0, 0]

    # writing bits of header size byte on the first pixels
    firstPixel[0] = utils.move3LastBits(firstPixel[0], parsedHeaderSizeBits[0])
    firstPixel[1] = utils.move3LastBits(firstPixel[1], parsedHeaderSizeBits[1])
    firstPixel[2] = utils.move2LastBits(firstPixel[2], parsedHeaderSizeBits[2])
    transposedImageMatrix[:, 0, 0] = firstPixel




    # Producing matrix of extracted bits from all header bytes
    bitsFromHeaderBytes = np.vstack(utils.vectorizedExtractBitsFromByte(header))
    bitsFromHeaderBytes = np.transpose(bitsFromHeaderBytes, (1,0))
    
    # Getting all pixels needed to write the header but the first (which contains the header size hidden)
    contentMatrix = transposedImageMatrix[:, 0, 1:headerSize+1]
    final = utils.vectorizedMove3LastBits(contentMatrix[0], bitsFromHeaderBytes[0])
    final = np.vstack((final, utils.vectorizedMove3LastBits(contentMatrix[1], bitsFromHeaderBytes[1])))
    final = np.vstack((final, utils.vectorizedMove2LastBits(contentMatrix[2], bitsFromHeaderBytes[2])))

    transposedImageMatrix[:, 0, 1:headerSize+1] = final
    return


parser = argparse.ArgumentParser()
parser.add_argument('--imgHostFile', type=str, help='Image to be used as the host of the hidden content')
parser.add_argument('--inputFile', type=str, help='File to be hidden in the image passed on --imgHostFile')
parser.add_argument('--outputFileName', type=str, help='Name of the resulting image. Include extension')

args = parser.parse_args()
if len(sys.argv[1:]) < 3:
    print(args._get_args())
    parser.print_help()
    exit()

inputFileBytes = np.fromfile(args.inputFile, dtype=np.uint8)
# print("inputFileBytes.shape -> ", inputFileBytes.shape)
# print("inputFileBytes.size -> ", inputFileBytes.size)

img = cv.imread(args.imgHostFile)
img = np.transpose(img, (2,1,0))

headerDict = createHeader(inputFileBytes.size)
writeHeaderIntoHostFile(img, headerDict)

img = np.transpose(img, (2,1,0))
cv.imwrite(args.outputFileName, img)