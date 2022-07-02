import pygame
from pygame.math import Vector2
from gun import Gun
from settings import Direction, ObjectType, colors
from math import atan, pi
from random import choice

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups: list[pygame.sprite.Group], pos: tuple, gun: Gun, based_stats: dict) -> None:
        super().__init__(groups)
        self.object_type = ObjectType.enemy
        self.can_move = True
        self.place_in_net = []

        self.based_stats = based_stats

        self.gun = gun
        self.notice_rad = based_stats['notice_rad']

        self.color = based_stats['color']
        self.image_orig = pygame.Surface(self.based_stats['size'])
        self.image_orig.set_colorkey('black')
        self.image_orig.fill(self.color)

        self.image = self.image_orig.copy()
        self.rect = self.image_orig.get_rect(topleft = pos)

        self.hitbox = self.rect.copy().inflate(7, 7)

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
        self.image = pygame.transform.rotate(self.image_orig , rot)  
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
        collision_objects = obsticles.query(self)
        for _object in collision_objects:
            if _object.object_type == ObjectType.wall or _object.object_type == ObjectType.enemy:
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
        
        if _distance in range(300, self.notice_rad):
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
        self.gun.fire([game.visible_sprites, game.bullets], (qx, qy), self.get_angle())
    
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
    def __init__(self, groups: list[pygame.sprite.Group], pos: tuple, guns: list[Gun], based_stats: dict) -> None:
        super().__init__(groups, pos, choice(guns), based_stats)
        self.import_graphics()
        self.inventory = guns
    
    def import_graphics(self):
        offset = 10
        size = self.image_orig.get_size()
        rect = pygame.Rect(offset, offset, size[0]//2-2*offset, size[1]//2-2*offset)
        pygame.draw.rect(self.image_orig, colors.boss_gray, rect)
        rect.left += size[0]//2
        rect.top += size[1]//2
        pygame.draw.rect(self.image_orig, colors.boss_gray, rect)
    
    def reload(self):
        if self.gun.current_ammo <= 0:
            self.gun.reload()
            self.gun = choice(self.inventory)