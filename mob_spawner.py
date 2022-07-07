from random import randint, choice
from enemy import Enemy, Boss, Worm
from settings import TILE_SIZE, RoomType, Status, opponents, bosses
from import_item import import_item, import_items

class MobSpawner:
    def __init__(self, gamestate, groups, stage_number) -> None:
        self.gamestate = gamestate
        self.groups = groups
        self.stage_number = stage_number
    
    def spawn(self, opponents_index: list[int], bosses_index: list[int]) -> None:
        for g_row in self.gamestate:
            for g_col in g_row:
                if g_col is not None:
                    if g_col.room_type == RoomType.normal:
                        for i in range(2, 12):
                            for j in range(2, 12):
                                if randint(0, 40) == 0:
                                    x = g_col.place.x * 15 * TILE_SIZE + j * TILE_SIZE
                                    y = g_col.place.y * 15 * TILE_SIZE + i * TILE_SIZE

                                    enemy_data = opponents[choice(opponents_index)]

                                    gun = import_item(Status.enemy, enemy_data['weapon'])
                                    Enemy(self.groups, (x, y), gun, enemy_data)
                                    
                    if g_col.room_type == RoomType.boss:
                        x = g_col.topright.place.x * 15 * TILE_SIZE + 7 * TILE_SIZE
                        y = g_col.topright.place.y * 15 * TILE_SIZE + 7 * TILE_SIZE
                        boss = bosses[choice(bosses_index)]
                        guns = import_items(Status.enemy, boss['weapons'])
                        self.boss = Worm(self.groups, (x, y), guns, boss)
