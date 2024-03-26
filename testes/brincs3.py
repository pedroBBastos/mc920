# como zerar os últimos n bits de um número???

toZero = 4
number = 202
print("Zerando os ultimos ", toZero, " bits do numero ", number, "(", '{:08b}'.format(number) , ")")


masc = 1 << toZero
print('{:08b}'.format(masc))
masc -= 1
print('{:08b}'.format(masc))
masc = ~masc
print('{:08b}'.format(masc))

number &= masc
print("Numero com os ", toZero, " bits zeros: ", '{:08b}'.format(number))

# como trocar os ultimos n bits de um número??????

nToExtract = 7
print("Colocando os ", toZero, " ultimos bits do numero ", nToExtract, "(", '{:08b}'.format(nToExtract) , ") em ", '{:08b}'.format(number))

mascaraParaPegarNUltimosBits = 2**toZero - 1

bitsToBePlaced = nToExtract & mascaraParaPegarNUltimosBits
print("The following bits are to be placed at the least ", toZero, " significant bits of number ", '{:08b}'.format(number), ": ", '{:08b}'.format(bitsToBePlaced))

number ^= bitsToBePlaced
print("Result ->>> ", bin(number), " = ", number)
