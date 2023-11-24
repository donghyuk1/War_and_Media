import math
import pygame
import button
#import visuals
#import country
import world
from settings import *
import random
import time
random.seed(time.time())
from copy import deepcopy as deep



class News(pygame.sprite.Sprite):

    def __init__(self, attacker_name, victim_name, position, mode):
        pygame.sprite.Sprite.__init__(self)
        self.is_fake_news = True if random.random() < 0.2 else False
        scale = random.random() * 0.5 + 0.5 # 0.5~1

        self.image = pygame.image.load("images/fake-news_.png").convert_alpha() \
            if self.is_fake_news else pygame.image.load("images/news_.png").convert_alpha()
        
        self.texts = ['Breaking News!']
        #self.image = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = deep(position)

        self.weapon = random.choice(WEAPON)
        self.mode = mode

        self.victim_number = int((scale * 10) ** 2)

        self.attention_bonus = scale * (3 if self.mode == CITIZEN else 1)
        self.authenticity_bonus = random.random()*2-1 if self.is_fake_news else random.random()

        
        self.victim = random.choice(victim_citizen) if random.random() < 0.2 else random.choice(victim_army)


        self.texts.append(attacker_name + ' attacked ' + victim_name + "'s " + self.victim + ' using ' + self.weapon)
        self.texts.append(str(self.victim_number) + (' citizens ' if self.mode == CITIZEN else ' solders ') +'dead and injured from this attack')
        self.texts.append('from ' + victim_name)
        self.life = len(self.texts)
        self.status = -1
        self.time = 0
        self.max_time = FPS * NEWSTIME
    
    def update(self):

        global broadcast
        if not broadcast:
            self.time += 1
        if self.time > self.max_time:
            self.kill()

        if pygame.sprite.spritecollide(self, player_group, False):
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                time.sleep(0.1)
                self.status +=1
        if self.status >= self.life:
            broadcast = False
            self.kill()
            return
        elif self.status == -1:
            return
        global news_text
        news_text = self.texts[self.status]


    '''def draw(self, surface):
        if self.status == -1:
            print(self.status)

            surface.blit(self.image, self.rect)
        else:
            print(self.texts)
            print(self.status)
            print(self.texts[self.status])
            global news_text
            news_text = deep(self.texts[self.status])'''


