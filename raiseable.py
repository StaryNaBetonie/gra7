from settings import ObjectType, Status
from import_item import import_item
from tile import Tile

class RaiseableItem(Tile):
    def __init__(self, groups, pos, item_index=None) -> None:
        self.item = import_item(Status.player, item_index)
        super().__init__(groups, pos, self.item.image_origin.copy(), ObjectType.raisable, 1, (0, 0))
        self.hitbox.center = self.rect.center = pos
        self.item_type = self.item.item_type
