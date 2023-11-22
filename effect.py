import pygame

class EffectMaster():
    def __init__(self):
        self.effects = []  # list of effects

    def emit(self, surface):
        for effect in self.effects:
            effect.draw(surface)
            if(effect.isTerminate()):
                self.effects.remove(effect)
            
    def installEffect(self, img, initial_pos, terminate_pos):
        self.effects.append(Effect(img, initial_pos=initial_pos, terminate_pos=terminate_pos))
        

class Effect():
    def __init__(self, img, initial_pos, terminate_pos, lifetime=10):
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

		#draw button on screen
        surface.blit(self.img, (self.pos_x, self.pos_y))
        
        if (self.time == self.lifetime):
            self.terminate = True

    def isTerminate(self):
        return self.terminate
    
