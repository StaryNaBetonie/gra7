from settings import Status
from import_item import import_item, import_items

class Inventory:
    def __init__(self) -> None:
        self.space = [import_item(Status.player, 8)]
    
    def all_weapons(self):
        self.space = import_items(Status.player, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 19, 20])
# import_items(Status.player, [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 18])
# import_item(Status.player, 8)