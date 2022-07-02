import pygame
from support import import_cut_graphicks
from math import sin, cos

class Particles(pygame.sprite.Sprite):
    def __init__(self, groups, angle, speed, color, pos) -> None:
        super().__init__(groups)

        self.life_time = 200
        self.time_of_born = pygame.time.get_ticks()

        self.image = pygame.Surface((5, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect(center = pos)
        
        self.direction = pygame.Vector2(cos(angle), -sin(angle))
        self.speed = speed
    
    def death(self):
        if pygame.time.get_ticks() - self.time_of_born > self.life_time:
            self.kill()
    
    def move(self):
        self.rect.center += self.direction*self.speed  
  
    def update(self):
        self.death()
        self.move()

class StaticParticle(pygame.sprite.Sprite):
    def __init__(self, groups, path, pos, size) -> None:
        super().__init__(groups)
        self.graphics = import_cut_graphicks(path, size)
        self.image = self.graphics[0]
        self.rect = self.image.get_rect(center = pos)
        self.animation_speed = 0.2
        self.animation_index = 0
    
    def animate(self):
        if self.animation_index > len(self.graphics)-1:
            self.kill()
        self.animation_index += self.animation_speed
        self.image = self.graphics[int(self.animation_index)]

    
    def update(self) -> None:
        self.animate()