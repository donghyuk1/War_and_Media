import pygame
import button
import effect
import country

#import os

#change working directory to current file directory
#os.chdir(os.path.dirname(os.path.realpath(__file__))) 

pygame.init()

#create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#game variables
game_paused = False

#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colours
TEXT_COL = (255, 255, 255) #white

#load button images
resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
video_img = pygame.image.load('images/button_video.png').convert_alpha()
audio_img = pygame.image.load('images/button_audio.png').convert_alpha()
keys_img = pygame.image.load('images/button_keys.png').convert_alpha()
back_img = pygame.image.load('images/button_back.png').convert_alpha()
country_img= pygame.image.load('images/country.png').convert_alpha()
rocket_img = pygame.image.load('images/fireworks.png').convert_alpha()

#create button instances
resume_button = button.Button(304, 125, resume_img, 1)
options_button = button.Button(297, 250, options_img, 1)
quit_button = button.Button(0, 0, quit_img, 0.5)
video_button = button.Button(226, 75, video_img, 1)
keys_button = button.Button(246, 325, keys_img, 1)
back_button = button.Button(332, 450, back_img, 1)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

clock = pygame.time.Clock()
PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT,40)

effects = effect.EffectMaster()  # empty effect

Player = country.Object(country_img, 200, 100, 1, 100, 10, 100, 100, country.BLUE)
B = country.Object(country_img, 500, 100, 1, 100, 10, 100, 100, country.GREEN)


#game loop
run = True
while run:
  
  
  screen.fill((52, 78, 91))



  #check if game is paused
  if game_paused == True:
    #check menu state
    #draw pause screen buttons
    if resume_button.draw(screen):
      game_paused = False
    if quit_button.draw(screen):
      run = False


  else:
    Player.draw(screen)
    if B.draw(screen) == country.ATTACK:
      effects.installEffect(rocket_img, Player.getPosition(), B.getPosition())

    if quit_button.draw(screen):
      run = False
      draw_text("Press SPACE to pause", font, TEXT_COL, 160, 250)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
          game_paused = True
    if event.type == pygame.QUIT:
      run = False
    if event.type == PARTICLE_EVENT:
        effects.emit(screen)

  pygame.display.update()

  clock.tick(60)

pygame.quit()