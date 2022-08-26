import pygame
from support2 import get_rect, generate_shadow
from settings import ObjectType

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, surface, object_type, layer, hitbox_offset, **pos) -> None:
        super().__init__(groups)
        self._layer = layer
        self.object_type = object_type
        self.place_in_grid = []
    
        self.image_origin = surface
        self.image = surface
        self.rect = get_rect(self.image, pos)
        self.hitbox = self.rect.copy().inflate(hitbox_offset)

        self.special_flag = 0
    
class Shadow(Tile):
    def __init__(self, groups, pos) -> None:
        super().__init__(groups, generate_shadow(2.5), ObjectType.shadow, -1, (0, 0), topleft = pos)
        self.hitbox = pygame.Rect(self.rect.topleft, (0, 0))
        self.special_flag = pygame.BLEND_RGBA_MULT
