import numpy as np
import cv2 as cv
import argparse
import pickle


# header size in 1 byte
# header
# content

def changeLast3BitsBetweenNumbers(a, b):
    # codigo ja ta pronto no brincs3.py
    # TODO: Poderia essa funcao aqui ser uma ufunc do numpy????
    return

# The header will have the output file extension and the file bytes size...
# The header will be a serialized python dictionary
def createHeader(size):
    headerDict = {'extension': '.png', 'content-size': size}
    serialized_bytes = pickle.dumps(headerDict)
    return np.frombuffer(serialized_bytes, dtype=np.uint8)

def writeHeaderIntoHostFile(hostImage, header):
    headerSize = header.size
    # TODO: Write header size
    return


parser = argparse.ArgumentParser()
parser.add_argument('--imgHostFile', type=str, help='Image to be used as the host of the hidden content')
parser.add_argument('--inputFile', type=str, help='File to be hidden in the image passed on --imgHostFile')
parser.add_argument('--outputFileName', type=str, help='Name of the resulting image. Include extension')

args = parser.parse_args()
print(args)

inputFileBytes = np.fromfile(args.inputFile, dtype=np.uint8)
print(inputFileBytes)
print("inputFileBytes.shape -> ", inputFileBytes.shape)
print("inputFileBytes.size -> ", inputFileBytes.size)

img = cv.imread(args.imgHostFile)
print("size -> ", img.size)
print("shape -> ", img.shape)
print("type -> ", type(img))