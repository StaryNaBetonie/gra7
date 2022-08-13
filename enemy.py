import pygame
from pygame.math import Vector2
from gun import Gun
from settings import Direction, ObjectType, colors
from math import atan, pi, sin, cos
from random import choice
from tile import Tile

class Enemy(Tile):
    def __init__(self, groups: list[pygame.sprite.Group], pos: tuple, gun: Gun, based_stats: dict, image: pygame.Surface) -> None:
        super().__init__(groups, image, ObjectType.enemy, 0, (7, 7), topleft = pos)
        self.based_stats = based_stats

        self.gun = gun
        self.notice_rad = based_stats['notice_rad']

        self.direction = Vector2(0, 0)
        self.acceleration = 0

        self.hp = based_stats['hp']
        self.speed = based_stats['speed']
        self.can_knock = based_stats['can_knock']


    def get_angle(self):
        if not self.direction.y: angle = 0 if self.direction.x > 0 else pi
        else: angle = atan(self.direction.x/self.direction.y) + pi/2
        if self.direction.y > 0: angle += pi

        return angle 

    def rotate(self):
        old_center = self.rect.center   
        rot = (self.get_angle()*180)/3.14
        self.image = pygame.transform.rotate(self.image_origin , rot)  
        self.rect = self.image.get_rect()  
        self.rect.center = old_center 

    def get_direction(self, follow_place):
        if self.acceleration != 0: return
        x = Vector2(follow_place).x - self.rect.centerx
        y = Vector2(follow_place).y - self.rect.centery
        magnitude = Vector2(x, y).magnitude()

        self.direction = Vector2(x/magnitude, y/magnitude)

    def move(self, game):
        self.hitbox.x += self.direction.x * self.speed
        self.collision(Direction.horizontal, game.static_objects)
        if self.acceleration == 0: self.collision(Direction.horizontal, game.net_group)
        self.hitbox.y += self.direction.y * self.speed
        self.collision(Direction.vertical, game.static_objects)
        if self.acceleration == 0: self.collision(Direction.vertical, game.net_group)
        self.rect.center = self.hitbox.center
    
    def collision(self, direction, obsticles):
        collision_objects = obsticles.query(self, self.hitbox)
        for _object in collision_objects:
            if _object.object_type in [ObjectType.wall, ObjectType.enemy, ObjectType.chest]:
                if direction == Direction.horizontal:
                    if self.direction.x > 0:
                        self.hitbox.right = _object.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = _object.hitbox.right
                elif direction == Direction.vertical:
                    if self.direction.y > 0:
                        self.hitbox.bottom = _object.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = _object.hitbox.bottom


    def move_logic(self, game):
        if self.direction.magnitude() != 0: self.direction.normalize()
        dx = self.hitbox.centerx - game.player.hitbox.centerx
        dy = self.hitbox.centery - game.player.hitbox.centery

        _distance = int(Vector2(dx, dy).magnitude())
        
        if _distance in range(300, self.notice_rad) or self.acceleration != 0:
            self.move(game)
        
    def get_hit(self, damage):
        self.hp -= damage
    
    def death(self):
        if self.hp > 0: return
        self.kill()

    def create_attack(self, game):
        if self.acceleration != 0: return
        _distance = (Vector2(self.rect.center) - Vector2(game.player.hitbox.center)).magnitude()
        if _distance >= self.notice_rad: return
        qx = self.rect.centerx + self.direction.x*self.rect.width/2
        qy = self.rect.centery + self.direction.y*self.rect.width/2
        self.gun.fire([game.bullets, game.visible_sprites], (qx, qy), self.get_angle())
    
    def reload(self):
        if self.gun.current_ammo <= 0:
            self.gun.reload()
    
    def acceleration_logic(self):
        if self.acceleration == 0: return
        self.speed += self.acceleration
        if self.speed > self.based_stats['speed']: return
        self.speed = self.based_stats['speed']
        self.acceleration = 0
    
    def update(self, game):
        self.create_attack(game)
        self.get_direction(game.player.hitbox.center)
        self.rotate()
        self.move_logic(game)
        self.gun.update()
        self.death()
        self.acceleration_logic()
        self.reload()

class Boss(Enemy):
    def __init__(self, groups: list[pygame.sprite.Group], pos: tuple, guns: list[Gun], based_stats: dict, image: pygame.Surface) -> None:
        super().__init__(groups, pos, choice(guns), based_stats, image)
        self.inventory = guns
        self.left = self.image
        self.right = pygame.transform.flip(self.image, True, False)
    
    def rotate(self):
        self.image = self.left if self.direction.x < 0 else self.right
    
    def get_pos(self):
        return self.hitbox.center
    
    def reload(self):
        if self.gun.current_ammo <= 0:
            self.gun.reload()
            self.gun = choice(self.inventory)

class WormPart(Tile):
    def __init__(self, groups, pos: tuple, image: pygame.Surface, resistance: float) -> None:
        super().__init__(groups, image, ObjectType.enemy, 0, (7, 7), center = pos)
        self.next_part = None
        self.resistance = resistance
        self.taken_damage = 0
    
    def get_hit(self, damage):
        self.taken_damage += damage*self.resistance
    
    def kill_part(self):
        if self.next_part is not None:
            self.next_part.kill_part()
        self.kill()
        
    def move(self, new_x: int, new_y: int, direction_x):
        if self.next_part is not None: 
            self.next_part.move(self.rect.centerx - direction_x * 20, self.rect.centery + self.hitbox.height-40, direction_x)
        self.hitbox.centerx = new_x
        self.hitbox.centery = new_y
        self.rect.center = self.hitbox.center

