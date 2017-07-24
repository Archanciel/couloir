import queue
from time import sleep

q = queue.Queue()

q.put('a')
q.put('b')
q.put('c')

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
                
        
    def changeWidth(self, width):
        widthOffset = self.__width - width
        widthIncrement = 1 if widthOffset > 0 else -1
        
        for i in range(abs(widthOffset)):
            self.__width += widthIncrement
        
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

seg = Segment(15, 7, 0.03)
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

for i in range(4):
    seg.draw()
    if i % 2 == 0:
        seg.changeWidth(7)
    else:
        seg.changeWidth(3)
        
        


        
        