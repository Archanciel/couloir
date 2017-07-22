from time import sleep
import random as r

MAX_SCREEN_WIDTH = 40
MAX_WIDTH = 11 #largeur max du couloir
MIN_WIDTH = 2 #largeur min du couloir
STEP_LENGTH = 0.025 #durée pause entre dessin d'une ligne en seconde
ITERATION_NUMBER = 500
#STEP_LENGTH = 0.05 #durée pause entre dessin d'une ligne en seconde
#ITERATION_NUMBER = 300


def populateLine(currWidth, ballX):
    '''
    Remplit la ligne qui est écrite
    toutes les STEP_LENGTH seconde
    pour simuler l'avancement dans
    le couloir.
    '''
    str, leftWallX = fillLeftSpace(currWidth)
    str += '|'
    isBallDrawn = False
    ballX -= leftWallX
    
    for i in range(currWidth):
        if i == ballX:
            str += '*'
            isBallDrawn = True
        else:
            str += ' '
        
    if not isBallDrawn:
        if ballX < currWidth / 2:
            str = str.replace("| ", "|*")
            str += '|'
        else:
            str += "*|"
    else:
        str += '|'
    
    return str, leftWallX + 1, leftWallX + currWidth

def fillLeftSpace(currWidth):
    '''
    Remplit le string retourné
    d'un nombre d'espaces fonction
    de la largeur du couloir à
    dessiner.
    '''
    str = ''
    spaceNumber = int((MAX_SCREEN_WIDTH - currWidth) / 2)
    glitch = r.randint(0, 1)
    spaceNumber += glitch
    
    for i in range(spaceNumber):
        str += ' '
    
    return str, spaceNumber

def varyCurrWidth(currWidth, variationAmount, variationChangeNumber):
    '''
    Calcule la variation de la largeur
    du couloir.
    '''
    if variationChangeNumber <= 0:
        variationAmount = r.randint(0, 1)
        if variationAmount == 0:
            variationAmount = -1
            
 #   variationAmount += variationAmount
    currWidth += variationAmount
    
    if currWidth > MAX_WIDTH:
        currWidth = MAX_WIDTH
        variationAmount = -1
        variationChangeNumber = MAX_VAR_CHANGE_NUMBER
    
    if currWidth < MIN_WIDTH:
        currWidth = MIN_WIDTH
        variationAmount = 1
        variationChangeNumber = MAX_VAR_CHANGE_NUMBER

    return currWidth, variationAmount

def calculateBallPosition(ballX, ballDirection, leftWallX, rightWallX):
    '''
    Calcule la position de la balle.
    
    La balle se déplace de gauche à
    droite et vice versa, changeant
    de direction lorsqu'elle se
    heurte au mur du couloir.
    '''
    
    if ballX < leftWallX:
        ballDirection = 1
    elif ballX >= rightWallX - 1:
        ballDirection = -1
        
    ballX += ballDirection
    
    return ballX, ballDirection
    
variationAmount = -1 
newCurrWidth = oldCurrWidth = MAX_WIDTH
MAX_VAR_CHANGE_NUMBER = 10
variationChangeNumber = MAX_VAR_CHANGE_NUMBER
ballX = int(MAX_SCREEN_WIDTH / 2) #coordonnée x de la balle
ballDirection = 1
leftWallX = 1
rightWallX = newCurrWidth - 1

#boucle principale
for i in range(ITERATION_NUMBER):
    line, leftWallX, rightWallX = populateLine(newCurrWidth, ballX)
    print(line)
    newCurrWidth, variationAmount = varyCurrWidth(oldCurrWidth, variationAmount, variationChangeNumber)
    ballX, ballDirection = calculateBallPosition(ballX, ballDirection, leftWallX, rightWallX)
    variationChangeNumber -= 1
    
    if variationChangeNumber <= -1 * MAX_VAR_CHANGE_NUMBER:
        variationChangeNumber = MAX_VAR_CHANGE_NUMBER
           
    sleep(STEP_LENGTH)