class Worm:
    def __init__(self, groups: list[pygame.sprite.Group], pos: tuple, guns: Gun, based_stats: dict) -> None:
        self.can_move = True
        self.based_stats = based_stats
        self.inventory = guns
        self.gun = self.inventory[0]
        self.notice_rad = based_stats['notice_rad']
        self.color = based_stats['color']
        self.head = self.get_snake(groups, pos)
        self.direction = pygame.Vector2()
        self.rotate_angle = 0

        self.hp = based_stats['hp']
        self.speed = based_stats['speed']
        self.can_knock = based_stats['can_knock']
    
    def get_pos(self):
        return self.head.hitbox.center

    def get_snake(self, groups, pos):
        head_graphics = pygame.transform.scale2x(pygame.image.load('graphics/snake/snake_head.png').convert_alpha())
        body_graphics = pygame.transform.scale2x(pygame.image.load('graphics/snake/snake_body.png').convert_alpha())
        tail_graphics = pygame.transform.scale2x(pygame.image.load('graphics/snake/snake_tail.png').convert_alpha())
        head = WormPart(groups, pos, head_graphics, 1)
        part = head
        for n in range(1, 5):
            image = body_graphics if n == 1 else tail_graphics
            part.next_part = WormPart(groups, pos, image, 0.5)
            part = part.next_part
        return head
    
    def get_angle(self):
        if not self.direction.y: angle = 0 if self.direction.x > 0 else pi
        else: angle = atan(self.direction.x/self.direction.y) + pi/2
        if self.direction.y > 0: angle += pi

        return angle
    
    def rotate(self): 
        angle = self.get_angle()
        if angle < pi: angle = 2*pi - angle
        offset = pi/8
        if angle < (3*pi/2 - offset): angle = (3*pi/2 - offset)
        if angle > (3*pi/2 + offset): angle = (3*pi/2 + offset)
        self.rotate_angle = angle
        rot = ((self.rotate_angle + pi/2)*180)/3.14
        self.head.image = pygame.transform.rotate(self.head.image_origin, rot)  
        self.head.rect = self.head.image.get_rect(center = self.head.hitbox.center) 

    def move(self, game):
        new_x = self.head.hitbox.centerx + self.direction.x * self.speed
        self.collision(Direction.horizontal, game.static_objects)
        new_y = self.head.hitbox.centery + self.direction.y * self.speed
        self.collision(Direction.vertical, game.static_objects)
        self.head.move(new_x, new_y, self.direction.x)
    
    def collision(self, direction, obsticles):
        collision_objects = obsticles.query(self.head, self.head.hitbox)
        for _object in collision_objects:
            if _object.object_type == ObjectType.wall:
                if direction == Direction.horizontal:
                    if self.direction.x > 0:
                        self.head.hitbox.right = _object.hitbox.left
                    elif self.direction.x < 0:
                        self.head.hitbox.left = _object.hitbox.right
                elif direction == Direction.vertical:
                    if self.direction.y > 0:
                        self.head.hitbox.bottom = _object.hitbox.top
                    elif self.direction.y < 0:
                        self.head.hitbox.top = _object.hitbox.bottom
            
    def move_logic(self, game):
        if self.direction.magnitude() != 0: self.direction.normalize()
        dx = self.head.hitbox.centerx - game.player.hitbox.centerx
        dy = self.head.hitbox.centery - game.player.hitbox.centery

        _distance = int(Vector2(dx, dy).magnitude())
        
        if _distance in range(300, self.notice_rad):
            self.move(game)
        
    def taken_damage(self):
        taken_damage = 0
        part = self.head
        while part.next_part is not None:
            taken_damage += part.taken_damage
            part = part.next_part
        self.hp = self.based_stats['hp'] - taken_damage
    
    def death(self):
        self.taken_damage()
        if  self.hp <= 0:
            self.kill()
    
    def kill(self):
        self.head.kill_part()
    
    def get_direction(self, follow_place):
        x = follow_place[0] - self.head.hitbox.centerx
        y = follow_place[1] - self.head.hitbox.centery
        magnitude = Vector2(x, y).magnitude()

        self.direction = Vector2(x/magnitude, y/magnitude)
    
    def create_attack(self, game):
        _distance = (Vector2(self.head.hitbox.center) - Vector2(game.player.hitbox.center)).magnitude()
        if _distance >= self.notice_rad: return
        qx = self.head.hitbox.centerx + self.head.hitbox.width//2*cos(self.rotate_angle)
        qy = self.head.hitbox.centery - (self.head.hitbox.height//2 - 50)*sin(self.rotate_angle)
        self.gun.fire([game.bullets, game.visible_sprites], (qx, qy), self.get_angle())

    def reload(self):
        if self.gun.current_ammo <= 0:
            self.gun.reload()
            self.gun = choice(self.inventory)
        
    def update(self, game):
        self.rotate()
        self.create_attack(game)
        self.get_direction(game.player.hitbox.center)
        self.move_logic(game)
        self.gun.update()
        self.death()
        self.reload()
