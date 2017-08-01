from time import sleep
from enum import Enum

MAX_SEGMENT_WIDTH = 30
MIN_SEGMENT_WIDTH = 3
SLEEP_TIME_SEC = 0.03

class WallCorrection(Enum):
    RIGHT_TO_LEFT_WIDTH_DECR = 1
    LEFT_TO_RIGHT_WIDTH_DECR = 2
    RIGHT_TO_LEFT_WIDTH_INCR = 3
    LEFT_TO_RIGHT_WIDTH_INCR = 4
    NONE = 5

class Step:
    @staticmethod
    def createStep(stepType, stepSize):
        if stepType == 'r':
            return LeftStep(stepSize)
        elif stepType == 'l':
            return RightStep(stepSize)
        else:
            raise ValueError("Illegal stepType " + stepType + " encountered")

    def __init__(self, leftWall, rightWall, size = 1):
        self.size = size
        self.leftWall = leftWall
        self.rightWall = rightWall

    def getLine(self):
        return self.leftWall + self.__fillSpaces() + self.rightWall

    def calculateOffset(self, previousStep):
        '''
        Calcule le décalage par rapport à previousStep
        :param previousStep:
        :return: 0, 1 ou -1
        '''
        raise NotImplementedError("Please implement this method")

    def needRightToLeftWidthDecrWallCorrection(self, previousStep, changeWidthIncrement):
        return False

    def needRightToLeftWidthIncrWallCorrection(self, previousStep, changeWidthIncrement):
        return False

    def needLeftToRightWidthDecrWallCorrection(self, previousStep, changeWidthIncrement):
        return False

    def needLeftToRightWidthIncrWallCorrection(self, previousStep, changeWidthIncrement):
        return False

    def __fillSpaces(self):
        s = ""
        
        for i in range(self.size):
            s += " "
            
        return s

class LeftStep(Step):
    def __init__(self, size = 1):
        super().__init__('/', '/', size)

    def calculateOffset(self, previousStep):
        if previousStep.__class__.__name__ == RightStep.__name__:
            return 0
        elif previousStep.__class__.__name__ == LeftStep.__name__:
            return -1
        else:
            raise TypeError("Invalid class " + previousStep.__class__.__name__ + " encountered")

    def needRightToLeftWidthDecrWallCorrection(self, previousStep, changeWidthIncrement):
        '''
        Dans la configuration ci-dessous, nous avons un changement de direction de droite
        à gauche couplé à une diminution de la largeur du chemin de 1. Une correction
        sera nécessaire, comme on peut le voir !

        last step   \       \   RightStep
        first step  /      /    LeftStep
        next steps /      /

        :param previousStep:
        :param changeWidthIncrement:
        :return:
        '''
        if changeWidthIncrement < 0 and previousStep.__class__.__name__ == RightStep.__name__:
            return True
        else:
            return False

    def needRightToLeftWidthIncrWallCorrection(self, previousStep, changeWidthIncrement):
        '''
        Dans la configuration ci-dessous, nous avons un changement de direction de droite
        à gauche couplé à une augmentation de la largeur du chemin de 1. Une correction
        sera nécessaire, comme on peut le voir !

        last step   \      \   RightStep
        first step  /       /  LeftStep
        next steps /       /

        :param previousStep:
        :param changeWidthIncrement:
        :return:
        '''
        if changeWidthIncrement > 0 and previousStep.__class__.__name__ == RightStep.__name__:
            return True
        else:
            return False

class RightStep(Step):
    def __init__(self, size = 1):
        super().__init__("\\", "\\", size)

    def calculateOffset(self, previousStep):
        if previousStep.__class__.__name__ == RightStep.__name__:
            return 1
        elif previousStep.__class__.__name__ == LeftStep.__name__:
            return 0

    def needLeftToRightWidthDecrWallCorrection(self, previousStep, changeWidthIncrement):
        '''
        Dans la configuration ci-dessous, nous avons un changement de direction de gauche
        à droite couplé à une diminution de la largeur du chemin de 1. Une correction
        sera nécessaire, comme on peut le voir !

         /       /		last step == LeftStep
          \      \		first step == RightStep
           \      \

        :param previousStep:
        :param changeWidthIncrement:
        :return:
        '''
        if changeWidthIncrement < 0 and previousStep.__class__.__name__ == LeftStep.__name__:
            return True
        else:
            return False

    def needLeftToRightWidthIncrWallCorrection(self, previousStep, changeWidthIncrement):
        '''
		Dans la configuration ci-dessous, nous avons un changement de direction de gauche
		à droite couplé à une augmentation de la largeur du chemin de 1. Une correction
		sera nécessaire, comme on peut le voir !

         /      /		last step == LeftStep
          \        \	first step == RightStep
           \        \

		:param previousStep:
		:param changeWidthIncrement:
		:return:
		'''
        if changeWidthIncrement > 0 and previousStep.__class__.__name__ == LeftStep.__name__:
            return True
        else:
            return False


