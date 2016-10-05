'''
- this is a working version
- car starting point changes with down arrow
- frame speed increases/decreases with left/right arrow key respectively
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
    posState, negState, wallStateMatrix = posNegWall_load
    return q_matrix, posState, negState, wallStateMatrix

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
    gamePath = []
    for state in breadcrumb:
        x_state, y_state = state
        x = y_state * 100
        y = x_state * 100
        gamePath.append((x,y))

    return gamePath

def changeGame():
    # define constants
    num_rows = 7
    num_cols = 7
    col_max = num_cols - 1
    row_max = num_rows - 1

    # defining grid
    q_matrix, posState, negState, wallStateMatrix = openPickledFiles()

    moveMatrix = makeMoveMatrix(q_matrix, num_rows, row_max, col_max, posState, negState, wallStateMatrix)
    availableState = createStates(num_rows, num_cols, posState, negState, wallStateMatrix)
    # trail shows the matrix string representation and breadcrumb is a list of tuples
    # each tuple is the state on path of destinatino
    trail, path = breadcrumb(moveMatrix, availableState, num_rows, num_cols, posState, negState, wallStateMatrix)
    game_path = gamePath(path)
    return game_path

##gamePath = changeGame()
##print(gamePath)


# --------------------pygame----------------------------------------
def playGame(gamePath):
    # initialize
    pygame.init()

    display_width = 700
    display_height = 700



    black = (0,0,0)
    white = (255,255,255)
    red = (230,50,50)

    up_angle = 90
    right_angle = 0
    left_angle = 180
    down_angle = 270

    # tuple is width,height
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('A bit Racey')

    clock = pygame.time.Clock()

    carImage = pygame.image.load('images/car-red.png')
    carImage = pygame.transform.scale(carImage, (100, 100))

    def car(x,y, angle):
        carImageRotated = pygame.transform.rotate(carImage, angle)
        gameDisplay.blit(carImageRotated,(x,y))

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
        
    def game_loop(gamePath):

        #x, y = convertState(state)
        
        angle = right_angle
        angle_list = [right_angle,
                      right_angle,
                      right_angle,
                      right_angle,
                      right_angle,
                      down_angle,
                      down_angle,
                      ]

        coord_delta = [(0,0), (100,0), (100,0), (100,0), (100,0), (0,100), (0,100)]
        counter = 0
        n = 5

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
                gamePath = changeGame()
                counter = 0
                
            gameDisplay.fill(white)
            
            if counter < len(gamePath):
                x,y = gamePath[counter]
                car(x,y,angle)
                counter += 1
            else:
                counter = 0

            #time.sleep(1)

            #if (x > display_width - 100) or (x < 0):
            #    crash()
            
            pygame.display.update()
            clock.tick(n) #number is frames/sec

    game_loop(gamePath)
    pygame.quit()  # quit pygame
    quit()         # quit idle

if __name__ == '__main__':
    path = changeGame()
    print(path)
    playGame(path)

'''
if __name__ == '__main__':

    # define constants
    num_rows = 7
    num_cols = 7
    col_max = num_cols - 1
    row_max = num_rows - 1

    # defining grid
    q_matrix, posState, negState, wallStateMatrix = openPickledFiles()

    moveMatrix = makeMoveMatrix(q_matrix)
    availableState = createStates()
    # trail shows the matrix string representation and breadcrumb is a list of tuples
    # each tuple is the state on path of destinatino
    trail, breadcrumb = breadcrumb(moveMatrix, availableState)
    gamePath = gamePath(breadcrumb)

    #play game
    playGame(gamePath)
''' 
