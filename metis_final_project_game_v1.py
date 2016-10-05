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

display_width = 900
display_height = 600

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
    
def game_loop():

    x = (display_width * 0.45)
    y = (display_height * 0.8)
    angle = up_angle

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
        car(x,y,angle)

        # just drawing a rectangle
        pygame.draw.rect(gameDisplay, red, Rect((40,40),(90,90)))

        #if (x > display_width - 100) or (x < 0):
        #    crash()
        
        pygame.display.update()

        clock.tick(30) #number is frames/sec

game_loop()
pygame.quit()  # quit pygame
quit()         # quit idle 