class PositionedStep:
    '''
    Container class qui dénote une Step positionnée en fonction de la Step qui la précède.

    Contient une Step et son offset tel qu'il a été calculé lors de l'ajout de la PositionedStep
    au Segment.

    En effet, sans cette classe, le Segment quui ne contiendrait que des Step ajoutées sans prendre
    en compte la Step qui la précède aurait cette allure:

         /   /
        /   /
       \   \
        \   \
         /   /
        /   /

    Avec cette classe:

         /   /      offset = 0
        /   /       offset = 0
        \   \       offset = 1
         \   \      offset = 0
         /   /      offset = -1
        /   /       offset = 0
    '''
    def __init__(self, offset, step):
        self.offset = offset
        self.step = step

class Segment():
    def __init__(self, leftPos, width, sleepTime = 0.1):
        self.leftPos = leftPos
        self.steps = [] 
        self.width = width
        self.sleepTime = sleepTime
        
    def addStep(self, step):
        step.size = self.width

        if len(self.steps) > 0:
            previousPositionedStep = self.steps[-1]
            offset = previousPositionedStep.step.calculateOffset(step)
        else:
            offset = 0

        self.steps.append(PositionedStep(offset, step))
        
    def draw(self, wallCorrection = WallCorrection.NONE):
        self.currPos = self.leftPos

        if wallCorrection == WallCorrection.RIGHT_TO_LEFT_WIDTH_DECR:
            '''
              \       \	9	last step
              /      /	8	first step
             /      /	8
                        if lst step == right et first step == left and ch width incr == -1
              \       \	9   last step
               \      /	8	first step: repl first '/' by ' \',
               /     /	7	reduce all further steps width by 1
            '''
            lastPositionedStep = self.steps[0]
            lastStep = lastPositionedStep.step

            #repl first '/' by ' \'
            filler = self.__filler(lastPositionedStep.offset + 1)
            firstStepWidthChangedLeftWall = lastStep.getLine().replace('/', '\\',1)

            #and now shift right wall
            firstStepWidthChangedLeftAndRightWall = self._replace_last(firstStepWidthChangedLeftWall, '/', ' /')

            print(filler + firstStepWidthChangedLeftAndRightWall)
            sleep(self.sleepTime)
            self.leftPos += 2
            self.currPos = self.leftPos

            for positionedStep in self.steps[1:]:
                self._drawStep(positionedStep)
        elif wallCorrection == WallCorrection.RIGHT_TO_LEFT_WIDTH_INCR:
            '''
              \      \
              /        /
             /        /

              \      \
              /       \ simply replace ' /' by '\' in firstStep.getLine()
             /        /
            '''
            lastPositionedStep = self.steps[0]
            lastStep = lastPositionedStep.step

            #repl first ' /' by '\'
            filler = self.__filler(lastPositionedStep.offset)
            firstStepWidthChangedRightWall = lastStep.getLine().replace(' /', '\\')

            print(filler + firstStepWidthChangedRightWall)
            sleep(self.sleepTime)

            for positionedStep in self.steps[1:]:
                self._drawStep(positionedStep)
        elif wallCorrection == WallCorrection.LEFT_TO_RIGHT_WIDTH_DECR:
            '''
             /       /	9	last step
              \      \	8	first step
               \      \
                        if lst step == left et first step == right and ch width incr == -1
             /       /	9	last step
             \      /	8	first step: decr curr (and further) offset by 1, repl last \ by / for first step
              \     \	7	reduce all further steps width by 1
            '''
            for positionedStep in self.steps:
                self._drawStep(positionedStep)
        elif wallCorrection == WallCorrection.LEFT_TO_RIGHT_WIDTH_INCR:
            '''
             /      /       8	last step
              \        \    10  first step
               \        \
                            if lst step == left et first step == right and ch width incr == 1
             /      /       8	last step
            /       \	    9   inserted step == last step with left wall ' /' replaced by '\', decr curr offset by 1
            \        \      10  first step: decr curr (and further) offset by 2
             \        \
            '''
            lastPositionedStep = self.steps[-1]
            lastStep = lastPositionedStep.step

            #insert step == last step with left wall ' /' replaced by '\', decr curr offset by 1
            insertedStepLine = self._replace_last(lastStep.getLine(),' /', '\\')
            filler = self.__filler(lastPositionedStep.offset - 1)
            print(filler + insertedStepLine)
            sleep(self.sleepTime)

            self.leftPos -= 2
            self.currPos = self.leftPos

            for positionedStep in self.steps:
                self._drawStep(positionedStep)
        else:
            for positionedStep in self.steps:
                self._drawStep(positionedStep)

    def _replace_last(self, source_string, replace_what, replace_with):
        head, _sep, tail = source_string.rpartition(replace_what)
        return head + replace_with + tail

    def _drawStep(self, positionedStep):
        step = positionedStep.step
        filler = self.__filler(positionedStep.offset)
        print(filler + step.getLine())
        sleep(self.sleepTime)

    @property
    def width(self):
        return self.__width
        
    @width.setter  
    def width(self, width):
        self.__width = width
        
        for step in self.steps:
            step.size = self.width

    def changePosAndWidth(self, newLeftPos, newWidth):
        '''
                  width (total, including walls)
            \   \	5
            /   /	5
            \  /	4
             \ \	3
              \ \	3
              /  \	4
             /   /	5
            /   /	5
           /   /	5
          /    \	6
         /      \	8
         \       \	9
          \       \	9
        :param newLeftPos:
        :param newWidth:
        :return:
        '''
        if newWidth > MAX_SEGMENT_WIDTH:
            newWidth = MAX_SEGMENT_WIDTH
        elif newWidth < MIN_SEGMENT_WIDTH:
            newWidth = MIN_SEGMENT_WIDTH

        changeWidthIncrement = 0

        if newWidth > self.__width:
            changeWidthIncrement = 1
        elif newWidth < self.__width:
            changeWidthIncrement = -1

        incrementNumber = abs(newWidth - self.__width)

        for i in range(incrementNumber):
            lastPositionedStep = self.steps[-1]
            firstPositionedStep = self.steps[0]
            rightToLeftWidthDecrWallCorrection = False
            leftToRightWidthDecrWallCorrection = False

            wallCorrection = WallCorrection.NONE

            if firstPositionedStep.step.needRightToLeftWidthDecrWallCorrection(lastPositionedStep.step, changeWidthIncrement):
                wallCorrection = WallCorrection.RIGHT_TO_LEFT_WIDTH_DECR
                changeWidthIncrement -= 1
            elif firstPositionedStep.step.needRightToLeftWidthIncrWallCorrection(lastPositionedStep.step, changeWidthIncrement):
                wallCorrection = WallCorrection.RIGHT_TO_LEFT_WIDTH_INCR
                changeWidthIncrement += 1
            elif firstPositionedStep.step.needLeftToRightWidthDecrWallCorrection(lastPositionedStep.step, changeWidthIncrement):
                wallCorrection = WallCorrection.LEFT_TO_RIGHT_WIDTH_DECR
                changeWidthIncrement -= 1
            elif firstPositionedStep.step.needLeftToRightWidthIncrWallCorrection(lastPositionedStep.step, changeWidthIncrement):
                wallCorrection = WallCorrection.LEFT_TO_RIGHT_WIDTH_INCR
                changeWidthIncrement += 1

            self.__width += changeWidthIncrement

            for positionedStep in self.steps:
                step = positionedStep.step
                step.size = self.__width

            self.draw(wallCorrection)

    def __filler(self, offset):
        s = ""
        self.currPos += offset
        
        for i in range(self.currPos):
            s += " "
            
        return s

