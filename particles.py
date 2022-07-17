import pygame
from settings import ObjectType
from support import get_surface, import_cut_graphicks
from math import sin, cos
from tile import Tile

class Particles(Tile):
    def __init__(self, groups, angle, speed, color, pos) -> None:
        super().__init__(groups, pos, get_surface((5, 5), color), ObjectType.wall, 2)

        self.life_time = 200
        self.time_of_born = pygame.time.get_ticks()
        
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

class StaticParticle(Tile):
    def __init__(self, groups, path, pos, size) -> None:
        self.graphics = import_cut_graphicks(path, size)
        super().__init__(groups, pos, self.graphics[0], ObjectType.wall, 2)
        self.rect.center = pos
        self.animation_speed = 0.2
        self.animation_index = 0
    
    def animate(self):
        if self.animation_index > len(self.graphics) - 1: self.kill()
        self.animation_index += self.animation_speed
        self.image = self.graphics[int(self.animation_index)]

    def update(self) -> None:
        self.animate()