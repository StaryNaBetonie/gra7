import pygame
from chest import Chest
from settings import Border, ObjectType, RoomType, TILE_SIZE
from tile import Tile
from random import choice, randint
from support import add_tile

class Room:
    def __init__(self, level, index, room_type, walls, status=True, active=False) -> None:
        self.room_type = room_type
        self.walls = walls
        self.shadow = pygame.image.load('graphics/levels/dungeon/shadow.png')
        self.shadow.set_alpha(100)

        self.active = active
        
        self.level = level

        self.place = pygame.math.Vector2(index)
        self.status = status
        self.border = []

    def import_floor(self, gameplay, floor_graphic):
        floor = floor_graphic
        if Border.bottom in self.border:
            new_floor = pygame.Surface((15 * TILE_SIZE, 15 * TILE_SIZE - 20))
            new_floor.blit(floor, (0, 0))
            floor = new_floor
        floor_x, floor_y = self.place * 15 * TILE_SIZE
        return Tile([gameplay.visible_sprites, gameplay.floor], floor, ObjectType.wall, -2, (0, 0), topleft = (floor_x, floor_y + 20))
    
    def random_chest_type(self):
        random_number = randint(1, 100)
        print('nigger')
        if random_number in range(1, 50): return 'wooden'
        elif random_number in range(51, 75): return 'sea_prism'
        elif random_number in range(76, 88): return 'golden'
        return 'nigger'

    def import_room(self, gameplay, floor_graphic):
        self.floor = self.import_floor(gameplay, floor_graphic)
        for style, layout in self.level.items():
            for row_index , row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = self.place.x * 15*TILE_SIZE + col_index * TILE_SIZE
                        y = self.place.y * 15*TILE_SIZE + row_index * TILE_SIZE

                        if style == 'walls':
                            if int(col) in [1, 2, 9, 10]:
                                self.add_top_tile([gameplay.visible_sprites, gameplay.walls], (x, y), self.walls[int(col)])
                            else:
                                Tile([gameplay.visible_sprites, gameplay.walls], self.walls[int(col)], ObjectType.wall, 0, (0, -10), topleft = (x, y))
                        elif style == 'item':
                            groups = [gameplay.visible_sprites, gameplay.chests, gameplay.walls]
                            Chest(groups, (x+TILE_SIZE/2, y+TILE_SIZE/2), self.random_chest_type())

    def set_active(self, player):
        player_place = (int(player.x/15/TILE_SIZE), int(player.y/15/TILE_SIZE))
        if player_place == self.place:
            self.active = True
    
    def add_top_tile(self, groups, pos, image):
        add_tile(groups, pos, image)
        x_place, y_place = pos
        Tile(groups, self.shadow, ObjectType.wall, -1, (-32, -20), topleft = (x_place, y_place + TILE_SIZE))
        
    def add_border(self, groups):
        x = self.place.x * 15*TILE_SIZE
        y = self.place.y * 15*TILE_SIZE
        for border in self.border:
            if border == Border.top:
                index_list = [1, 2]
                self.add_top_tile(groups, (x+7*TILE_SIZE, y), self.walls[choice(index_list)])
                for i in range(1, 5):
                    self.add_top_tile(groups, (x + (7 - i) * TILE_SIZE, y), self.walls[choice(index_list)])
                    self.add_top_tile(groups, (x + (7 + i) * TILE_SIZE, y), self.walls[choice(index_list)])
                
            if border == Border.bottom:
                index_list = [13, 14]
                add_tile(groups, (x+7*TILE_SIZE, y+14*TILE_SIZE), self.walls[choice(index_list)])
                for i in range(1, 5):
                    add_tile(groups, (x +(7-i)*TILE_SIZE, y+14*TILE_SIZE), self.walls[choice(index_list)])
                    add_tile(groups, (x +(7+i)*TILE_SIZE, y+14*TILE_SIZE), self.walls[choice(index_list)])

            if border == Border.left:
                index_list = [4, 8]
                add_tile(groups, (x, y+7*TILE_SIZE), self.walls[choice(index_list)])
                for i in range(1, 5):
                    add_tile(groups, (x, y+(7-i)*TILE_SIZE), self.walls[choice(index_list)])
                    add_tile(groups, (x, y+(7+i)*TILE_SIZE), self.walls[choice(index_list)])

            if border == Border.right:
                index_list = [7, 11]
                add_tile(groups, (x+14*TILE_SIZE, y+7*TILE_SIZE), self.walls[choice(index_list)])
                for i in range(1, 5):
                    add_tile(groups, (x+14*TILE_SIZE, y+(7-i)*TILE_SIZE), self.walls[choice(index_list)])
                    add_tile(groups, (x+14*TILE_SIZE, y+(7+i)*TILE_SIZE), self.walls[choice(index_list)])

        
        if self.room_type is not RoomType.boss:
            if not Border.bottom in self.border:
                add_tile(groups, (x+3*TILE_SIZE, y+14*TILE_SIZE), self.walls[6])
                add_tile(groups, (x+11*TILE_SIZE, y+14*TILE_SIZE), self.walls[5])
            if not Border.left in self.border:
                self.add_top_tile(groups, (x, y+3*TILE_SIZE), self.walls[10])
                add_tile(groups, (x, y+11*TILE_SIZE), self.walls[6])
            if not Border.right in self.border:
                self.add_top_tile(groups, (x+14*TILE_SIZE, y+3*TILE_SIZE), self.walls[9])
                add_tile(groups, (x+14*TILE_SIZE, y+11*TILE_SIZE), self.walls[5])
            if not Border.top in self.border:
                self.add_top_tile(groups, (x+3*TILE_SIZE, y), self.walls[10])
                self.add_top_tile(groups, (x+11*TILE_SIZE, y), self.walls[9])
            
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
        self.botright.border.append(Border.bottom)
        self.corridor.import_room(groups, floor_graphic)
        self.botleft.import_room(groups, floor_graphic)
        self.botright.import_room(groups, floor_graphic)
        self.topleft.import_room(groups, floor_graphic)
        self.topright.import_room(groups, floor_graphic)