class Weapon(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.speed = 10
        self.image = pygame.image.load("images/missiles_.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = deep(pos)
        self.rect.center = (pos.x, pos.y)

    '''def update(self):
        
        #check collision with characters
        if pygame.sprite.spritecollide(self, explode_group, False):
            self.kill()'''
    
    def getPosition(self):
        return self.pos
               

class Rocket(pygame.sprite.Sprite):
    def __init__(self, init_pos, term_pos, attack_name, attacked_name, color):
        super().__init__()
        self.speed = 5
        self.image = pygame.image.load("images/missile_.png").convert_alpha()
        self.target_image = pygame.image.load("images/aim_.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (init_pos.x, init_pos.y)
        self.pos = deep(init_pos)
        self.term_pos = deep(term_pos)
        self.direction = deep((self.term_pos - self.pos).normalize())
        rotate_angle = (math.atan2(-self.direction.y, self.direction.x)) / math.pi * 180
        self.image = pygame.transform.rotate(self.image, rotate_angle)
        self.time = (term_pos - init_pos).length() // self.speed
        self.attack_name = attack_name
        self.attacked_name = attacked_name
        
        self.color = color

    def update(self):
        self.time -= 1
        #move bullet
        self.pos += self.direction * self.speed
        self.rect.center = (self.pos.x, self.pos.y)
        #check if bullet has gone off screen

        if self.time < 0:
            explode_group.add(Explode(self.term_pos, self.attack_name, self.attacked_name))
            self.kill()

    def drawLine(self, surface):
        pygame.draw.line(surface, self.color, (self.pos.x, self.pos.y), (self.term_pos.x, self.term_pos.y), width=1)

    def drawTarget(self, surface):
        target_rect = self.target_image.get_rect()
        target_rect.center = (self.term_pos.x, self.term_pos.y)
        surface.blit(self.target_image, target_rect)


## TODO : from this

class Explode(pygame.sprite.Sprite):
    def __init__(self, pos, attack_name, attacked_name, time=1):
        super().__init__()
        self.image = pygame.image.load("images/explosion_.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = deep(pos)
        self.rect.center = self.pos
        self.time = time * FPS
        self.attack_name = attack_name
        self.attacked_name = attacked_name
        self.mode = CITIZEN

    def update(self):
        self.time -= 1
        country_list = war.getCountryList()
        for country in  country_list:
            weapon_collide_list = pygame.sprite.spritecollide(self, country, False)
            if weapon_collide_list:
                self.mode = ARMY
                for weapon_collide in weapon_collide_list:
                    weapon_collide.kill()


        if self.time < 0:
            news_group.add(News(self.attack_name, self.attacked_name, self.pos, self.mode))
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/player_.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(pos)
        self.speed = 5
        self.health = 100
        self.reputation = 0 # max 100!
        self.attention = 1
        self.authenticity = 0
        self.flip = False

      
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.flip = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.flip = False
        else:
            self.direction.x = 0

    def update(self):

        self.input()
        self.pos += self.direction * self.speed
        self.rect.center = self.pos

        if pygame.sprite.spritecollide(self, explode_group, False):
            self.health = 0
        
        for news in pygame.sprite.spritecollide(self, news_group, False):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                global broadcast
                broadcast = True
                self.report(news.attention_bonus, news.authenticity_bonus)
                
    def report(self, attention_bonus, authenticity_bonus):
        self.attention += attention_bonus
        self.authenticity += authenticity_bonus
        self.reputation += self.attention * self.authenticity
        
    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        

    def getPosition(self):
        return self.pos

class RocketGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, surface):
        super().draw(surface)
        for sprite in self.sprites():
            sprite.drawLine(surface)
            sprite.drawTarget(surface)


class Country(pygame.sprite.Group):
    def __init__(self, img, pos, team, name):
        super().__init__()
        self.image = img
        self.team = team
        self.name = name
        changeColor(img, RED) if self.team == 'teamA' else changeColor(img, GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.pos = pos


    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        surface.blit(flag_img, self.rect.center)
        super().draw(surface)

    def generateWeapon(self, num_weapon):
        for i in range(num_weapon):
            random_point = self.generateRandomPoint()
            Weapon(random_point, self)
            print(f'installed weapon in position {random_point}')

    def generateRandomPoint(self):
        within = False
        while not within:
            randomPoint = pygame.math.Vector2(random.uniform(0, self.width-1), random.uniform(0, self.height-1))
            if withinMask(self.image, randomPoint):
                within = True
        return randomPoint + self.pos

    def getPosition(self):
        return self.pos
    
    def getName(self):
        return self.name


class War():
    def __init__(self):
        self.teamA = []
        self.teamB = []

    def addTeamA(self, img, pos, name):
        new_country = Country(img, pos, 'teamA', name)
        new_country.generateWeapon(INIT_WEAPON)
        self.teamA.append(new_country)
    
    def addTeamB(self, img, pos, name):
        new_country = Country(img, pos, 'teamB', name)
        new_country.generateWeapon(INIT_WEAPON)
        self.teamB.append(new_country)
    
    def update(self):
        rand = random.random()
        if rand < violent:
            self.attack()
        rand1 = random.random()
        rand2 = random.random()
        if rand1 < violent:
            if rand2 < 0.5:
                random.choice(self.teamA).generateWeapon(1)
            else:
                random.choice(self.teamB).generateWeapon(1)

        for country in self.teamA:
            country.update()
        for country in self.teamB:
            country.update()
    
    def draw(self, surface):
        for country in self.teamA:
            country.draw(surface)
        for country in self.teamB:
            country.draw(surface)
        
        
    def attack(self):
        rand = random.random()

        if rand < 0.5:
            attack = random.choice(self.teamA)
            attacked = random.choice(self.teamB)
            list_sprites = attack.sprites()
            if list_sprites:
                weapon = random.choice(list_sprites)
            else:
                return
            init_position = deep(weapon.getPosition())
            attack_position = deep(attacked.generateRandomPoint())
            #attack_position = random.choice(self.teamB).getPosition()
            rocket_group.add(Rocket(init_position, attack_position, attack.getName(), attacked.getName(), RED))
        else:
            attack = random.choice(self.teamB)
            attacked = random.choice(self.teamA)
            list_sprites = attack.sprites()
            if list_sprites:
                weapon = random.choice(list_sprites)
            else:
                return
            init_position = deep(weapon.getPosition())
            attack_position = deep(attacked.generateRandomPoint())
            #attack_position = random.choice(self.teamB).getPosition()
            rocket_group.add(Rocket(init_position, attack_position, attack.getName(), attacked.getName(), GREEN))

    def getCountryList(self):
        return self.teamA + self.teamB


############################################################################################################
#functions

def changeColor(surface, color):
    w, h = surface.get_size()
    for i in range(w):
        for j in range(h):
            if surface.get_at((i, j))[0] != 0:
                surface.set_at((i, j), color)

def withinMask(surface, point):

    if surface.get_at((int(point.x), int(point.y)))[0] == 0:
        return False
    else:
        return True

def renderText(text, font, text_col):
    return font.render(text, True, text_col)

def gameEnding(surface):
    text_img = renderText("You died due to unexpected attack while reporting...", font, WHITE)
    for i in range(4 * FPS):
        surface.fill(RED2)
        surface.blit(text_img, (200, 300))
        pygame.display.update()

        clock.tick(FPS)
    
def gameWining(surface):
    text_img = renderText("You became a great reporter! Congrats!!", font, WHITE)
    for i in range(4 * FPS):
        surface.fill(BLUE2)
        surface.blit(text_img, (200, 300))
        pygame.display.update()

        clock.tick(FPS)

############################################################################################################
#where the script begins

pygame.init()

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#pygame.display.set_caption("Main Menu")

violent = 0.01

#game variables
game_paused = False
game_end = False
broadcast = False
die = False
win = False


#define fonts
font = pygame.font.SysFont("arialblack", 25)
camera_borders = {'left' : 300, 'right' : 300, 'top' : 200, 'bottom' : 200}
news_text = None


#load button images
resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
keys_img = pygame.image.load('images/button_keys.png').convert_alpha()
back_img = pygame.image.load('images/button_back.png').convert_alpha()
country_img1= pygame.image.load('images/country1_.png').convert_alpha()
country_img2= pygame.image.load('images/country2_.png').convert_alpha()
country_img3= pygame.image.load('images/country3_.png').convert_alpha()
country_img4= pygame.image.load('images/country4_.png').convert_alpha()

news_background_img = pygame.transform.scale(pygame.image.load('images/news_background.jpg').convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))
news_announcer_img = pygame.image.load('images/broadcast.png').convert_alpha()
flag_img = pygame.image.load('images/country.png').convert_alpha()



#full screen
#add all the screens to this map, and crop it to the screen size considering position

map = world.getWorldMap()

#create button instances
resume_button = button.Button(500, 300, resume_img, 1)
quit_button = button.Button(250, 300, quit_img, 1)
player = Player((300, 300))

camera_offset = pygame.math.Vector2(0, 0)

# sprite Group
#weapon_group = pygame.sprite.Group() # group of weapons
rocket_group = RocketGroup() #pygame.sprite.Group() # group of flying rockets
explode_group = pygame.sprite.Group() # group of explosion effect
news_group = pygame.sprite.Group() # group of news
player_group = pygame.sprite.Group()
player_group.add(player)

war = War()
war.addTeamA(country_img1, pygame.math.Vector2(200, 200), 'Gryffindor')
war.addTeamB(country_img2, pygame.math.Vector2(800, 800), 'Hufflepuff')
war.addTeamA(country_img3, pygame.math.Vector2(1200, 600), 'Ravenclaw')
war.addTeamB(country_img2, pygame.math.Vector2(1200, 1200), 'Slytherin')

clock = pygame.time.Clock()

#PARTICLE_EVENT = pygame.USEREVENT + 1
#pygame.time.set_timer(PARTICLE_EVENT,40)

#game loop
run = True
while run:

    full_screen = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
    screen.fill(BG_COL)
    
    if player.health <= 0:
        die = True
        run = False

    if player.reputation >= 100:
        win = True
        run = False

    #check if game is paused
    if game_paused == True:
        #check menu state
        #draw pause screen buttons
        if resume_button.draw(screen):
            game_paused = False
        if quit_button.draw(screen):
            die = False
            run = False
    

    elif broadcast == True:
        news_group.update()
        news_group.draw(screen)
        news_text_img = renderText(news_text, font, WHITE)
        screen.blit(news_background_img, (0, 0))
        screen.blit(news_announcer_img, (200, 300))
        screen.blit(news_text_img, (100, 100))


    else:
        full_screen.blit(map, (0, 0), (0, 0, WORLD_WIDTH, WORLD_HEIGHT))

        war.update()
        player.update()
        rocket_group.update()
        explode_group.update()
        news_group.update()

        war.draw(full_screen)
        player.draw(full_screen)
        rocket_group.draw(full_screen)
        explode_group.draw(full_screen)
        news_group.draw(full_screen)

        player_pos = player.getPosition()
        if player_pos.x < (camera_offset.x + camera_borders['left']):
            camera_offset.x = player_pos.x - camera_borders['left']
        if player_pos.x > (camera_offset.x + SCREEN_WIDTH - camera_borders['right']):
            camera_offset.x = player_pos.x - SCREEN_WIDTH + camera_borders['right']
        if player_pos.y < (camera_offset.y + camera_borders['top']):
            camera_offset.y = player_pos.y - camera_borders['top']
        if player_pos.y > (camera_offset.y + SCREEN_HEIGHT - camera_borders['bottom']):
            camera_offset.y = player_pos.y - SCREEN_HEIGHT + camera_borders['bottom']
        

        screen.blit(full_screen, (0, 0), (camera_offset.x, camera_offset.y, WORLD_WIDTH, WORLD_HEIGHT))
        repu_img = renderText(f"reputation : {int(player.reputation)}", font, WHITE)
        atten_img = renderText(f"attention : {int(player.attention)}", font, WHITE)
        auth_img = renderText(f"authenticity : {int(player.authenticity)}", font, WHITE)
        screen.blit(repu_img, (0, 0))
        screen.blit(atten_img, (0, 50))
        screen.blit(auth_img, (0, 100))

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_paused = True
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()


    clock.tick(FPS)

if die:
    gameEnding(screen)
if win:
    gameWining(screen)
pygame.quit()