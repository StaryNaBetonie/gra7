import pygame
from math import pi, sin, cos, atan
from pygame.math import Vector2
from settings import Direction, ItemType, ObjectType, colors
from inventory import Inventory
from random import randint
from cooldown import Cooldown
from tile import Tile
from support import get_surface

class Player(Tile):
    def __init__(self, groups, pos) -> None:
        super().__init__(groups, pos, get_surface((40, 40), colors.cyanic), ObjectType.player, 0)
        self.on_screen = Vector2(0, 0)

        self.inventory = Inventory()
        self.weapon_number = 0
        self.gun = self.inventory.space[self.weapon_number]

        self.max_hp = 30
        self.hp = self.max_hp

        self.can_get_hit = Cooldown(100)
        self.is_not_dodging = Cooldown(200)
        self.can_make_dodge = Cooldown(700)
        self.dodge_direction = pygame.math.Vector2()

        self.direction = Vector2()
        self.speed = 6

        self.interaction_hitbox = self.rect.copy().inflate(10, 10)
    
    def interact_with_objects(self, game):
        objects = game.net_group.query(self, self.interaction_hitbox)
        for _object in objects:
            if _object.object_type == ObjectType.raisable:
                self.add_item(_object.item)
                _object.kill()
            if _object.object_type == ObjectType.chest:
                _object.open(game)
    
    def get_hit(self):
        if not self.can_get_hit(): return
        self.can_get_hit.can_perform = False
        self.can_get_hit.last_used_time = pygame.time.get_ticks()
        self.hp -= 1

    def add_item(self, item):
        if item.item_type == ItemType.modifier:
            self.gun.add_modifier(item)
        else:
            self.inventory.space.append(item)
    
    def make_dodge(self):
        if not self.can_make_dodge(): return
        if self.direction.magnitude() == 0: return
        self.is_not_dodging.can_perform = False
        self.can_make_dodge.can_perform = False
        self.is_not_dodging.last_used_time = pygame.time.get_ticks()
        self.can_make_dodge.last_used_time = pygame.time.get_ticks()

    def get_mouse_angle(self):
        mouse = pygame.mouse.get_pos()
        dx = -self.on_screen.x + mouse[0]
        dy = self.on_screen.y - mouse[1]

        if dx == 0: angle = pi/2 if dy > 0 else 3*pi/2
        else:  angle = atan(dy/dx)
        if dx < 0: angle += pi
        
        self.spin = Vector2(-cos(angle), sin(angle))
        
        return angle
    
    def rotate(self):
        old_center = self.rect.center   
        rot = (self.get_mouse_angle()*180)/3.14
        self.image = pygame.transform.rotate(self.image_origin , rot)  
        self.rect = self.image.get_rect()  
        self.rect.center = old_center 

    def set_directions(self, actions):
        if not self.is_not_dodging(): return

        if actions['up']: self.direction.y = -1
        elif actions['down']: self.direction.y = 1
        else: self.direction.y = 0
        
        if actions['left']: self.direction.x = -1
        elif actions['right']: self.direction.x = 1
        else: self.direction.x = 0

    def change_item_slot(self, direction):
        if direction and self.weapon_number != len(self.inventory.space)-1:
            self.weapon_number += 1
        if not direction and self.weapon_number != 0:
            self.weapon_number -= 1
        self.gun = self.inventory.space[self.weapon_number]
    
    def move(self, game):
        if self.direction.magnitude() != 0: self.direction.normalize()
        self.hitbox.centerx += self.direction.x * self.speed
        self.wall_collision(Direction.horizontal, game)
        self.hitbox.centery += self.direction.y * self.speed
        self.wall_collision(Direction.vertical, game)
        self.dodge_direction = self.direction
        self.rect.center = self.hitbox.center
        self.interaction_hitbox.center = self.hitbox.center
        
        if self.hitbox.colliderect(game.gamestate.exit.rect):
            if game.gamestate.mob_spawner.boss is None:
                game.new_level()
    
    def wall_collision(self, direction, game):
        collision_objects = game.static_objects.query(self, self.hitbox)
        for _object in collision_objects:
            if direction == Direction.horizontal:
                if self.direction.x > 0:
                    self.hitbox.right = _object.hitbox.left
                if self.direction.x < 0:
                    self.hitbox.left = _object.hitbox.right

            if direction == Direction.vertical:
                if self.direction.y > 0:
                    self.hitbox.bottom = _object.hitbox.top
                if self.direction.y < 0:
                    self.hitbox.top = _object.hitbox.bottom
    
    def fire(self, action, game):
        if not action: return
        x_start = self.hitbox.centerx - self.spin.x * (self.gun.image_origin.get_width())
        y_start = self.hitbox.centery - self.spin.y * (self.gun.image_origin.get_width())
        self.gun.fire([game.visible_sprites, game.bullets], (x_start, y_start), self.get_mouse_angle())
        
    def set_alpha(self):
        alpha = 255 if self.is_not_dodging() else 0
        self.image_origin.set_alpha(alpha)
        self.gun.image_origin.set_alpha(alpha)
    
    def set_speed(self):
        speed = 6 if self.is_not_dodging() else 15
        self.speed = speed
    
    def set_color(self):
        color = colors.cyanic if self.can_get_hit() else colors.crimson
        self.image_origin.fill(color)
    
    def cooldowns(self):
        self.can_get_hit.timer()
        self.is_not_dodging.timer()
        self.can_make_dodge.timer()
    
    def gun_special_interaction(self, game):
        self.gun.special_interaction(game)
    
    def update(self, actions, game):
        self.move(game)
        self.gun_special_interaction(game)
        self.cooldowns()
        self.rotate()
        self.set_directions(actions)
        self.fire(actions['fire'], game)
        self.gun.update()
        self.set_alpha()
        self.set_speed()
        self.set_color()