import pygame
from settings import *
from visuals import changeColor

colors = ['green', '']


def getWorldMap():
    num_width = 5
    num_height = 5
    
    screen = pygame.Surface((WORLD_WIDTH,WORLD_HEIGHT))
    screen.fill(WHITE)
    bg = pygame.image.load("images/wave.jpg")
    bg = pygame.transform.scale(bg, (WORLD_WIDTH // num_width, WORLD_HEIGHT // num_height))
            
    for i in range(-num_width, num_width):
        for j in range(-num_height, num_height):
            screen.blit(bg, (i * (WORLD_WIDTH // num_width), j * (WORLD_HEIGHT // num_height)))
            

    '''c = pygame.image.load("images/country1.png").convert_alpha()
    changeColor(c, RED)

    screen.blit(c, (0, 0))'''


    return screen
