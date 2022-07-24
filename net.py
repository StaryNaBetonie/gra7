import pygame
from settings import TILE_SIZE

class NetGroup:
    def __init__(self) -> None:
        self.net = self.new_net()
        self.cell_size = (TILE_SIZE*5)

    def new_net(self):
        net = []
        for i in range(45):
            net.append([])
            for j in range(45):
                net[i].append([])
        
        return net
    
    def clear(self):
        self.net = self.new_net()
    
    def add_object(self, object):
        left_index = object.hitbox.left//self.cell_size
        right_index = object.hitbox.right//self.cell_size
        top_index = object.hitbox.top//self.cell_size
        bot_index = object.hitbox.bottom//self.cell_size

        x_idexes_number = 1 + (right_index - left_index)
        y_idexes_number = 1 + (bot_index - top_index)

        object.place_in_net = []

        for x in range(x_idexes_number):
            for y in range(y_idexes_number):
                x_index = left_index + x
                y_index = top_index + y
                if self.debug(object, x_index, y_index):
                    object.place_in_net.append((x_index, y_index))
                    self.net[y_index][x_index].append(object)
    
    def debug(self, object, x_index, y_index) -> bool:
        net_size = len(self.net) - 1
        if not x_index in range(net_size): 
            object.kill()
            return False
        if not y_index in range(net_size):
            object.kill()
            return False
        return True
    
    def add_list(self, list):
        for obj in list:
            self.add_object(obj)
        
    def update(self, game):
        self.clear()
        self.add_object(game.player)
        self.add_list(game.bullets.sprites())
        self.add_list(game.enemies.sprites())
        self.add_list(game.items.sprites())
        self.add_list(game.chests.sprites())

    def query(self, object, hitbox):
        ret_arr = []
        for place in object.place_in_net:
            x_index, y_index = place
            for obj in self.net[y_index][x_index]:
                if hitbox.colliderect(obj.hitbox):
                    if obj != object:
                        ret_arr.append(obj)
        return ret_arr

    def draw(self, window, player):
        half_width = window.get_size()[0] // 2
        half_heigth = window.get_size()[1] // 2

        for y in range(45):
            for x in range(45):
                dx = x * TILE_SIZE * 5 - player.hitbox.centerx + half_width
                dy = y * TILE_SIZE * 5 - player.hitbox.centery + half_heigth
                color = 'blue' if len(self.net[y][x]) else 'yellow'

                rect = pygame.Rect(dx, dy, TILE_SIZE * 5, TILE_SIZE * 5)
                pygame.draw.rect(window, color, rect, 1)
                
                
