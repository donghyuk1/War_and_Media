import pygame
import world
import random
import time
import sys
from settings import *

random.seed(time.time())

class Weapon(pygame.sprite.Sprite):
	def __init__(self, pos, group):
		super().__init__(group)
		self.speed = 10
		self.image = pygame.image.load("images/missiles_.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (pos.x, pos.y)

	def update(self):
		
		#check collision with characters
		'''if pygame.sprite.spritecollide(self, explode_group, False):
			self.kill()'''

class Country(pygame.sprite.Group):
    def __init__(self, img, pos):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos.x, pos.y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.pos = pos

        self.weapon_list = [] # list of weapon positions

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        super().draw(surface)

    def generateWeapon(self, num_weapon):
        for i in range(num_weapon):
            super().add(Weapon(self.generateRandomPoint(), self))

    def generateRandomPoint(self):
        within = False
        while not within:
            randomPoint = pygame.math.Vector2(random.randint(0, self.width-1), random.randint(0, self.height-1))
            if withinMask(self.image, randomPoint):
                within = True
        return randomPoint + self.pos
        



############################################################################################################
#functions

def changeColor(surface, color):
    w, h = surface.get_size()
    for i in range(w):
        for j in range(h):
            if surface.get_at((i, j))[0] != 0:
                surface.set_at((i, j), color)

def withinMask(surface, point):
    print(point)

    if surface.get_at((int(point.x), int(point.y)))[0] == 0:
        return False
    else:
        return True


'''def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))'''





pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

img = pygame.image.load("images/country1.png").convert_alpha()
map = world.getWorldMap()

countryGroup = Country(img, pygame.math.Vector2(100, 100))
countryGroup.generateWeapon(10)

clock = pygame.time.Clock()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    screen.blit(map, (0, 0), (0, 0, WORLD_WIDTH, WORLD_HEIGHT))

    countryGroup.update()
    countryGroup.draw(screen)


    pygame.display.update()

    clock.tick(FPS)
