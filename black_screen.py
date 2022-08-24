import pygame

class BlackScreen:
    def __init__(self):
        self.image = pygame.Surface((1920, 1080))
        self.color = 255
        self.speed = -5
    
    def play(self, window, new_gamsetate, player):
        self.color += self.speed
        if self.color <= 0:
            self.color = 0
            player.direction.y = 0
            self.speed *= -1
            new_gamsetate()
        elif self.color > 255:
            self.color = 255
            self.speed *= -1
            player.moving_down = False

        self.image.fill((self.color, self.color, self.color))
        window.blit(self.image, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)