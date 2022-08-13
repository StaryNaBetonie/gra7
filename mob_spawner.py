from random import randint, choice
from enemy import Enemy, Boss, Worm
from settings import TILE_SIZE, RoomType, Status, opponents, bosses
from import_item import import_item, import_items
from support import get_surface, import_graphics

class MobSpawner:
    def __init__(self, gamestate, stage_number) -> None:
        self.gamestate = gamestate
        self.groups = [gamestate.gameplay.enemies, gamestate.gameplay.visible_sprites]
        self.stage_number = stage_number
    
    def spawn(self, opponents_index: list[int], boss_index: int) -> None:
        for g_row in self.gamestate.gamestate:
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
                                    image = get_surface(enemy_data['size'], enemy_data['color'])
                                    Enemy(self.groups, (x, y), gun, enemy_data, image)
                                    
                    if g_col.room_type == RoomType.boss:
                        x = g_col.topright.center.x
                        y = g_col.topright.center.y
                        if boss_index == 3:
                            x = g_col.center.x * TILE_SIZE
                            y = g_col.center.y * TILE_SIZE
                        boss = bosses[boss_index]
                        guns = import_items(Status.enemy, boss['weapons'])
                        boss_name = boss['name']
                        image = import_graphics(f'graphics/bosses/{boss_name}.png')
                        self.boss = Boss(self.groups, (x, y), guns, boss, image)
