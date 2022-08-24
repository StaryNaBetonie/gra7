from email.mime import image
import pygame
from chest import Chest
from settings import Border, ObjectType, RoomType, TILE_SIZE
from tile import Tile
from random import choice, randint
from support import add_tile, generage_shadow

class Room:
    def __init__(self, level, index, room_type, walls, status=True, active=False) -> None:
        self.room_type = room_type
        self.walls = walls
        self.floor_surface = pygame.Surface((15 * TILE_SIZE, 15 * TILE_SIZE))

        self.active = active
        
        self.level = level

        self.place = pygame.math.Vector2(index)
        self.center = pygame.Vector2(TILE_SIZE * (self.place.x * 15 + 7.5), TILE_SIZE * (self.place.y * 15 + 7.5))
        self.status = status
        self.border = []

    def import_floor(self, gameplay):
        floor_x, floor_y = self.place * 15 * TILE_SIZE
        return Tile([gameplay.visible_sprites, gameplay.floor], self.floor_surface, ObjectType.wall, -2, (0, 0), topleft = (floor_x, floor_y))
    
    def random_chest_type(self):
        random_number = randint(1, 100)
        if random_number in range(1, 50): return 'wooden'
        elif random_number in range(51, 75): return 'sea_prism'
        elif random_number in range(76, 88): return 'golden'
        return 'nigger'

    def import_room(self, gameplay, floor_graphics):
        if self.room_type is RoomType.chest:
            groups = [gameplay.visible_sprites, gameplay.chests, gameplay.walls]
            Chest(groups, self.center, self.random_chest_type())
        for style, layout in self.level.items():
            for row_index , row in enumerate(layout):
                for col_index, col in enumerate(row):
                    index = int(col)
                    if col != '-1':
                        x = self.place.x * 15*TILE_SIZE + col_index * TILE_SIZE
                        y = self.place.y * 15*TILE_SIZE + row_index * TILE_SIZE

                        if style == 'walls':
                            if index in [1, 2, 9, 10]:
                                self.add_top_tile([gameplay.visible_sprites, gameplay.walls], (x, y), self.walls[index])
                            else:
                                Tile([gameplay.visible_sprites, gameplay.walls], self.walls[index], ObjectType.wall, 0, (0, -10), topleft = (x, y))
                        
                        elif style == 'floor':
                            if index == 5:
                                index_list = [5, 6, 9, 10]
                                floor_part_image = floor_graphics[choice(index_list)]
                            else:
                                floor_part_image = floor_graphics[index]
                            self.floor_surface.blit(floor_part_image, (col_index * TILE_SIZE, row_index * TILE_SIZE))

    def set_active(self, player):
        player_place = (int(player.x/15/TILE_SIZE), int(player.y/15/TILE_SIZE))
        if player_place == self.place:
            self.active = True
    
    def add_top_tile(self, groups, pos, image):
        add_tile(groups, pos, image)
        x_place, y_place = pos
        Tile(groups, generage_shadow(2.5), ObjectType.shadow, -1, (-64, -41), topleft = (x_place, y_place + TILE_SIZE))
        
    def add_border(self, groups, floor_graphics):
        x = self.place.x * 15*TILE_SIZE
        y = self.place.y * 15*TILE_SIZE
        for border in self.border:
            if border == Border.top:
                index_list = [1, 2]
                self.add_top_tile(groups, (x+7 * TILE_SIZE, y), self.walls[choice(index_list)])
                self.floor_surface.blit(floor_graphics[choice(index_list)],(7 * TILE_SIZE, TILE_SIZE))
                for i in range(1, 5):
                    self.add_top_tile(groups, (x + (7 - i) * TILE_SIZE, y), self.walls[choice(index_list)])
                    self.add_top_tile(groups, (x + (7 + i) * TILE_SIZE, y), self.walls[choice(index_list)])
                    if i != 4:
                        self.floor_surface.blit(floor_graphics[choice(index_list)],((7 + i) * TILE_SIZE , TILE_SIZE))
                        self.floor_surface.blit(floor_graphics[choice(index_list)],((7 - i) * TILE_SIZE , TILE_SIZE))
                
            if border == Border.bottom:
                index_list = [13, 14]
                add_tile(groups, (x+7 * TILE_SIZE, y+14*TILE_SIZE), self.walls[choice(index_list)])
                self.floor_surface.blit(floor_graphics[choice(index_list)],(7 * TILE_SIZE, 13*TILE_SIZE))
                for i in range(1, 5):
                    add_tile(groups, (x +(7-i)*TILE_SIZE, y+14*TILE_SIZE), self.walls[choice(index_list)])
                    add_tile(groups, (x +(7+i)*TILE_SIZE, y+14*TILE_SIZE), self.walls[choice(index_list)])
                    if i != 4:
                        self.floor_surface.blit(floor_graphics[choice(index_list)],((7 - i) * TILE_SIZE, 13*TILE_SIZE))
                        self.floor_surface.blit(floor_graphics[choice(index_list)],((7 + i) * TILE_SIZE, 13*TILE_SIZE))

            if border == Border.left:
                index_list = [4, 8]
                add_tile(groups, (x, y+7*TILE_SIZE), self.walls[choice(index_list)])
                self.floor_surface.blit(floor_graphics[choice(index_list)],(TILE_SIZE, 7 * TILE_SIZE))
                for i in range(1, 5):
                    add_tile(groups, (x, y+(7-i)*TILE_SIZE), self.walls[choice(index_list)])
                    add_tile(groups, (x, y+(7+i)*TILE_SIZE), self.walls[choice(index_list)])
                    if i != 4:
                        self.floor_surface.blit(floor_graphics[choice(index_list)],(TILE_SIZE, (7 + i) * TILE_SIZE))
                        self.floor_surface.blit(floor_graphics[choice(index_list)],(TILE_SIZE, (7 - i) * TILE_SIZE))

            if border == Border.right:
                index_list = [7, 11]
                add_tile(groups, (x+14*TILE_SIZE, y+7*TILE_SIZE), self.walls[choice(index_list)])
                self.floor_surface.blit(floor_graphics[choice(index_list)],(13*TILE_SIZE, 7 * TILE_SIZE))
                for i in range(1, 5):
                    add_tile(groups, (x+14*TILE_SIZE, y+(7-i)*TILE_SIZE), self.walls[choice(index_list)])
                    add_tile(groups, (x+14*TILE_SIZE, y+(7+i)*TILE_SIZE), self.walls[choice(index_list)])
                    if i != 4:
                        self.floor_surface.blit(floor_graphics[choice(index_list)],(13*TILE_SIZE, (7 + i) * TILE_SIZE))
                        self.floor_surface.blit(floor_graphics[choice(index_list)],(13*TILE_SIZE, (7 - i) * TILE_SIZE))

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
        self.center = self.botright.place * 15
    
    def set_active(self, player):
        player_place = (int(player.x/15/TILE_SIZE), int(player.y/15/TILE_SIZE))
        if player_place == self.botleft.place:
            self.active = True
    
    def import_floor(self, gameplay):
        self.corridor.import_floor(gameplay)
        self.botleft.import_floor(gameplay)
        self.botright.import_floor(gameplay)
        self.topleft.import_floor(gameplay)
        self.topright.import_floor(gameplay)
        
    def import_room(self, groups, floor_graphic):
        self.corridor.import_room(groups, floor_graphic)
        self.botleft.import_room(groups, floor_graphic)
        self.botright.import_room(groups, floor_graphic)
        self.topleft.import_room(groups, floor_graphic)
        self.topright.import_room(groups, floor_graphic)