class Interpolation:
    def interpolate(self, mappedInputRow, mappedInputColumn, originalImage):
        raise Exception("No interpolation implemented...")

class NearestNeighborInterpolation(Interpolation):
    def interpolate(self, mappedInputRow, mappedInputColumn, originalImage):
        return originalImage[round(mappedInputRow-1), round(mappedInputColumn-1)]

class BilinearInterpolation(Interpolation):
    def interpolate(self, mappedInputRow, mappedInputColumn, originalImage):
        y = int(mappedInputRow)
        x = int(mappedInputColumn)
        dy = abs(mappedInputRow - y)
        dx = abs(mappedInputColumn - x)
        try:
            upperLeftNeighborWeighedValue = abs((1-dx))*abs((1-dy))*originalImage[y,x]
            upperRightNeighborWeighedValue = dx*abs((1-dy))*originalImage[y,x+1]
            lowerLeftNeighborWeighedValue = abs((1-dx))*dy*originalImage[y+1, x]
            lowerRightNeighborWeighedValue = dx*dy*originalImage[y+1, x+1]

            return  upperLeftNeighborWeighedValue + \
                    upperRightNeighborWeighedValue + \
                    lowerLeftNeighborWeighedValue + \
                    lowerRightNeighborWeighedValue
        except IndexError as e:
            # print("IndexError")
            # estou por padrão assumindo que sempre que alguma conta acima sair para fora da imagem
            # eu atribuo o valor do pixel x,y passado (com mod caso este tbem esteja saindo da img)
            return originalImage[y%originalImage.shape[0], x%originalImage.shape[1]]
            # TODO: verificar se fazer o mod, como o acima, é a melhor forma 
            # de contornar o BO de IndexError quando a img de saida é maior que a de entrada...
            # resized_image[row, column] = image[y, x]
            # if resized_image[row, column] <= 0 or resized_image[row, column] >= 255:
            #     print("---------------------------------")
            #     print("On IndexError -> ", resized_image[row, column])
            #     print("---------------------------------")

class BicubicInterpolation(Interpolation):
    def __P(self, t):
        return t if t > 0 else 0

    def __R(self, s):
        return (1/6)*(self.__P(s+2)**3 - 4*self.__P(s+1)**3 + 6*self.__P(s)**3 - 4*self.__P(s-1)**3)
    
    def interpolate(self, mappedInputRow, mappedInputColumn, originalImage):
        inputRows, inputColumns = originalImage.shape[:2]
        y = int(mappedInputRow)
        x = int(mappedInputColumn)
        dy = abs(mappedInputRow - y)
        dx = abs(mappedInputColumn - x)
        sum = 0
        for m in [-1, 0, 1, 2]:
            for n in [-1, 0, 1, 2]:
                sum += originalImage[(y+n)%inputRows,(x+m)%inputColumns]*self.__R(m-dx)*self.__R(dy-n)
        return sum

class LagrangeInterpolation(Interpolation):
    def __L(self, n, x, y, dx, image, inputRows, inputColumns):
        return (-dx*(dx-1)*(dx-2)*image[(y+n-2)%inputRows,(x-1)%inputColumns])/6 + \
            ((dx+1)*(dx-1)*(dx-2)*image[(y+n-2)%inputRows, x%inputColumns])/2 + \
            (-dx*(dx+1)*(dx-2)*image[(y+n-2)%inputRows, (x+1)%inputColumns])/2 + \
            (dx*(dx+1)*(dx-1)*image[(y+n-2)%inputRows, (x+2)%inputColumns])/6
    
    def interpolate(self, mappedInputRow, mappedInputColumn, originalImage):
        inputRows, inputColumns = originalImage.shape[:2]
        y = int(mappedInputRow)
        x = int(mappedInputColumn)
        dy = abs(mappedInputRow - y)
        dx = abs(mappedInputColumn - x)
        return -dy*(dy-1)*(dy-2)*self.__L(1, x, y, dx, originalImage, inputRows, inputColumns)/6 + \
                (dy+1)*(dy-1)*(dy-2)*self.__L(2, x, y, dx, originalImage, inputRows, inputColumns)/2 + \
                -dy*(dy+1)*(dy-2)*self.__L(3, x, y, dx, originalImage, inputRows, inputColumns)/2 + \
                dy*(dy+1)*(dy-1)*self.__L(4, x, y, dx, originalImage, inputRows, inputColumns)/6
    
