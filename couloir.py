from time import sleep
import random as r

MAX_WIDTH = 40 #largeur max du couloir
MIN_WIDTH = 30 #largeur min du couloir
STEP_LENGTH = 0.0125 #durée pause entre dessin d'une ligne en seconde
ITERATION_NUMBER = 1000
STEP_LENGTH = 0.05 #durée pause entre dessin d'une ligne en seconde
ITERATION_NUMBER = 300


def populateLine(currWidth, ballX):
    '''
    Remplit la ligne qui est écrite
    toutes les STEP_LENGTH seconde
    pour simuler l'avancement dans
    le couloir.
    '''
    str, leftWallX = fillLeftSpace(currWidth)
    str += '|'
    
    for i in range(currWidth):
        if i == ballX:
            str += '*'
        else:
            str += ' '
        
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
    spaceNumber = int((MAX_WIDTH - currWidth) / 2)
    
    for i in range(spaceNumber):
        str += ' '
    
    return str, spaceNumber

def varyCurrWidth(currWidth, variationAmount, variationChangeNumber):
    '''
    Calcule la variation de la largeur
    du couloir.
    '''
    if variationChangeNumber <= 0:
        variationAmount = r.randint(-1, 1)
    
    currWidth += variationAmount
    
    if currWidth > MAX_WIDTH:
        currWidth = MAX_WIDTH
        variationAmount = -1 * variationAmount
        variationChangeNumber = MAX_VAR_CHANGE_NUMBER
    
    if currWidth < MIN_WIDTH:
        currWidth = MIN_WIDTH
        variationAmount = -1 * variationAmount
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
currWidth = MAX_WIDTH
MAX_VAR_CHANGE_NUMBER = 10
variationChangeNumber = MAX_VAR_CHANGE_NUMBER
ballX = int(currWidth / 2) #coordonnée x de la balle
ballDirection = 1
leftWallX = 1
rightWallX = currWidth - 1

#boucle principale
for i in range(ITERATION_NUMBER):
    ballX, ballDirection = calculateBallPosition(ballX, ballDirection, leftWallX, rightWallX)
    line, leftWallX, rightWallX = populateLine(currWidth, ballX)
    print(line)
    currWidth, variationAmount = varyCurrWidth(currWidth, variationAmount, variationChangeNumber)
    variationChangeNumber -= 1
 #   ballX, ballDirection = calculateBallPosition(ballX, ballDirection, leftWallX, rightWallX)
    
    if variationChangeNumber <= -1 * MAX_VAR_CHANGE_NUMBER:
        variationChangeNumber = MAX_VAR_CHANGE_NUMBER
           
    sleep(STEP_LENGTH)
