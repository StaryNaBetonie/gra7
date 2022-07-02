import pygame
from random import randint, choice
from room import Room, MainRooms, BossRoom
from settings import RoomType, Border, TILE_SIZE
from mob_spawner import MobSpawner
from tile import Tile
from raiseable import RaiseableItem
from support import import_cut_graphicks, import_csv_layout

class Gamestate:
    def __init__(self, stage_number: int, state_data: dict, **groups: dict) -> None:
    
        self.walls = pygame.sprite.Group()
        self.groups = groups
        self.groups['walls'] = self.walls
        self.name = state_data['name']

        path = f'graphics/levels/{self.name}/'
        self.walls_graphics = import_cut_graphicks(path+'walls.jpg', (TILE_SIZE, TILE_SIZE))
        self.floor_graphics = pygame.image.load(path+'floor.jpg')
        self._import_levels(self.name)
        self.key_color = state_data['key_color']
        
        self.stage_number = stage_number
        self.gamestate = [[None]*15 for i in range(15)]
        self.gamestate[7][7] = MainRooms(self._enter, (7, 7), RoomType._enter, self.walls_graphics)
        self.add_map()
        self.add_border()
        self.add_special_room(3, self._exit, RoomType._exit)
        self.add_special_room(3, self._chest, RoomType.chest)
        self.add_special_room(3, self._chest, RoomType.chest)
        self.import_rooms()
        
        self.mob_spawner = MobSpawner(self.gamestate, [self.groups['visible'], self.groups['enemies']], self.stage_number)
    
    def _import_levels(self, state_type: str) -> None:
        path = f'levels/{state_type}/'
        self._exit = {'walls': import_csv_layout(path+'exit_walls.csv'),
                'exit': import_csv_layout(path+'exit_exit.csv')}

        self._enter = {
            'walls': import_csv_layout(path+'enter_walls.csv'),
            'player': import_csv_layout(path+'enter_player.csv')
        }

        self._chest = {
            'walls': import_csv_layout(path+'chest_room.csv'),
            'item': import_csv_layout(path+'chest_item.csv')
            }

        self.boss_room = [
            {'walls': import_csv_layout(path+'corridor.csv')},
            {'walls': import_csv_layout(path+'boss_room_botleft.csv')},
            {'walls': import_csv_layout(path+'boss_room_botright.csv')},
            {'walls': import_csv_layout(path+'boss_room_topleft.csv')},
            {'walls': import_csv_layout(path+'boss_room_topright.csv')}
        ]

        self.levels = [
            {'walls': import_csv_layout(path+'map1.csv')},
            {'walls': import_csv_layout(path+'map2.csv')},
            {'walls': import_csv_layout(path+'map3.csv')},
            {'walls': import_csv_layout(path+'map4.csv')},
            {'walls': import_csv_layout(path+'map5.csv')},
            {'walls': import_csv_layout(path+'map6.csv')}
        ]
    
    def kill_boss(self, groups):
        if self.mob_spawner.boss is not None:
            if self.mob_spawner.boss.hp <= 0:
                RaiseableItem(groups, self.mob_spawner.boss.rect.center)
                self.mob_spawner.boss = None


    def get_the_highest_room(self, rooms):
        _min = rooms[0]
        for room in rooms:
            if room.place.y < _min.place.y:
                _min = room
        return _min

    def add_boss_room(self):
        potentially_good_rooms = []
        for row in self.gamestate:
            for room in row:
                if room is not None:
                    if Border.top in room.border:
                        potentially_good_rooms.append(room)
        right_room = self.get_the_highest_room(potentially_good_rooms)
        x = int(right_room.place.x)
        y = int(right_room.place.y)

        self.gamestate[x][y-1] = BossRoom(self.boss_room, (x, y-1), self.walls_graphics)

    def add_map(self):
        _sum = 0
        for i in range(3):
            _sum += self.add_points()
        
        while _sum < 6:
            _sum = 0
            for i in range(3):
                _sum += self.add_points()

    def set_player(self):
        return self.gamestate[7][7].set_player(self._enter['player'])
    
    def add_point(self, x, y, gamestate):
        n = 0
        if randint(1, 3) == 1:
            n += 1
            if self.gamestate[x][y] is None:
                gamestate[x][y] = Room(choice(self.levels), (x, y), RoomType.normal, self.walls_graphics)
        return n
    
    def add_points(self):
        new_gamestate = self.gamestate.copy()
        n = 0

        for row_index, row in enumerate(self.gamestate):
            for col_index, col in enumerate(row):
                if col is not None:
                    if col.status is True:
                        if col.room_type is not RoomType._enter:
                            col.status = False
                        if row_index is not 0:
                            n += self.add_point(row_index-1, col_index, new_gamestate)
                        if row_index is not 13:
                            n += self.add_point(row_index+1, col_index, new_gamestate)
                        if col_index is not 0:
                            n += self.add_point(row_index, col_index-1, new_gamestate)
                        if col_index is not 12:
                            n += self.add_point(row_index, col_index+1, new_gamestate)
        self.gamestate = new_gamestate
        return n

    def add_special_room(self, number, level, type):
        rooms = []
        for row in self.gamestate:
            for col in row:
                if col is not None and col.room_type == RoomType.normal:
                    if len(col.border) == number:
                        if col.room_type != self._enter:
                            rooms.append(col)
        if len(rooms) == 0:
            self.add_special_room(number-1, level, type)
        else:
            room = rooms[randint(0, len(rooms)-1)]
            if type == RoomType._exit:
                self.gamestate[int(room.place.x)][int(room.place.y)] = MainRooms(level, room.place, type, self.walls_graphics, False)
            else:
                self.gamestate[int(room.place.x)][int(room.place.y)] = Room(level, room.place, type, self.walls_graphics, False)


    def add_border(self):
        for row_index, row in enumerate(self.gamestate):
            for col_index, col in enumerate(row):
                if col is not None:
                    tab = []
                    
                    if col.place.y == 0:
                        tab.append(Border.top)
                    elif self.gamestate[row_index][col_index-1] is None:
                        tab.append(Border.top)

                    if col.place.y == len(self.gamestate)-1:
                        tab.append(Border.bottom)
                    elif self.gamestate[row_index][col_index+1] is None:
                        tab.append(Border.bottom)

                    if col.place.x == 0:
                        tab.append(Border.left)
                    elif self.gamestate[row_index-1][col_index] is None:
                        tab.append(Border.left)

                    if col.place.x == len(self.gamestate)-1:
                        tab.append(Border.right)
                    elif self.gamestate[row_index+1][col_index] is None:
                        tab.append(Border.right)

                    col.border = tab
    
    def import_rooms(self):
        self.add_border()
        self.add_boss_room()
        self.add_border()

        for row in self.gamestate:
            for col in row:
                if col is not None:
                    if not col.room_type == RoomType.boss:
                        col.add_border([self.groups['visible'], self.groups['walls']])
                    col.room = col.import_room(self.groups, self.floor_graphics)
                    if col.room_type == RoomType._exit:
                        self.exit = Tile([self.groups['visible']], col.set_player(self._exit['exit']), pygame.image.load('graphics/stairs.jpg'))

    
    def update(self, player):
        for row in self.gamestate:
            for col in row:
                if col is not None:
                    col.set_active(player)
    
    def delete_gamestate(self):
        self.exit.kill()
        for wall in self.walls:
            wall.kill()
