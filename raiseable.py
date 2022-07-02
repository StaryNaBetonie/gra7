import pygame
from settings import ObjectType, Status
from import_item import import_item

class RaiseableItem(pygame.sprite.Sprite):
    def __init__(self, groups, pos, item_index=None) -> None:
        super().__init__(groups)
        self.object_type = ObjectType.raisable
        self.can_move = False
        self.place_in_net = []
        self.item = import_item(Status.player, item_index)
        self.item_type = self.item.item_type
        self.image = self.item.image_origin.copy()
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect