import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surface, object_type, layer, hitbox_offset = (0, -10)) -> None:
        super().__init__(groups)
        self._layer = layer
        self.object_type = object_type
        self.place_in_net = []
    
        self.image_origin = surface
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.copy().inflate(hitbox_offset)