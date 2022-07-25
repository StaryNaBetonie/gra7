import pygame
from enemy import Enemy
from player import Player
from random import randint
from gamestate import Gamestate
from ui import UI
from settings import stage_data, LocationType
from net import NetGroup

class GamePlay:
    def __init__(self) -> None:
        self.type = LocationType.gameplay
        self.visible_sprites = CustomCamera()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.chests = pygame.sprite.Group()
        self.floor = pygame.sprite.Group()
        self.net_group = NetGroup()
        self.static_objects = NetGroup()
        
        self.actions = {'up':False, 'left':False, 'down':False, 'right':False, 'fire':False}

        self.ui = UI()

        self.enemy_cooldow = 2500
        self.enemy_time = 0

        self.stage_number = 0
        self.new_gamestate()

        self.player = Player([self.visible_sprites], self.gamestate.set_player())
    
    def new_gamestate(self):
        _stage_data = stage_data[self.stage_number%4]
        self.static_objects.clear()
        self.gamestate = Gamestate(self)
        self.static_objects.add_list(self.walls.sprites())
        self.gamestate.mob_spawner.spawn(_stage_data['opponents'], _stage_data['bosses'])

    def render(self, screen):
        self.visible_sprites.custom_draw(self.player)
        self.player.gun.render(screen, self.player)
        self.ui.show_gun(self.player.gun.image_origin.copy(), screen)
        self.ui.show_gun_stats(screen, self.player.gun.damage, self.player.gun.based_stats['ammo'])
        self.ui.show_player_hp(self.player.hp, screen)
        self.ui.show_player_ammo(self.player.gun.current_ammo, screen)
        self.ui.show_map(self.gamestate.gamestate, screen, self.player.rect)
        self.ui.show_boss_hp(screen, self.gamestate.mob_spawner.boss, self.player.rect.center)
        self.ui.reload(screen, self.player)

    def kill_entity(self):
        for item in self.items.sprites():
            item.kill()
        for enemy in self.enemies.sprites():
            enemy.kill()

    def new_level(self):
        for floor in self.floor: floor.kill()
        self.stage_number += 1
        self.kill_entity()
        self.gamestate.delete_gamestate()
        self.new_gamestate()
        self.player.hitbox.topleft = self.gamestate.set_player()
    
    def key_color(self):
        return self.gamestate.key_color
            
    def update(self):
        self.gamestate.kill_boss([self.visible_sprites, self.items])
        self.player.update(self.actions, self)
        self.particles.update()
        self.enemies.update(self) 
        self.bullets.update(self)
        self.gamestate.update(self.player.rect)
        self.net_group.update(self)
        if self.gamestate.mob_spawner.boss is  None: return
        self.gamestate.mob_spawner.boss.update(self)

class CustomCamera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_heigth = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_heigth
        player.on_screen = pygame.math.Vector2(self.half_width, self.half_heigth)

        for sprite in sorted(self.sprites(), key = lambda sprite: (sprite._layer, sprite.rect.centery)):
            offset_pos = sprite.rect.topleft - self.offset
            x = sprite.rect.centerx-player.hitbox.centerx
            y = sprite.rect.centery-player.hitbox.centery
            if pygame.math.Vector2(x, y).magnitude() < 1700:
                self.display_surface.blit(sprite.image, offset_pos)