from settings import ObjectType, Status, ItemType
from import_item import import_item
from tile import Tile

class RaiseableItem(Tile):
    def __init__(self, groups, pos, item_index=None) -> None:
        self.item = import_item(Status.player, item_index)
        super().__init__(groups, self.item.image_origin.copy(), ObjectType.raisable, self.get_layer(), (0, 0), center = pos)
        self.item_type = self.item.item_type
    
    def get_layer(self):
        return -1 if self.item.item_type == ItemType.modifier else 1
