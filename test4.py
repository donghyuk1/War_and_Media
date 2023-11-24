
import pygame

 

# 스크린 전체 크기 지정

SCREEN_WIDTH = 400
SCREEN_HEIGHT  = 500

 

# 색상 상수

BLACK = (0, 0, 0)

 

# pygame 초기화

pygame.init()

 

# 스크린 객체 저장
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("pygame test")

 

# FPS를 위한 Clock 생성
clock = pygame.time.Clock()

 

playing = True
while playing:

    # 이벤트 처리
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()

 

       

    # 스크린 배경색 칠하기

    SCREEN.fill((255, 255, 255))

    myFont = pygame.font.SysFont( "arial", 30, True, False)

    text_Title= myFont.render("Pygame Text Test", True, BLACK)

    text_Rect = text_Title.get_rect()

    text_Rect.centerx = round(SCREEN_WIDTH / 2)

    text_Rect.y = 50

    SCREEN.blit(text_Title, text_Rect)

    text_Title2= myFont.render("Pygame Text Test 2", True, BLACK)

    SCREEN.blit(text_Title2, [50, 200])

    pygame.display.flip()

 

    # 1초에 60번의 빈도로 순환하기

    clock.tick(60)