import string
from chemin import *
import random as r

MAX_ASCII_VALUE = 122
MIN_ASCII_VALUE =65
START_WIDTH = 20
START_POS = 30
MIN_WIDTH_INC = 2
MAX_WIDTH_INC = 5

class GeoMap:
    def __init__(self, pathRepresentation):
        self.directionList = self._decode(pathRepresentation)

    def _decode(self, representation):
        raise NotImplementedError("Please Implement this method")
        
    def getDirection(self, step):
        return self.directionList[step]
        
    def getStepNumber(self):
        return len(self.directionList)
        
class StringGeoMap(GeoMap):
    def __init__(self, stringRepr):
        super().__init__(stringRepr)
        
    def _decode(self, stringRepr):
        '''
        Transforme un texte en une liste de Direction's
        '''
        #élimine les espaces
        stringRepr = "".join(filter(str.isalpha, stringRepr))

        #append to stringrepr its first char so that when looping on corrsponding direction when changing the segment width
        #no gap occurs
        stringRepr = stringRepr + stringRepr[0]
        directionList = []
        
        for i in range(len(stringRepr) - 1):
            sChar = stringRepr[i]
            eChar = stringRepr[i + 1]
            if sChar == eChar:
                continue
                
            startAscii = ord(sChar)
            endAscii = ord(eChar)
            startAscii = self._normaliseAscii(startAscii)
            endAscii = self._normaliseAscii(endAscii)

            orientation = 0
            steps = 0
            
            if startAscii > endAscii: #par ex w > a
                orientation = 'l'
            else:   
                orientation = 'r'
                
            steps = abs(startAscii - endAscii)     
            directionList.append(Direction(orientation, steps))
            
        return directionList

    def _normaliseAscii(self, asciiCode):
        if asciiCode > MAX_ASCII_VALUE:
            return MAX_ASCII_VALUE
        elif asciiCode < MIN_ASCII_VALUE:
            return MIN_ASCII_VALUE
        else:
            return asciiCode

class Direction:
    def __init__(self, orientation, stepNumber):
        self.orientation = orientation
        self.stepNumber = stepNumber
        
    def __str__(self):
        return self.orientation + ' ' + str(self.stepNumber)

class Driver:
    def __init__(self, geoMap):
        self.geoMap = geoMap
        self.segment = Segment(START_POS, START_WIDTH, SLEEP_TIME_SEC)
        ball = Ball("*")

        for i in range(self.geoMap.getStepNumber()):
            direction = self.geoMap.getDirection(i)
            step = Step.createStep(direction.orientation, ball, START_WIDTH)
            for j in range(direction.stepNumber):
                self.segment.addStep(step)

    def drive(self):
        widthInc = self._calcNewWidthInc(1)
        self.segment.changePosAndWidth(0,START_WIDTH + widthInc)
        widthInc = self._calcNewWidthInc(widthInc)
        self.segment.changePosAndWidth(0, START_WIDTH + widthInc)
        widthInc = self._calcNewWidthInc(widthInc)
        self.segment.changePosAndWidth(0, START_WIDTH + widthInc)
        widthInc = self._calcNewWidthInc(widthInc)
        self.segment.changePosAndWidth(0, START_WIDTH + widthInc)


    def _calcNewWidthInc(self, previousWidthInc):
        widthInc = r.randint(-MAX_WIDTH_INC, MAX_WIDTH_INC)
        while abs(widthInc) < MIN_WIDTH_INC:
            widthInc = r.randint(-MAX_WIDTH_INC, MAX_WIDTH_INC)
        if (previousWidthInc < 0 and widthInc < 0) or (previousWidthInc > 0 and widthInc > 0):
            widthInc *= -1
        return widthInc


if __name__ == '__main__':
    #driver = Driver(StringGeoMap("Tamara, Walter, Béatrice. Jean-Pierre"))
#    driver = Driver(StringGeoMap("Tamara, adadadadad, Walter, Béatrice. Jean-Pierre, adadadadad"))
    driver = Driver(StringGeoMap("adadadadad, acaeafadad, adadadadad"))
    driver.drive()

