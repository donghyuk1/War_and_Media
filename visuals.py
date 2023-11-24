import pygame
import math
from settings import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.surface = pygame.display.get_surface()

        #camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.surface.get_size()[0] // 2
        self.half_h = self.surface.get_size()[1] // 2
        
        # box setup
        self.camera_borders = {'left' : 200, 'right' : 200, 'top' : 100, 'bottom' : 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.surface.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.surface.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l,t,w,h)
        
        # ground
        self.ground_surf = pygame.image.load('images/wave.jpg').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

        self.keyboard_speed = 5
		# zoom 
        self.zoom_scale = 1
        self.internal_surf_size = (2500,2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

    def center_target_camera(self,target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def box_target_camera(self,target):

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d]: self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]: self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]: self.camera_rect.y += self.keyboard_speed

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoom_scale += 0.1
        if keys[pygame.K_e]:
            self.zoom_scale -= 0.1
            self.zoom_scale = max(self.zoom_scale, 0.1)

    def custom_draw(self,player):
        
        self.center_target_camera(player)
        #self.box_target_camera(player)
        #self.keyboard_control()
        self.zoom_keyboard_control()

        self.internal_surf.fill('#71ddee')

        # ground 
        ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
        self.internal_surf.blit(self.ground_surf,ground_offset)

        # active elements
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surf.blit(sprite.image,offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surf,self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center = (self.half_w,self.half_h))

        self.surface.blit(scaled_surf,scaled_rect)




class RocketEffectMaster():
    def __init__(self, missle_img, target_img, explode_img):
        self.effects = []
        self.isCollide = False
        self.missle_img = missle_img
        self.target_img = target_img
        self.explode_img = explode_img
    
    def step(self, surface, pos):
        self.isCollide = False
        for effect in self.effects:
            (collide, end) = effect.draw(surface, pos)
            if end:
                self.effects.remove(effect)
            if collide:
                self.isCollide = True
        return self.isCollide
    
    def installEffect(self, initial_pos, terminate_pos):
        self.effects.append(RocketEffect(initial_pos=initial_pos, 
                                         terminate_pos=terminate_pos, 
                                         missle_img=self.missle_img, 
                                         target_img=self.target_img, 
                                         explode_img=self.explode_img))
    
    def collide(self):
        return self.isCollide

    def listNews(self):
        pass
    
    


class RocketEffect():
    def __init__(self, initial_pos, terminate_pos, missle_img, target_img, explode_img, lifetime=2, explode_time=1):
        self.explode = False
        self.img = missle_img
        self.target_img = target_img
        self.explode_img = explode_img
        self.init_pos = initial_pos
        self.term_pos = terminate_pos
        self.pos_x = self.init_pos[0]
        self.pos_y = self.init_pos[1]
        self.time = 0
        self.explode_time = explode_time * FPS
        self.lifetime = lifetime * FPS
        self.inc_x = (terminate_pos[0] - initial_pos[0]) / self.lifetime
        self.inc_y = (terminate_pos[1] - initial_pos[1]) / self.lifetime
        self.rect = self.target_img.get_rect()
        self.rect.center = self.term_pos
        self.terminate = False
        self.is_collide = False


    def draw(self, surface, pos):

        self.is_collide = False
        self.time += 1
        # update position
        self.pos_x += self.inc_x
        self.pos_y += self.inc_y
        rotate_angle = (math.atan2(-self.inc_y, self.inc_x)) / math.pi * 180
        rotated_img = pygame.transform.rotate(self.img, rotate_angle)
        rotated_img_rect = rotated_img.get_rect()
        rotated_img_rect.center = (self.pos_x, self.pos_y)
        if self.time > self.lifetime:
            self.explode = True

        if (self.time == (self.lifetime + self.explode_time)):
            self.terminate = True

        if not self.explode:
            surface.blit(rotated_img, (rotated_img_rect.x, rotated_img_rect.y))
            surface.blit(self.target_img, (self.rect.x, self.rect.y))
            pygame.draw.line(surface, RED, (self.pos_x, self.pos_y), self.term_pos, width=1)
        elif self.explode:
            if self.rect.collidepoint(pos):
                self.is_collide = True
            surface.blit(self.explode_img, (self.rect.x, self.rect.y))

        return (self.is_collide, self.terminate)
        

class EffectMaster():
    def __init__(self):
        self.effects = []  # list of effects

    def step(self, surface):
        for effect in self.effects:
            effect.draw(surface)
            if(effect.isTerminate()):
                self.effects.remove(effect)
            
    def installEffect(self, img, initial_pos, terminate_pos):
        self.effects.append(Effect(img, initial_pos=initial_pos, terminate_pos=terminate_pos))


class Effect():
    def __init__(self, img, initial_pos, terminate_pos, lifetime=30):
        self.img = img
        self.init_pos = initial_pos
        self.term_pos = terminate_pos
        self.pos_x = self.init_pos[0]
        self.pos_y = self.init_pos[1]
        self.time = 0
        self.lifetime = lifetime
        self.inc_x = (terminate_pos[0] - initial_pos[0]) / self.lifetime
        self.inc_y = (terminate_pos[1] - initial_pos[1]) / self.lifetime
        self.terminate = False

    def draw(self, surface):
        
        self.time += 1

        # update position
        self.pos_x += self.inc_x
        self.pos_y += self.inc_y
        rotate_angle = (math.atan2(-self.inc_y, self.inc_x)) / math.pi * 180
        rotated_img = pygame.transform.rotate(self.img, rotate_angle)
		#draw button on screen
        surface.blit(rotated_img, (self.pos_x, self.pos_y))
        
        if (self.time == self.lifetime):
            self.terminate = True

    def isTerminate(self):
        return self.terminate
    
def changeColor(surface, color):
    w, h = surface.get_size()
    for i in range(w):
        for j in range(h):
            if surface.get_at((i, j))[0] != 0:
                surface.set_at((i, j), color)