import random as r

def testLeftToRightWithWidthInc():
    leftPos = 10

    startWidth = 6
    endWidth = 7

#    testLeftToRight(endWidth, leftPos, startWidth)

    startWidth = 7
    endWidth = 6

#    testLeftToRight(endWidth, leftPos, startWidth)

    startWidth = 6
    endWidth = 7

#    testRightToLeft(endWidth, leftPos, startWidth)

    startWidth = 7
    endWidth = 6

    testRightToLeft(endWidth, leftPos, startWidth)

def testLeftToRight(endWidth, leftPos, startWidth):
    print("LeftToRight testing. Start width: {}, end width: {}\n".format(startWidth, endWidth))

    seg = Segment(leftPos, startWidth, SLEEP_TIME_SEC)
    lst = LeftStep()
    rst = RightStep()

    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.draw()
    # seg.changePosAndWidth(0, r.randint(0, 35))
    seg.changePosAndWidth(0, endWidth)


def testRightToLeft(endWidth, leftPos, startWidth):
    print("RightToLeft testing. Start width: {}, end width: {}\n".format(startWidth, endWidth))

    seg = Segment(leftPos, startWidth, SLEEP_TIME_SEC)
    lst = LeftStep()
    rst = RightStep()

    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(rst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.addStep(lst)
    seg.draw()
    # seg.changePosAndWidth(0, r.randint(0, 35))
    seg.changePosAndWidth(0, endWidth)


if __name__ == '__main__':
    testLeftToRightWithWidthInc()