import queue
from time import sleep
import random as r

q = queue.Queue()

q.put('a')
q.put('b')
q.put('c')

MAX_SEGMENT_WIDTH = 30
MIN_SEGMENT_WIDTH = 3
SLEEP_TIME_SEC = 0.05

while not q.empty():
    print(q.get())

class Step:
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
        raise NotImplementedError("Please Implement this method")

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

class RightStep(Step):
    def __init__(self, size = 1):
        super().__init__("\\", "\\", size)

    def calculateOffset(self, previousStep):
        if previousStep.__class__.__name__ == RightStep.__name__:
            return 1
        elif previousStep.__class__.__name__ == LeftStep.__name__:
            return 0

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
        
    def draw(self):
        self.currPos = self.leftPos
        
        for positionedStep in self.steps:
            offset = positionedStep.offset
            step = positionedStep.step
            filler = self.__filler(offset)
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
            self.__width += changeWidthIncrement
        
            for positionedStep in self.steps:
                step = positionedStep.step
                step.size = self.width
                
            self.draw()
                       
    def __filler(self, offset):
        s = ""
        self.currPos += offset
        
        for i in range(self.currPos):
            s += " "
            
        return s
        
lst = LeftStep()
rst = RightStep()

seg = Segment(10, 7, SLEEP_TIME_SEC)
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

for i in range(1):
    seg.changePosAndWidth(0, r.randint(0, 35))

        


        
        