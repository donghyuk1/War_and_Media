import random
import pygame
import button

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

NONE = 0
FIRSTCLICK = 1
ATTACK = 2
#INVASION = 3
#INVESTIGATION = 4

class ObjectMaster():
    def __init__(self):
        self.player = None
        self.objects = []

    def attack(A, B):
        A.attck(B)

class Object(pygame.sprite.Sprite):
    def __init__(self, group, img, name, x, y, scale, init_health, power, init_money, radius, color):
        super().__init__(group)
        self.name = name
        width = img.get_width()
        height = img.get_height()
        self.flag_img = pygame.image.load("images/country.png")
    
        self.image = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.state = 0

        self.health = init_health
        self.power = power
        self.money = init_money
        self.color = color
        self.pos = (x, y) # position of its center
        self.size = radius # size of the country expressed with circle
        self.isWar = False
        self.clicked = False

        attack_img = pygame.image.load("images/button_resume.png").convert_alpha()
        investigate_img = pygame.image.load("images/button_quit.png").convert_alpha()
        
        self.attackButton = button.Button(x-20, y+20, attack_img, 1)
        #self.investigationButton = button.Button(x+20, y+20, investigate_img, 1)



    def draw(self, surface):
        
        
        pos = pygame.mouse.get_pos()


        '''if self.isWar:
            pygame.draw.circle(surface, RED, self.pos, self.size)
        else:
            pygame.draw.circle(surface, self.color, self.pos, self.size)'''

        #draw button on screen
        #surface.blit(self.image, (self.rect.x, self.rect.y))

		#check mouseover and clicked conditions

        action = self.showMenuButtons(surface, self.clicked)

        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
        else:
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = False

        return action


    def showMenuButtons(self, surface, isMenu=False):
        if isMenu == False:
            return
        else:
            if self.attackButton.draw(surface):
                self.clicked = False
                return ATTACK
            #elif self.investigationButton.draw()
            #   return INVESTIGATION

# weapon : image of weapon, used for drawing

    def isCollision(self, Opponent):
        dist = (self.pos[0] - Opponent.pos[0]) ** 2 +\
              (self.pos[1] - Opponent.pos[1]) **2 
        return (((self.size + Opponent.size) **2) >= dist)

    def attack(self, Opponent):
        self.money -= self.power
        self.isWar = True
        Opponent.invasion(self.power)


    def invasion(self, power):
        self.health -= power
        self.isWar = True

    def getPosition(self):
        return self.pos


class Weapon(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('images/missiles_.png')
        self.rect = self.image.get_rect(center = pos)

