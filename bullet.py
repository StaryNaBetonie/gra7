import pygame
from pygame.math import Vector2
from random import randint, choice
from particles import Particles, StaticParticle
from settings import ObjectType, Status, colors, bullets, BulletType
from math import pi, sin, cos
from explosion import Explosion
from particles import StaticParticle
from cooldown import Cooldown
from support import get_surface
from tile import Tile

def create_bullet(groups, based_stats, pos, angle, status, damage, rotate_angle=None):
    bullet_type = based_stats['type']
    if bullet_type is BulletType.normal: Bullet(groups, based_stats, pos, angle, status, damage, rotate_angle)
    elif bullet_type is BulletType.orbit: OrbitBullets(groups, based_stats, pos, angle, status, damage, rotate_angle)
    elif bullet_type is BulletType.explosive: ExplosiveBullets(groups, based_stats, pos, angle, status, damage, rotate_angle)
    elif bullet_type is BulletType.fragment: FragmentationBullet(groups, based_stats, pos, angle, status, damage, rotate_angle)

class Bullet(Tile):
    def __init__(self, groups: list[pygame.sprite.Group], based_stats: dict, pos: tuple, angle: float, status: Status, damage: int, rotate_angle=None) -> None:
        super().__init__(groups, get_surface(based_stats['size'], based_stats['color']), ObjectType.bullet, 2, (0, 0), center = pos)
        self.based_stats = based_stats

        self.light_rad = self.based_stats['light_rad']
        self.bullet_type = self.based_stats['type']
        self.status = status
        self.damage = damage
        self.angle = angle

        self.rotate(angle, rotate_angle, pos)

        self.direction = Vector2(cos(angle), -sin(angle)).normalize()

        self.speed = self.based_stats['speed']
        self.acceleration = self.based_stats['acceleration']

        self.life_cooldown = Cooldown(15000)
        self.life_cooldown.can_perform = False
        self.life_cooldown.last_used_time = pygame.time.get_ticks()
    
    def rotate(self, angle, rotate_angle, pos):
        self.rotate_angle = angle if rotate_angle is None else rotate_angle
        self.image = pygame.transform.rotate(self.image_origin, self.rotate_angle/pi*180)
        self.rect = self.image.get_rect(center = pos)

    def move(self, game):
        self.actions(game)
        self.hitbox.center += self.direction * self.speed
        self.rect.center = self.hitbox.center
        self.speed += self.acceleration
        self.speed = max(0, self.speed)

    def actions(self, game):
        if game.static_objects.query(self, self.hitbox):
            self.hit_obsticle(game)
        obsticles = game.grid_group.query(self, self.hitbox)
        if self.status == Status.player:
            for _object in obsticles:
                if _object.object_type == ObjectType.enemy:
                    self.hit_obsticle(game)
                    _object.get_hit(self.damage)
        elif self.status == Status.enemy:
            for _object in obsticles:
                if _object.object_type == ObjectType.player:
                    if _object.is_not_dodging():
                        self.hit_obsticle(game)
                        _object.get_hit()

    def show_particles(self, groups):
        _colors = [colors.yellow, colors.smoke_gray, colors.orange]
        for i in range(randint(2, 4)):
            offset = randint(-5, 5)
            if offset == 0: offset = 1
            angle = self.angle + pi/6/offset 
            Particles(groups, angle, self.speed, choice(_colors), self.hitbox.center)
    
    def hit_obsticle(self, game):
        self.show_particles([game.visible_sprites, game.particles])
        self.kill()
    
    def life_time(self):
        if self.life_cooldown():
            self.kill()

    def update(self, game):
        self.life_time()
        self.life_cooldown.timer()
        self.move(game)

class OrbitBullets(Bullet):
    def __init__(self, groups: list[pygame.sprite.Group], based_stats: dict, pos: tuple, angle: float, status: Status, damage: int, rotate_angle=None) -> None:
        super().__init__(groups, based_stats, pos, angle, status, damage, rotate_angle)
        self.direction = Vector2(cos(angle), -sin(angle)).normalize()
        self.rotation_speed = self.based_stats['rotate_speed']
        self.radius = 0
        self.abstract_point = pygame.math.Vector2(pos)
    
    def move(self, game):
        self.actions(game)
        self.abstract_point += self.direction * self.speed
        x = self.abstract_point.x + cos(self.rotate_angle) * self.radius
        y = self.abstract_point.y - sin(self.rotate_angle) * self.radius
        self.hitbox.center = (x, y)
        self.rect.center = self.hitbox.center
        self.rotate_angle += self.rotation_speed
        self.angle = self.rotate_angle
    
    def add_rad(self):
        if self.radius < self.based_stats['bullet_radius']:
            self.radius += 3

    def update(self, game):
        super().update(game)
        self.add_rad()

class ExplosiveBullets(Bullet):
    def __init__(self, groups: list[pygame.sprite.Group], based_stats: dict, pos: tuple, angle: float, status: Status, damage: int, rotate_angle=None) -> None:
        super().__init__(groups, based_stats, pos, angle, status, 0, rotate_angle)
        self.explosion_damage = damage

    def show_particles(self, groups, opponents):
        Explosion(groups, self.rect.center, opponents, self.explosion_damage)
    
    def special_effects(self, groups):
        x = self.rect.centerx - self.direction.x * self.rect.width
        y = self.rect.centery - self.direction.y * self.rect.height
        StaticParticle(groups, 'graphics/effects/small-smoke.png', (x, y), (48, 48))
    
    def move(self, game):
        super().move(game)
        self.special_effects([game.visible_sprites, game.particles])
    
    def hit_obsticle(self, game):
        self.show_particles([game.visible_sprites, game.particles], game.enemies.sprites())
        self.kill()

class FragmentationBullet(Bullet):
    def __init__(self, groups: list[pygame.sprite.Group], based_stats: dict, pos: tuple, angle: float, status: Status, damage: int, rotate_angle=None) -> None:
        super().__init__(groups, based_stats, pos, angle, status, damage, rotate_angle)
        self.bullets_inside = self.based_stats['bullets_inside']
        self.can_explode = Cooldown(500)
        self.can_explode.can_perform = False
        self.can_explode.last_used_time =  pygame.time.get_ticks()
    
    def new_bullets(self, game):
        for n in range(self.bullets_inside):
            groups = [game.visible_sprites, game.bullets]
            based_stats = bullets[self.based_stats['bullets_inside_id']]
            angle = self.angle + n * 2 * pi / self.bullets_inside
            create_bullet(groups, based_stats, self.hitbox.center, angle, self.status, self.damage//self.bullets_inside*2)

    def explode(self, game):
        if self.can_explode():
            self.new_bullets(game)
            self.kill()

    def update(self, game):
        super().update(game)
        self.can_explode.timer()
        self.explode(game)

