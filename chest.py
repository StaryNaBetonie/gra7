import pygame
from raiseable import RaiseableItem
from settings import ObjectType, item_range, ChestStatus
from support import import_cut_graphicks
from random import choice
from tile import Tile

class Chest(Tile):
    def __init__(self, groups, pos, type) -> None:
        self.image_list = import_cut_graphicks(f'graphics/chests/{type}.png', (88, 62))
        super().__init__(groups, pos, self.image_list[0], ObjectType.chest, 0)
        self.rect.center = self.hitbox.center = pos
        self.status = ChestStatus.closed
        self.gun_index = choice(item_range[type])
    
    def open(self, gameplay):
        if self.status == ChestStatus.opened: return
        self.status = ChestStatus.opened
        self.image = self.image_list[1]
        pos_x, pos_y = self.hitbox.center
        RaiseableItem([gameplay.items, gameplay.visible_sprites], (pos_x, pos_y - 30), self.gun_index)
        