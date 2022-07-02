import pygame
from settings import ItemType
from random import randint

class Modifier:
    def __init__(self) -> None:
        self.image_origin = pygame.Surface((30, 30))
        self.image_origin.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
        self.item_type = ItemType.modifier
        self.dmg_boost = randint(1, 5)