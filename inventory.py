from settings import Status
from import_item import import_item, import_items

class Inventory:
    def __init__(self) -> None:
        self.index = 0
        self.space = [import_item(Status.player, 8)]
    
    def go_left(self):
        self.index = max(0, self.index - 1)
    
    def go_right(self):
        self.index = min(self.index + 1, len(self.space)-1)

    def add_item(self, item):
        self.space.append(item)
    
    def select_gun(self):
        return self.space[self.index]
    
    def all_weapons(self):
        self.index = 0
        self.space = import_items(Status.player, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 19, 20, 21])