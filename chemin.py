import queue
from time import sleep
import random as r

q = queue.Queue()

q.put('a')
q.put('b')
q.put('c')

MAX_SEGMENT_WIDTH = 40
MIN_SEGMENT_WIDTH = 3

while not q.empty():
    print(q.get())

class Step:
    def __init__(self, leftWall, rightWall, offset, size = 1):
        self.size = size
        self.leftWall = leftWall
        self.rightWall = rightWall
        self.offset = offset

    def getLine(self):
        return self.leftWall + self.__fillSpaces() + self.rightWall
    
    def __fillSpaces(self):
        s = ""
        
        for i in range(self.size):
            s += " "
            
        return s

class VerStep(Step):
    def __init__(self, size = 1):
        super().__init__('|', '|', 0, size)
        
class LeftStep(Step):
    def __init__(self, size = 1):
        super().__init__('/', '/', -1, size)
        
class RightStep(Step):
    def __init__(self, size = 1):
        super().__init__("\\", "\\", 1, size)

class Segment():
    def __init__(self, leftPos, width, sleepTime = 0.1):
        self.leftPos = leftPos
        self.steps = [] 
        self.width = width
        self.sleepTime = sleepTime
        
    def addStep(self, step):
        step.size = self.width
        self.steps.append(step)
        
    def draw(self):
        self.currPos = self.leftPos
        
        for step in self.steps:
            filler = self.__filler(step.offset)
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
                
        
    def changeWidth(self, newWidth):
        if newWidth > MAX_SEGMENT_WIDTH:
            newWidth = MAX_SEGMENT_WIDTH
        elif newWidth < MIN_SEGMENT_WIDTH:
            newWidth = MIN_SEGMENT_WIDTH

        changeIncrement = 0

        if newWidth > self.__width:
            changeIncrement = 1
        elif newWidth < self.__width:
            changeIncrement = -1

        incrementNumber = abs(newWidth - self.__width)

        for i in range(incrementNumber):
            self.__width += changeIncrement
        
            for step in self.steps:
                step.size = self.width
                
            self.draw()
                       
    def __filler(self, offset):
        s = ""
        self.currPos += offset
        
        for i in range(self.currPos):
            s += " "
            
        return s
        
vst = VerStep()
lst = LeftStep()
rst = RightStep()
vst = VerStep()

seg = Segment(15, 7, 0.01)
seg.addStep(vst)
seg.addStep(lst)
seg.addStep(lst)
seg.addStep(vst)
seg.addStep(rst)
seg.addStep(rst)
seg.addStep(vst)
seg.addStep(lst)
seg.addStep(lst)
seg.addStep(lst)
seg.addStep(lst)
seg.addStep(vst)
seg.addStep(rst)
seg.addStep(rst)
seg.addStep(rst)
seg.addStep(rst)

seg.draw()

for i in range(20):
    seg.changeWidth(r.randint(1, 45))

        


        
        