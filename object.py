import pygame
import random


victim_citizen = ['hospital', 'school', 'citizen']
victim_army = ['army', 'army airport', 'military base']
weapon = ['missle', 'chemical weapon', 'firefighter' 'bomber', 'helicopter']
CITIZEN = 0
ARMY = 1

class NewsGroup(pygame.sprite.Group):
    def __init__(self):
        self.surface = None # update from step
        self.news_list = []
        self.broadcast = []

    # return list of news
    def step(self, surface, position):

        self.broadcast = []
        for news in self.news_list:
            if news.draw(surface, position):
                self.broadcast.append(news.texts)
                self.news_list.remove(news)
    
        return self.broadcast
    

    def createNews(self, attacker, victim, position):
        self.news_list.append(attacker.name, victim.name, position)


class News(pygame.sprite.Sprite):

    def __init__(self, attacker_name, victim_name, position):
        self.is_fake_news = True if random.random() < 0.2 else False
        scale = random.random() * 0.5 + 0.5 # 0.5~1

        self.image = pygame.image.load("images/fake_news.png").convert_alpha() \
            if self.is_fake_news else pygame.image.load("images/news_.png").convert_alpha()
        width = img.get_width()
        height = img.get_height()
        self.texts = ['Breaking News!']
        #self.image = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
        self.rect = self.img.get_rect()
        self.rect.center = position

        self.weapon = random.choice(weapon)
        self.mode = CITIZEN if self.is_fake_news else (CITIZEN if random() < 0.2 else ARMY)

        self.victim_number = int((scale * 10) ** 2)

        self.reputation_bonus = random.random()
        self.attention_bonus = scale * (3 if self.mode == CITIZEN else 1)
        self.authenticity_bonus = random.random()*2-1 if self.is_fake_news else random.random()

        
        self.victim = random.choice(victim_citizen) if random.random() < 0.2 else random.choice(victim_army)


        self.texts.append(attacker_name + ' attacked ' + victim_name + "'s " + self.victim + ' using ' + self.weapon)
        self.texts.append(str(self.victim_number) + (' citizens ' if self.mode == CITIZEN else ' solders ') +'dead and injured from this attack')
        self.texts.append('from ' + victim_name)

        self.isBroadCasted = False

    def update(self):
        pass

    def draw(self, surface, pos):


        #draw button on screen
        surface.blit(self.img, (self.rect.x, self.rect.y))

        if self.isBroadCasted:
            self.broadcast(surface, pos)

	
    def broadcast(self, surface, pos):
        pass


class Weapon(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed = 10
		self.image = pygame.image.load("missiles_.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction

	def update(self):
		
		#check collision with characters
		if pygame.sprite.spritecollide(player, bullet_group, False):
			if player.alive:
				player.health -= 5
				self.kill()
		for enemy in enemy_group:
			if pygame.sprite.spritecollide(enemy, bullet_group, False):
				if enemy.alive:
					enemy.health -= 25
					self.kill()