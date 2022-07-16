import pygame
from raiseable import RaiseableItem
from settings import ObjectType, item_range, ChestStatus
from support import import_cut_graphicks
from random import choice

class Chest(pygame.sprite.Sprite):
    def __init__(self, groups, pos, type) -> None:
        super().__init__(groups)
        self.object_type = ObjectType.chest
        self.status = ChestStatus.closed
        self.image_list = import_cut_graphicks(f'graphics/chests/{type}.png', (88, 62))
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(center = pos)
        self.gun_index = choice(item_range[type])
        self.hitbox = self.rect.copy().inflate(0, -30)
    
    def open(self, gameplay):
        if self.status == ChestStatus.opened: return
        self.status = ChestStatus.opened
        self.image = self.image_list[1]
        pos_x, pos_y = self.hitbox.center
        RaiseableItem(gameplay.items, (pos_x, pos_y - 30), self.gun_index)
        