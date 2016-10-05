'''
- to do:
(1) [done] put walls for each element in wallStateMatrix

from previous version:
(1) [done]make care change direction so that it is facing right way
(2) [done] adiabatic tapering (x,y)
(3) [done] straightforward angle change
'''

import numpy as np
import random
from sklearn.externals import joblib
import pygame
from pygame.locals import *
import time

def openPickledFiles():
    q_matrix = joblib.load('qMatrix_7by7_ver2.pkl')
    posNegWall_load = joblib.load('posNegWallState_7by7_ver2.pkl')
    trainingStates = joblib.load('overallTrainingStates_7by7_ver3.pkl')
    posState, negState, wallStateMatrix = posNegWall_load
    return q_matrix, posState, negState, wallStateMatrix, trainingStates

def makeMoveMatrix(q_matrix, num_rows, row_max, col_max, posState, negState, wallStateMatrix):
    
    actionAbbr = ['U','D','L','R']
    movementGrid = []

    for i in range(row_max+1):
        #x = q_matrix[i*5 : i*5+5].flatten()
        x = q_matrix[i*num_rows : i*num_rows+num_rows].flatten()
        row = []
        for j in range(col_max+1):
            row.append(actionAbbr[np.argmax(x[j*4:j*4+4])])
        movementGrid.append(row)
    moveMatrix = np.array(movementGrid)
    
    #putting in the wall, pos and neg states
    for wallState in wallStateMatrix:
        moveMatrix[wallState] = 'X'
    moveMatrix[posState] = '+'
    moveMatrix[negState] = '-'
    
    return moveMatrix

def createTrail(num_rows, num_cols, posState, negState, wallStateMatrix):
    emptyStrRow = [' ']*num_cols
    trailLst = []
    for _ in range(7):
        trailLst.append(emptyStrRow)
    
    trail = np.array(trailLst)
    
    for wallState in wallStateMatrix:
        trail[wallState[0], wallState[1]] = 'X'
    trail[posState[0], posState[1]] = '+'
    trail[negState[0], negState[1]] = '-'
    
    return trail

def createStates(num_rows, num_cols, posState, negState, wallStateMatrix):
    states = []

    for i in range(num_rows):
        for j in range(num_cols):
            states.append((i,j))

    availableState = states[:]
    for wallState in wallStateMatrix:
        availableState.pop(availableState.index(wallState))
        
    availableState.pop(availableState.index(posState))
    availableState.pop(availableState.index(negState))

    return availableState

def breadcrumb(moveMatrix, availableState, num_rows, num_cols, posState, negState, wallStateMatrix):
    
    trail = createTrail(num_rows, num_cols, posState, negState, wallStateMatrix)
    
    state = availableState[np.random.choice(len(availableState))]
    trail[state] = '@'
    breadCrumb = [state]
    while state != posState:
        direction = moveMatrix[state]
        if direction == 'U': state = (state[0]-1, state[1])
        if direction == 'D': state = (state[0]+1, state[1])
        if direction == 'L': state = (state[0], state[1]-1)
        if direction == 'R': state = (state[0], state[1]+1)
        
        breadCrumb.append(state)
    
    for element in breadCrumb[1:-1]:
        trail[element] = '*'
        
    return trail, breadCrumb

def gamePath(breadcrumb):
    '''
    Program return the game coordinates car should use to get to destination
    - breadcrumb: path as a list of states
    - Improvement: don't assume steps are always 100, use another variable to control this
    '''
    gamePath = []
    for state in breadcrumb:
        x_state, y_state = state
        x = y_state * 100
        y = x_state * 100
        gamePath.append((x,y))

    return gamePath

def getStateDirection(pathList, moveMatrix):
    angleList = []
    for path in pathList:
        direction = moveMatrix[path]
        if direction == 'U': angleList.append(90)
        if direction == 'D': angleList.append(270)
        if direction == 'L': angleList.append(180)
        if direction == 'R': angleList.append(0)

    # final reward should have car oriented right
    angleList.append(0)

    return angleList

def expandPath(gamePath):
    expandedPath = []
    count = 0
    while count < len(gamePath)-1:
        currentGridCoord = gamePath[count]
        expandedPath.append(currentGridCoord)
        
        delta_x = int((gamePath[count+1][0] - gamePath[count][0])/10)
        delta_y = int((gamePath[count+1][1] - gamePath[count][1])/10)

        x, y = currentGridCoord
        for _ in range(9):
            x = x + delta_x
            y = y + delta_y
            expandedPath.append( (x, y)  )
        count += 1
    expandedPath.append(gamePath[-1])
    return expandedPath

def expandAngle(angleList):
    expandedAngle = []
    count = 0
    while count < len(angleList)-1:
        currentAngle = angleList[count]
        expandedAngle.append(currentAngle)

        angle = currentAngle

        delta = int((angleList[count+1] - angleList[count])/10)
        for _ in range(9):
            angle = angle + delta
            expandedAngle.append(angle)
        count += 1
    expandedAngle.append(angleList[-1])

    return expandedAngle

def expandAngle2(angleList):
    expandedAngle = []
    count = 0
    while count < len(angleList)-1:
        currentAngle = angleList[count]
        expandedAngle.append(currentAngle)

        angle = currentAngle

        first = angleList[count]
        last = angleList[count + 1]
        avg = 0.5*(first + last)
        #extra = [first, 0.75*first, 0.5*first, 0.25*first, avg, 0.25*last, 0.50*last, 0.75*last, last]
        extra = [first]*9
        expandedAngle.extend(extra)
    
        count += 1
    expandedAngle.append(angleList[-1])

    return expandedAngle
        
def changeGame():
    # define constants
    num_rows = 7
    num_cols = 7
    col_max = num_cols - 1
    row_max = num_rows - 1

    # defining grid
    q_matrix, posState, negState, wallStateMatrix, trainingStates = openPickledFiles()

    moveMatrix = makeMoveMatrix(q_matrix, num_rows, row_max, col_max, posState, negState, wallStateMatrix)
    availableState = createStates(num_rows, num_cols, posState, negState, wallStateMatrix)
    # trail shows the matrix string representation and breadcrumb is a list of tuples
    # each tuple is the state on path of destination
    #----- changing from 'path' to 'prevPath'
    trail, path = breadcrumb(moveMatrix, availableState, num_rows, num_cols, posState, negState, wallStateMatrix)

    # here we determine direction of car
    angleList = getStateDirection(path, moveMatrix)

    # this path in grid coordinates
    game_path = gamePath(path)

    # intermediate states
    expandedGamePath = expandPath(game_path)

    # intermediate angles
    expandedAngle = expandAngle2(angleList)

    # rectangle coordinates
    wallRectCoord = gamePath(wallStateMatrix)

    # training path
    trainingPaths = []
    for paths in trainingStates[1:]:
        trainingPaths.extend(paths)
    overallTrainingPath = gamePath(trainingPaths)
    
    return game_path, trail, path, angleList, expandedGamePath, expandedAngle, wallRectCoord, overallTrainingPath

