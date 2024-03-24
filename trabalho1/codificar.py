import numpy as np
import cv2 as cv
import argparse
import pickle
import sys

# constant definitions
maskToGet3LastBits = 7 # 0b111
maskToGet2LastBits = 3 # 0b011

maskToZero3LastBits = ~((1 << 3) - 1)
maskToZero2LastBits = ~((1 << 2) - 1)

# header size in 1 byte
# header
# content

def extractBitsFromByte(n):
    aux = n
    intoRed = aux & maskToGet3LastBits
    aux >>= 3
    intoGreen = aux & maskToGet3LastBits
    aux >>= 3
    intoBlue = aux
    return np.array([intoRed,intoGreen,intoBlue])

def move3LastBits(x, y):
  auxX = x & maskToZero3LastBits
  bitsToBePlaced = y & maskToGet3LastBits
  return auxX ^ bitsToBePlaced

def move2LastBits(x, y):
  auxX = x & maskToZero2LastBits
  bitsToBePlaced = y & maskToGet2LastBits
  return auxX ^ bitsToBePlaced

vectorizedExtractBitsFromByte = np.frompyfunc(extractBitsFromByte, 1, 1)
vectorizedMove3LastBits = np.frompyfunc(move3LastBits, 2, 1)
vectorizedMove2LastBits = np.frompyfunc(move2LastBits, 2, 1)


def createHeader(size):
    """
    The header will have the output file extension and the file bytes size...
    The header will be a serialized python dictionary
    """
    headerDict = {'extension': '.png', 'content-size': size}
    serialized_bytes = pickle.dumps(headerDict)
    return np.frombuffer(serialized_bytes, dtype=np.uint8)

def writeHeaderIntoHostFile(transposedImageMatrix, header):
    print("header size -> ", header.size)
    headerSize = header.size

    # Producing the 3 block bits from the header size byte
    parsedBitsFromByte = extractBitsFromByte(headerSize)
    # parsedBitsFromByte = np.reshape(parsedBitsFromByte, (3, 1))
    print("bits header size ", parsedBitsFromByte)

    # print(transposedImageMatrix)
    firstPixelColumn = transposedImageMatrix[:, 0, 0]
    print("bytes first pixel ", firstPixelColumn)

    # writing bits of header size on the first pixels
    firstPixelColumn[0] = move3LastBits(firstPixelColumn[0], parsedBitsFromByte[0])
    firstPixelColumn[1] = move3LastBits(firstPixelColumn[1], parsedBitsFromByte[1])
    firstPixelColumn[2] = move2LastBits(firstPixelColumn[2], parsedBitsFromByte[2])
    print("bytes first pixel changed ", firstPixelColumn)
    transposedImageMatrix[:, 0, 0] = firstPixelColumn
    print("bytes first pixel changed finalll", transposedImageMatrix[:, 0, 0])

    # Producing matrix of extracted bits from all header bytes
    bitsFromHeaderBytes = np.vstack(vectorizedExtractBitsFromByte(header))
    bitsFromHeaderBytes = np.transpose(bitsFromHeaderBytes, (1,0))
    print(bitsFromHeaderBytes)
    
    # Getting all pixels needed to write the header but the first (which contains the header size hidden)
    contentMatrix = transposedImageMatrix[:, :, 1:headerSize+1]
    print(contentMatrix.shape)
    final = vectorizedMove3LastBits(contentMatrix[0], bitsFromHeaderBytes[0])
    final = np.vstack((final, vectorizedMove3LastBits(contentMatrix[1], bitsFromHeaderBytes[1])))
    final = np.vstack((final, vectorizedMove2LastBits(contentMatrix[2], bitsFromHeaderBytes[2])))
    print(contentMatrix.shape)
    transposedImageMatrix[:, :, 1:headerSize+1] = contentMatrix

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
# print("size -> ", img.size)
# print("shape -> ", img.shape)

headerDict = createHeader(inputFileBytes.size)
writeHeaderIntoHostFile(img, headerDict)

img = np.transpose(img, (2,1,0))
cv.imwrite(args.outputFileName, img)