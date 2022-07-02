from random import randint
import pygame
from cooldown import Cooldown
from settings import Status
from bullet import Bullet, CircleBullet, OrbitBullets, ExplosiveBullets
from math import pi, sin, cos

class Gun:
    def __init__(self, owner: Status, gun_data: dict) -> None:

        self.based_stats = gun_data

        self.bullets_data = self.based_stats['bullets']

        self.owner = owner
        self.item_type = self.based_stats['item_type']

        if self.based_stats['path'] != None:
            image_origin = pygame.image.load(self.based_stats['path']).convert_alpha()
            self.image_origin = pygame.transform.scale(image_origin, (image_origin.get_width()*3, image_origin.get_height()*3))

        self.offset = self.based_stats['offset']
        self.current_ammo = self.based_stats['ammo']
        self.damage = self.based_stats['dmg']

        self.can_fire = Cooldown(self.based_stats['fire_rate'])

        _reload = int(self.based_stats['reload_time']/self.based_stats['ammo'])
        self.can_add_bullet = Cooldown(_reload)

        self.last_reload_time = 0
        self.last_reload_bullets = 0

        self.can_reload = True
    
    def render(self, screen, player):
        angle = player.get_mouse_angle()
        image = self.image_origin.copy()
        if angle > pi/2 and angle < 3*pi/2: image = pygame.transform.flip(image, False, True)
        image = pygame.transform.rotate(image, (angle/pi*180))
        x_place = player.on_screen.x + cos(angle)*40 - image.get_width()//2
        y_place = player.on_screen.y - sin(angle)*40 - image.get_height()//2

        screen.blit(image, (x_place, y_place))
    
    def make_shots(self, groups, user_place, angle):
        n = randint(-10, 10)
        if n == 0: n = 1
        offset = self.offset/n
        Bullet(groups, self.bullets_data, user_place, angle+offset, self.owner, self.damage)

    def fire(self, groups, user_place, angle):
        if not self.can_fire(): return
        if not self.can_reload: return
        if self.current_ammo <= 0: return

        self.can_fire.can_perform = False
        self.can_fire.last_used_time = pygame.time.get_ticks()
        self.make_shots(groups, user_place, angle)
        self.current_ammo -= 1

    def reload(self):
        if not self.can_reload: return

        self.can_reload = False
        self.can_add_bullet.can_perform = False
        self.can_add_bullet.last_used_time = pygame.time.get_ticks()
        
        self.last_reload_time = self.can_add_bullet.last_used_time
        self.last_reload_bullets = self.current_ammo

    def add_ammo_logic(self):
        if self.can_reload: return
        if self.current_ammo == self.based_stats['ammo']:
            self.can_reload = True
        else:
            if not self.can_add_bullet(): return
            self.add_ammo()
            self.can_add_bullet.can_perform = False
        
    def add_ammo(self):
        self.current_ammo += 1
        self.can_add_bullet.last_used_time = pygame.time.get_ticks()
    
    def add_modifier(self, modifier):
        self.damage += modifier.dmg_boost

    def update(self):
        self.cooldown()
        self.add_ammo_logic()
    
    def cooldown(self):
        self.can_fire.timer()
        self.can_add_bullet.timer()
    
    def special_interaction(self, gameplay):
        pass