# --------------------pygame----------------------------------------
def playGame(gamePath, angleList, wallRectCoord):
    # initialize
    pygame.init()

    display_width = 700
    display_height = 700

    black = (0,0,0)
    lightBlack = (20,20,20)
    white = (255,255,255)
    red = (230,50,50)
    grey = (200,200,200)
    yellow = (255,255,0)

    up_angle = 90
    right_angle = 0 #360
    left_angle = 180
    down_angle = 270

    # tuple is width,height
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('Smart Car')

    clock = pygame.time.Clock()

    carImage = pygame.image.load('images/car-red.png')
    carImage = pygame.transform.scale(carImage, (100, 100))

    #buildingImage = pygame.image.load('images/building_1.jpg')
    buildingImage = pygame.image.load('images/cartoon_house_3.png')
    buildingImage = pygame.transform.scale(buildingImage, (100, 100))

    roadImage = pygame.image.load('images/road_5.jpg')
    roadImage = pygame.transform.scale(roadImage, (100,100))

    moneybag = pygame.image.load('images/bag-of-gold-clipart-1.jpg')
    moneybag = pygame.transform.scale(moneybag, (100, 100))
    
    jailHouse = pygame.image.load('images/jailHouse.png')
    jailHouse = pygame.transform.scale(jailHouse, (100, 100))

    def car(x,y, angle):
        carImageRotated = pygame.transform.rotate(carImage, angle)
        gameDisplay.blit(carImageRotated,(x,y))

    def building(x,y):
        gameDisplay.blit(buildingImage,(x,y))

    def draw_moneyBag_jailHouse(x,y):
        gameDisplay.blit(moneybag,(x,y))
        gameDisplay.blit(jailHouse,(x,y-100))

    def road(x,y):
        gameDisplay.blit(roadImage,(x,y))

    def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

    def message_display(text):
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        # text surface and rectangular containing the text
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()
        
        time.sleep(2)

        #restart the game
        game_loop()
        
    def crash():
        message_display('You crashed')

    def convertState(state):
        x_state, y_state = state
        x = y_state * 100
        y = x_state * 100

        return x,y

    def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
        x1, y1 = start_pos
        x2, y2 = end_pos
        dl = dash_length

        if (x1 == x2):
            ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
            xcoords = [x1] * len(ycoords)
        elif (y1 == y2):
            xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
            ycoords = [y1] * len(xcoords)
        else:
            a = abs(x2 - x1)
            b = abs(y2 - y1)
            c = round(math.sqrt(a**2 + b**2))
            dx = dl * a / c
            dy = dl * b / c

            xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
            ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

        next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
        last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
        for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
            start = (round(x1), round(y1))
            end = (round(x2), round(y2))
            pygame.draw.line(surf, color, start, end, width)
        
    def game_loop(gamePath, angleList, wallRectCoord):

        counter = 0
        n = 30

        gameExit = False

        while not gameExit:

            # we put all events in this loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #gameExit = True
                    pygame.quit()
                    quit()
     
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT] and (x > -5):
                #x -= 10
                #angle = left_angle
                n += 2
            if pressed[pygame.K_RIGHT]  and (x < display_width - 90):
                #x += 10
                #angle = right_angle
                if n > 2:
                    n -= 2
            if pressed[pygame.K_UP] and (y>0):
                y -= 10
                angle = up_angle
            if pressed[pygame.K_DOWN] and (y < display_height):
                #y+=10
                #angle = down_angle
                #_, _, _, angles, gamePath, angleList = changeGame()
                _, _, _, angles, gamePath, angleList, wallRectCoord = changeGame()
                counter = 0
                
            #gameDisplay.fill((200, 200, 200))
            gameDisplay.fill(lightBlack)

            '''drawing divider lines'''
            for i in range(7):
                draw_dashed_line(gameDisplay, yellow, (0, i*100+50), (800, i*100+50), dash_length=20)
                #draw_dashed_line(gameDisplay, yellow, (i*100+50, 0), (i*100+50, 700), dash_length=20)

   
            # just drawing a rectangle
            for rect in wallRectCoord:
                building(rect[0], rect[1])

            draw_moneyBag_jailHouse(600,600)
            
            if counter < len(gamePath):
                x,y = gamePath[counter]
                #angle = angleList[counter]
                angle = 0
                car(x,y,angle)
                counter += 1
            else:
                counter = 0

            

            #time.sleep(1)

            #if (x > display_width - 100) or (x < 0):
            #    crash()
            
            pygame.display.update()
            clock.tick(n) #number is frames/sec

    game_loop(gamePath, angleList, wallRectCoord)
    pygame.quit()  # quit pygame
    quit()         # quit idle

if __name__ == '__main__':

    game_path, trail, path, angleList, expandedGamePath, expandedAngle, wallRectCoord, overallTrainingPath = changeGame()
    #playGame(expandedGamePath, expandedAngle, wallRectCoord)
    playGame(overallTrainingPath, expandedAngle, wallRectCoord)
    '''
    print('training states: ', firstTrainingPath)
    print('game_path: ', game_path)
    '''
