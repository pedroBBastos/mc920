import numpy as np
import cv2 as cv
import argparse
import sys
import utils
import json

# header size in 1 byte
# header
# content


def createHeader(size, fileNameWhenDecode):
    """
    The header will have the output file extension and the file bytes size...
    The header will be a serialized python dictionary
    """
    if fileNameWhenDecode == None:
        print("--fileNameWhenDecode must not be empty")
        exit()
    headerDict = {"content-size": size, "result-name": fileNameWhenDecode}
    json_string = json.dumps(headerDict)
    serialized_bytes = bytes(json_string, 'utf-8')
    return np.frombuffer(serialized_bytes, dtype=np.uint8)

def writeHeaderSizeIntoHostFile(transposedImageMatrix, header):
    headerSize = header.size
    print("headerSize -> ", headerSize)

    # Producing the 3 block bits from the header size byte
    parsedHeaderSizeBits = utils.extractBitsFromByte(headerSize)
    firstPixel = transposedImageMatrix[:, 0, 0]

    # writing bits of header size byte on the first pixels
    firstPixel[0] = utils.move3LastBits(firstPixel[0], parsedHeaderSizeBits[0])
    firstPixel[1] = utils.move3LastBits(firstPixel[1], parsedHeaderSizeBits[1])
    firstPixel[2] = utils.move2LastBits(firstPixel[2], parsedHeaderSizeBits[2])
    transposedImageMatrix[:, 0, 0] = firstPixel
    return headerSize

def writeHeaderIntoHostFile(transposedImageMatrix, header):
    # print("header -> ", header)
    headerSize = writeHeaderSizeIntoHostFile(transposedImageMatrix, header)

    # Producing matrix of extracted bits from all header bytes
    bitsFromHeaderBytes = np.vstack(utils.vectorizedExtractBitsFromByte(header))
    bitsFromHeaderBytes = np.transpose(bitsFromHeaderBytes, (1,0))
    
    # Getting all pixels needed to write the header but the first (which contains the header size hidden)
    contentMatrix = transposedImageMatrix[:, 0, 1:headerSize+1] # first row of image, starting from second pixel
    final = utils.vectorizedMove3LastBits(contentMatrix[0], bitsFromHeaderBytes[0])
    final = np.vstack((final, utils.vectorizedMove3LastBits(contentMatrix[1], bitsFromHeaderBytes[1])))
    final = np.vstack((final, utils.vectorizedMove2LastBits(contentMatrix[2], bitsFromHeaderBytes[2])))

    transposedImageMatrix[:, 0, 1:headerSize+1] = final
    return

def writeFullContentIntoHostFile(transposedImageMatrix, contentByteArray):

     # Producing matrix of extracted bits from all content bytes
    bitsFromContentBytes = np.vstack(utils.vectorizedExtractBitsFromByte(contentByteArray))
    bitsFromContentBytes = np.transpose(bitsFromContentBytes, (1,0))

    # Getting all pixels from image except those dedicated to the header (first row of image)
    writableMatrix = transposedImageMatrix[:, 1:, :]
    print(writableMatrix.shape)
    rows = writableMatrix.shape[1]
    cols = writableMatrix.shape[2]

    # Teste se double reshape esta resultando na mesma matrix... Deu certo,
    # então dá pra usar o mesmo raciocício da escrita do header e depois voltar para shape
    # de duas dimensões para cada banda de cor....

    # contentMatrix2 = np.reshape(contentMatrix, (3, rows*cols))
    # print(contentMatrix2.shape)
    # contentMatrix3 = np.reshape(contentMatrix, (3, rows, cols))
    # print(contentMatrix3.shape)
    # print("np.array_equal(contentMatrix, contentMatrix3) -> ", np.array_equal(contentMatrix, contentMatrix3))
    # print("contentMatrix == contentMatrix3 -> ", contentMatrix == contentMatrix3)

    writableMatrixLineShapedByColor = np.reshape(writableMatrix, (3, rows*cols))
    contentSize = contentByteArray.size
    final = utils.vectorizedMove3LastBits(writableMatrixLineShapedByColor[0, 0:contentSize], bitsFromContentBytes[0])
    final = np.vstack((final, utils.vectorizedMove3LastBits(writableMatrixLineShapedByColor[1, 0:contentSize], bitsFromContentBytes[1])))
    final = np.vstack((final, utils.vectorizedMove2LastBits(writableMatrixLineShapedByColor[2, 0:contentSize], bitsFromContentBytes[2])))
    
    writableMatrixLineShapedByColor[:, 0:contentSize] = final
    writableMatrix = np.reshape(writableMatrixLineShapedByColor, (3, rows, cols))

    print("np.array_equal(transposedImageMatrix[:, 1:, :], contentMatrix) -> ", np.array_equal(transposedImageMatrix[:, 1:, :], writableMatrix))
    transposedImageMatrix[:, 1:, :] = writableMatrix
    return


parser = argparse.ArgumentParser()
parser.add_argument('--imgHostFile', type=str, help='Image to be used as the host of the hidden content')
parser.add_argument('--inputFile', type=str, help='File to be hidden in the image passed on --imgHostFile')
parser.add_argument('--outputFileName', type=str, help='Name of the resulting image. Include extension')
parser.add_argument('--fileNameWhenDecode', type=str, help='Name of the file when decoding takes place. Include extension')

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
print(img.shape)

if (img.shape[1]-1)*img.shape[2] < inputFileBytes.size:
    print("Content to be hidden is larger than image!! Choose a greater image")
    exit()

headerDict = createHeader(inputFileBytes.size, args.fileNameWhenDecode)
writeHeaderIntoHostFile(img, headerDict)
writeFullContentIntoHostFile(img, inputFileBytes)

img = np.transpose(img, (2,1,0))
cv.imwrite(args.outputFileName, img)