import pygame
from support2 import get_rect
from settings import ObjectType

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, surface, object_type, layer, hitbox_offset, **pos) -> None:
        super().__init__(groups)
        self._layer = layer
        self.object_type = object_type
        self.place_in_net = []
    
        self.image_origin = surface
        self.image = surface
        self.rect = get_rect(self.image, pos)
        self.hitbox = self.rect.copy().inflate(hitbox_offset)

        self.special_flag = self.get_special_flag()
    
    def get_special_flag(self):
        return pygame.BLEND_RGBA_MULT if self.object_type is ObjectType.shadow else 0
