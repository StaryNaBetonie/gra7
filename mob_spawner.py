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
        for room_row in self.gamestate.gamestate:
            for room_col in room_row:
                if room_col is not None:
                    if room_col.room_type == RoomType.normal:
                        for row_index , row in enumerate(room_col.spawn_layer):
                            for col_index, col in enumerate(row):
                                if 'S' in col:
                                    if randint(0, 40) == 0:
                                        x = TILE_SIZE * (room_col.place.x * 15 + col_index + 0.5)
                                        y = TILE_SIZE * (room_col.place.y * 15 + row_index + 0.5)

                                        enemy_data = opponents[choice(opponents_index)]

                                        gun = import_item(Status.enemy, enemy_data['weapon'])
                                        image = get_surface(enemy_data['size'], enemy_data['color'])
                                        Enemy(self.groups, (x, y), gun, enemy_data, image)
                                    
                    if room_col.room_type == RoomType.boss:
                        x = room_col.topright.center.x
                        y = room_col.topright.center.y
                        if boss_index == 3:
                            x = room_col.center.x * TILE_SIZE
                            y = room_col.center.y * TILE_SIZE
                        boss = bosses[boss_index]
                        guns = import_items(Status.enemy, boss['weapons'])
                        boss_name = boss['name']
                        image = import_graphics(f'graphics/bosses/{boss_name}.png')
                        self.boss = Boss(self.groups, (x, y), guns, boss, image)
