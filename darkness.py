import pygame
from bullet import Bullet

class Darkness:
    def __init__(self, gameplay) -> None:
        self.gameplay = gameplay
        self.player = gameplay.player
        self.light_sources = []

        self.surface = pygame.Surface((1920, 1080))
        rect = pygame.Rect(2000, 0, 50, 50)
        pygame.draw.rect(self.surface, ('white'), rect)

    def render(self, window):
        self.surface.fill('black')
        self.dynamic_light(self.gameplay.bullets.sprites())
        self.render_light(self.player.pos_on_screen, 200)
        self.correct()
        window.blit(self.surface, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
    
    def render_light(self, center, rad):
        color = 0
        speed = 15
        for i in range(255//speed, 0, -1):
            color += speed
            pygame.draw.circle(self.surface, (color, color, color), center, rad + i)
    
    def correct(self):
        pygame.draw.circle(self.surface, 'white', self.player.pos_on_screen, 200)
        for source in self.light_sources:
            pygame.draw.circle(self.surface, 'white', source[0], source[1])

    def dynamic_light(self, bullets: list[Bullet]):
        self.light_sources = []
        for bullet in bullets:
            self.light_sources.append((bullet.pos_on_screen, bullet.light_rad))
            self.render_light(bullet.pos_on_screen, bullet.light_rad)
