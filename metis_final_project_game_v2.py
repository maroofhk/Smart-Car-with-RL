'''
a. Based on the sentdex pygame tutorial on youtube
 - https://www.youtube.com/watch?v=xh4SV3kF-zk&index=3&list=PLQVvvaa0QuDdLkP8MrOXLe_rKuf6r80KO
 - title: Game Development in Python 3 With PyGame - 4 - Adding Boundaries
 - by: sentdex

1) tested out how to get a rectangle to be displayed in test1.py and using it here [https://www.youtube.com/watch?v=9-oS50C4B6Y]

'''

import pygame
from pygame.locals import *
import time

# initialize
pygame.init()

display_width = 700
display_height = 700

num_rows = 7
num_cols = 7

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
    
def game_loop(state):

    x, y = convertState(state)
    
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
            x -= 10
            angle = left_angle
        if pressed[pygame.K_RIGHT]  and (x < display_width - 90):
            x += 10
            angle = right_angle
        if pressed[pygame.K_UP] and (y>0):
            y -= 10
            angle = up_angle
        if pressed[pygame.K_DOWN] and (y < display_height):
            y+=10
            angle = down_angle

        gameDisplay.fill(white)
        
##        if counter < 7:
##            x += coord_delta[counter][0]
##            y += coord_delta[counter][1]
##            angle = angle_list[counter]
##            counter += 1
##        else:
##            counter = 0
##            x = 0
##            y = 0
##            angle = right_angle
##            
##        time.sleep(1)
        
        # just drawing a rectangle
        pygame.draw.rect(gameDisplay, red, Rect((0,0),(100,100)))
        car(x,y,angle)

        if (x > display_width - 100) or (x < 0):
            crash()
        
        pygame.display.update()

        clock.tick(1) #number is frames/sec

state = (5,3)
game_loop(state)
pygame.quit()  # quit pygame
quit()         # quit idle 

