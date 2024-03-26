text = "Some text to be chunked..."
# print(ord(text))

for c in text:
    
    print('{:08b}'.format(ord(c)))
    
    mascara3Bits = 7 # 0b111
    mascara2Bits = 3 # 0b011

    asciiValue = ord(c)
    first3Bits = asciiValue & mascara3Bits
    print("first3Bits -> ", '{:08b}'.format(first3Bits))
    asciiValue = asciiValue >> 3

    second3Bits = asciiValue & mascara3Bits
    print("second3Bits -> ", '{:08b}'.format(second3Bits))
    asciiValue = asciiValue >> 3

    print("last2Bits -> ", '{:08b}'.format(asciiValue))


    print("-------------------------------------")