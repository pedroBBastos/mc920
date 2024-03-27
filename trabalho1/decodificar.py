import numpy as np
import cv2 as cv
import argparse
import json
import sys
import utils

def find_difference(s1, s2):
    differences = []
    for i, (char1, char2) in enumerate(zip(s1, s2)):
        if char1 != char2:
            differences.append((i, char1, char2))
    return differences

def create_file_from_bytes(byte_stream, file_path):
    with open(file_path, 'wb') as f:
        f.write(byte_stream)

def readHeader(transposedImageMatrix):
    firstPixel = transposedImageMatrix[:, 0, 0]
    headerSize = utils.extractByteFromPixel(firstPixel)
    print("first pixel -> ", firstPixel, ", header size -> ", headerSize)

    headerContentMatrix = transposedImageMatrix[:, 0, 1:headerSize+1]
    print(headerContentMatrix)

    headerDictByteArray = utils.extractByteFromPixel(headerContentMatrix) # desse jeito aqui consegue fazer o broadcast.......
    my_string = headerDictByteArray.tobytes().decode('utf-8')
    my_string = my_string.replace('\x00', '') # por algum motivo, após o decode tem um monte de char nulo '\x00' na string....
    dictionary = json.loads(my_string)
    print("dictionary -> ", dictionary)

    return dictionary

def readContent(headerDict, transposedImageMatrix):
    contentSize = headerDict['content-size']

    readableMatrix = transposedImageMatrix[:, 1:, :]
    print("readableMatrix.shape -> ", readableMatrix.shape)
    rows = readableMatrix.shape[1]
    cols = readableMatrix.shape[2]
    readableMatrixLineShapedByColor = np.reshape(readableMatrix, (3, rows*cols))
    print("readableMatrixLineShapedByColor.shape -> ", readableMatrixLineShapedByColor.shape)

    message = readableMatrixLineShapedByColor[0, 0:contentSize]
    message = np.vstack((message, readableMatrixLineShapedByColor[1, 0:contentSize]))
    message = np.vstack((message, readableMatrixLineShapedByColor[2, 0:contentSize]))
    print("message.shape -> ", message.shape)
    message = message.T
    print("message.shape -> ", message.shape)
    message = utils.extractByteArrayFromPixelList(message)
    print("message.shape -> ", message.shape)

    create_file_from_bytes(message.tobytes(), headerDict['result-name'])
    return


parser = argparse.ArgumentParser()
parser.add_argument('--imgFile', type=str, help='Image with a hidden content')

args = parser.parse_args()
if len(sys.argv[1:]) < 1:
    print(args._get_args())
    parser.print_help()
    exit()


imgFileToDecode = cv.imread(args.imgFile)
imgFileToDecode = np.transpose(imgFileToDecode, (2,1,0))

headerDict = readHeader(imgFileToDecode)
readContent(headerDict, imgFileToDecode)