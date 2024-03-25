import numpy as np

# constant definitions
maskToGet3LastBits = 7 # 0b111
maskToGet2LastBits = 3 # 0b011

maskToZero3LastBits = ~((1 << 3) - 1)
maskToZero2LastBits = ~((1 << 2) - 1)

def extractBitsFromByte(n):
    aux = n
    intoRed = aux & maskToGet3LastBits
    aux >>= 3
    intoGreen = aux & maskToGet3LastBits
    aux >>= 3
    intoBlue = aux
    return np.array([intoRed,intoGreen,intoBlue])

def move3LastBits(x, y):
    """
    Inserts to 3 least significant bits from y into the 3 x least significant bits
    and returns the new byte
    """
    auxX = x & maskToZero3LastBits
    bitsToBePlaced = y & maskToGet3LastBits
    return auxX ^ bitsToBePlaced

def move2LastBits(x, y):
    """
    Inserts to 2 least significant bits from y into the 2 x least significant bits
    and returns the new byte
    """
    auxX = x & maskToZero2LastBits
    bitsToBePlaced = y & maskToGet2LastBits
    return auxX ^ bitsToBePlaced

# defining vectorized functions
vectorizedExtractBitsFromByte = np.frompyfunc(extractBitsFromByte, 1, 1)
vectorizedMove3LastBits = np.frompyfunc(move3LastBits, 2, 1)
vectorizedMove2LastBits = np.frompyfunc(move2LastBits, 2, 1)

def extractByteFromPixel(threeBandsPixel):
    byteResult = move2LastBits(0, threeBandsPixel[2])
    byteResult <<= 3
    byteResult = move3LastBits(byteResult, threeBandsPixel[1])
    byteResult <<= 3
    byteResult = move3LastBits(byteResult, threeBandsPixel[0])
    return byteResult

def extractByteFromPixel2(threeBandsPixels: np.ndarray):
    # Initialize an empty array to store the results
    byteResults = np.empty(threeBandsPixels.shape[0], dtype=np.uint8)

    # Iterate over each row of the matrix
    for i, pixel in enumerate(threeBandsPixels):
        # Extract byte from the current row
        byteResult = move2LastBits(0, pixel[2])
        byteResult <<= 2
        byteResult = move3LastBits(byteResult, pixel[1])
        byteResult <<= 3
        byteResult = move3LastBits(byteResult, pixel[0])

        # Store the result in the array
        byteResults[i] = byteResult

    return byteResults