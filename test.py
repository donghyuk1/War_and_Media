import pygame, sys
import visuals

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load('images/player_.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 5

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
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()

# setup 
camera_group = visuals.CameraGroup()
player = Player((640,360),camera_group)


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

		if event.type == pygame.MOUSEWHEEL:
			camera_group.zoom_scale += event.y * 0.03

	screen.fill('#71ddee')

	camera_group.update()
	camera_group.custom_draw(player)


	pygame.display.update()
	
	clock.tick(60)