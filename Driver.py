import string

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
        directionList = []
        
        for i in range(len(stringRepr) - 1):
            sChar = stringRepr[i]
            eChar = stringRepr[i + 1]
            if sChar == eChar:
                continue
                
            startAscii = ord(sChar)
            endAscii = ord(eChar)
                
            orientation = 0
            steps = 0
            
            if startAscii > endAscii: #par ex w > a
                orientation = 'l'
            else:   
                orientation = 'r'
                
            steps = abs(startAscii - endAscii)     
            directionList.append(Direction(orientation, steps))
            
        return directionList
    	
class Direction:
    def __init__(self, orientation, steps):
        self.orientation = orientation
        self.steps = steps
        
    def __str__(self):
        return self.orientation + ' ' + str(self.steps)

class Driver:
    def __init__(self, geoMap):
        self.geoMap = geoMap
        self.location = 0

    def drive(self):
        direction = geoMap.getDirection(self.location)
        self.location += 1

        return direction   
        
s = StringGeoMap("Tamara, Walter, Béatrice. Jean-Pierre")

for i in range(s.getStepNumber()):
    d = s.getDirection(i)
    print(d)