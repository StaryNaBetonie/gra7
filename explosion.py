import pygame
from particles import StaticParticle

class Explosion:
    def __init__(self, groups: list[pygame.sprite.Group], pos: tuple, opponents: list, damage: int) -> None:
        self.animation = StaticParticle(groups, 'graphics/effects/big-explosion.png', pos, (128, 128))
        self.radius = 200
        self.damage = damage
        self.pos = pos
        self.knock(opponents)

    def knock(self, opponents):
        for opponent in opponents:
            _magnitude = pygame.Vector2(opponent.hitbox.centerx - self.pos[0], opponent.hitbox.centery - self.pos[1]).magnitude()
            if _magnitude <= self.radius:
                opponent.hp -= self.damage
                if opponent.can_knock:
                    opponent.direction = pygame.Vector2((opponent.hitbox.centerx-self.pos[0])/_magnitude, (opponent.hitbox.centery-self.pos[1])/_magnitude)
                    opponent.acceleration = -1
                    opponent.speed = 20