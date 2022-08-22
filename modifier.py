import pygame
from settings import ItemType
from random import randint
from support import import_graphics

class Modifier:
    def __init__(self) -> None:
        self.image_origin = import_graphics('graphics/chests/damage_up.png')
        self.item_type = ItemType.modifier
        self.dmg_boost = randint(1, 5)