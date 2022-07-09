import pygame
from settings import Border, RoomType, TILE_SIZE, weapon_names
from tile import Tile
from random import choice, randint
from raiseable import RaiseableItem

class Room:
    def __init__(self, level, index, room_type, walls, status=True, active=False) -> None:
        self.room_type = room_type
        self.walls = walls

        self.active = active
        
        self.level = level

        self.place = pygame.math.Vector2(index)
        self.status = status
        self.border = []
    
    def import_room(self, groups, floor_graphic):
        self.floor = Tile(groups['floor'], self.place*15*TILE_SIZE, floor_graphic)
        for style, layout in self.level.items():
            for row_index , row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = self.place.x * 15*TILE_SIZE + col_index * TILE_SIZE
                        y = self.place.y * 15*TILE_SIZE + row_index * TILE_SIZE

                        if style == 'walls':
                            Tile([groups['visible'], groups['walls']], (x, y), self.walls[int(col)])
                        if style == 'item':
                            index = choice(weapon_names)
                            RaiseableItem([groups['visible'], groups['items']], (x+TILE_SIZE/2, y+TILE_SIZE/2), index)

    def set_active(self, player):
        player_place = (int(player.x/15/TILE_SIZE), int(player.y/15/TILE_SIZE))
        if player_place == self.place:
            self.active = True
    
    def add_border(self, groups):
        x = self.place.x * 15*TILE_SIZE
        y = self.place.y * 15*TILE_SIZE
        for border in self.border:
            if border == Border.top:
                index_list = [1, 2]
                Tile(groups, (x+7*TILE_SIZE, y), self.walls[choice(index_list)])
                for i in range(1, 5):
                    Tile(groups, (x +(7-i)*TILE_SIZE, y), self.walls[choice(index_list)])
                    Tile(groups, (x +(7+i)*TILE_SIZE, y), self.walls[choice(index_list)])
                
            if border == Border.bottom:
                index_list = [13, 14]
                Tile(groups, (x+7*TILE_SIZE, y+14*TILE_SIZE), self.walls[choice(index_list)])
                for i in range(1, 5):
                    Tile(groups, (x +(7-i)*TILE_SIZE, y+14*TILE_SIZE), self.walls[choice(index_list)])
                    Tile(groups, (x +(7+i)*TILE_SIZE, y+14*TILE_SIZE), self.walls[choice(index_list)])

            if border == Border.left:
                index_list = [4, 8]
                Tile(groups, (x, y+7*TILE_SIZE), self.walls[choice(index_list)])
                for i in range(1, 5):
                    Tile(groups, (x, y+(7-i)*TILE_SIZE), self.walls[choice(index_list)])
                    Tile(groups, (x, y+(7+i)*TILE_SIZE), self.walls[choice(index_list)])

            if border == Border.right:
                index_list = [7, 11]
                Tile(groups, (x+14*TILE_SIZE, y+7*TILE_SIZE), self.walls[choice(index_list)])
                for i in range(1, 5):
                    Tile(groups, (x+14*TILE_SIZE, y+(7-i)*TILE_SIZE), self.walls[choice(index_list)])
                    Tile(groups, (x+14*TILE_SIZE, y+(7+i)*TILE_SIZE), self.walls[choice(index_list)])

        
        if not self.room_type == RoomType.boss:
            if not Border.bottom in self.border:
                Tile(groups, (x+3*TILE_SIZE, y+14*TILE_SIZE), self.walls[6])
                Tile(groups, (x+11*TILE_SIZE, y+14*TILE_SIZE), self.walls[5])
            if not Border.left in self.border:
                Tile(groups, (x, y+3*TILE_SIZE), self.walls[10])
                Tile(groups, (x, y+11*TILE_SIZE), self.walls[6])
            if not Border.right in self.border:
                Tile(groups, (x+14*TILE_SIZE, y+3*TILE_SIZE), self.walls[9])
                Tile(groups, (x+14*TILE_SIZE, y+11*TILE_SIZE), self.walls[5])
            if not Border.top in self.border:
                Tile(groups, (x+3*TILE_SIZE, y), self.walls[10])
                Tile(groups, (x+11*TILE_SIZE, y), self.walls[9])
            
    def delete_room(self):
        for row in self.tiles:
            for col in row:
                if col != None:
                    col.kill()
                
class MainRooms(Room):
    def set_player(self, level):
        for row_index , row in enumerate(level):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = self.place.x * 15*TILE_SIZE + col_index * TILE_SIZE
                    y = self.place.y * 15*TILE_SIZE + row_index * TILE_SIZE

                    return (x, y)

class BossRoom:
    def __init__(self, level, index, walls) -> None:
        self.active = False
        self.status = False
        self.room_type = RoomType.boss
        self.place = pygame.math.Vector2(index)
        self.corridor = Room(level[0], index, self.room_type, walls, False)
        self.botleft = Room(level[1], (index[0], index[1]-1), self.room_type, walls, False)
        self.botright = Room(level[2], (index[0]+1, index[1]-1), self.room_type, walls, False)
        self.topleft = Room(level[3], (index[0], index[1]-2), self.room_type, walls, False)
        self.topright = Room(level[4], (index[0]+1, index[1]-2), self.room_type, walls, False)
    
    def set_active(self, player):
        player_place = (int(player.x/15/TILE_SIZE), int(player.y/15/TILE_SIZE))
        if player_place == self.botleft.place:
            self.active = True
        
    def import_room(self, groups, floor_graphic):
        self.corridor.import_room(groups, floor_graphic)
        self.botleft.import_room(groups, floor_graphic)
        self.botright.import_room(groups, floor_graphic)
        self.topleft.import_room(groups, floor_graphic)
        self.topright.import_room(groups, floor_graphic)