class Shotgun(Gun):
    def __init__(self, owner: Status, gun_data: dict) -> None:
        super().__init__(owner, gun_data)
        self.one_shot = int((self.based_stats['number_of_bullets_in_one_shot']-1)//2)
    
    def add_bullet(self, groups: list[pygame.sprite.Group], user_place: tuple, angle: float) -> None:
        Bullet(groups, self.bullets_data, user_place, angle, self.owner, self.damage)

    def make_shots(self, groups, user_place, angle):
        self.add_bullet(groups, user_place, angle)
        offset = self.offset
        for i in range(self.one_shot):
            self.add_bullet(groups, user_place, angle+offset)
            self.add_bullet(groups, user_place, angle-offset)
            offset+=self.offset

class GildedHydra(Shotgun):
    def special_interaction(self, gameplay):
        max_hp  = gameplay.player.max_hp
        current_hp = gameplay.player.hp
        self.based_stats['ammo'] = max_hp - current_hp + 1
        _reload = self.based_stats['reload_time']/self.based_stats['ammo']
        self.can_add_bullet.time_long = _reload
    
class Railgun(Gun):
    def make_shots(self, groups, user_place, angle):
        for i in range(2): OrbitBullets(groups, self.bullets_data, user_place, angle, self.owner, self.damage, pi/2+i*pi-angle)

class WallGun(Shotgun):
    def make_shots(self, groups, user_place, angle):
        self.add_bullet(groups, user_place, angle)
        _sin = sin(angle)
        _cos = cos(angle)
        distance = 20
        for i in range(self.one_shot):
            x = user_place[0]+_sin*distance-_cos*(i+1)*self.offset
            y = user_place[1]+_cos*distance+_sin*(i+1)*self.offset
            self.add_bullet(groups, (x, y), angle)
            x = user_place[0]-_sin*distance-_cos*(i+1)*self.offset
            y = user_place[1]-_cos*distance+_sin*(i+1)*self.offset
            self.add_bullet(groups, (x, y), angle)
            distance += 20

class IceBraker(Shotgun):
    def add_bullet(self, groups: list[pygame.sprite.Group], user_place: tuple, angle: float) -> None:
        Bullet(groups, self.bullets_data[0], user_place, angle, self.owner, self.damage)

    def make_shots(self, groups, user_place, angle):
        if self.current_ammo == 1:
            ExplosiveBullets(groups, self.bullets_data[1], user_place, angle, self.owner, self.damage)
        else:
            super().make_shots(groups, user_place, angle)

class RocketLauncher(Gun):
    def make_shots(self, groups, user_place, angle):
        ExplosiveBullets(groups, self.bullets_data, user_place, angle, self.owner, self.damage)

class DoubleGun:
    def __init__(self, owner: Status, gun_data: dict, guns: list[Gun]) -> None:
        self.status = owner
        self.double_based_stats = gun_data
        self.item_type = self.double_based_stats['item_type']
        self.guns = guns
        self.gun_index = 0
        self.current_gun = self.guns[self.gun_index]
        self._import_stats()
    
    def _import_stats(self) -> None:
        self.image_origin = self.current_gun.image_origin
        self.damage = self.current_gun.damage
        self.based_stats = self.current_gun.based_stats
        self.current_ammo = self.current_gun.current_ammo
        self.can_reload = self.current_gun.can_reload
        self.last_reload_bullets = self.current_gun.last_reload_bullets
        self.can_add_bullet = self.current_gun.can_add_bullet
        self.last_reload_time = self.current_gun.last_reload_time
    
    def _update_stats(self):
        self.current_ammo = self.current_gun.current_ammo
        self.can_reload = self.current_gun.can_reload
    
    def fire(self, groups, user_place, angle):
        self.current_gun.fire(groups, user_place, angle)
    
    def reload(self):
        self.gun_index += 1
        self.current_gun = self.guns[self.gun_index%2]
        self.current_gun.reload()
        self._import_stats()
    
    def update(self):
        self._update_stats()
        self.current_gun.update()
    
    def add_modifier(self, modifier):
        self.guns[0].add_modifier(modifier)
        self.guns[1].add_modifier(modifier)
    
    def render(self, screen, player):
        self.current_gun.render(screen, player)
    
    def special_interaction(self, gameplay):
        self.current_gun.special_interaction(gameplay)

class ShotgunM3(Shotgun):
    def __init__(self, owner: Status, gun_data: dict) -> None:
        super().__init__(owner, gun_data)
        self.one_shot = self.based_stats['number_of_bullets_in_one_shot']

    def make_shots(self, groups, user_place, angle):
        for n in range(self.one_shot):
            _angle = 2*pi*n/self.one_shot
            OrbitBullets(groups, self.bullets_data, user_place, angle, self.owner, self.damage, _angle)