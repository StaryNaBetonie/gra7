import pygame
from black_screen import BlackScreen
from player import Player
from random import randint
from gamestate import Gamestate, DeepDark
from ui import UI
from settings import StageType, stage_data, LocationType
from grid import GridGroup

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
        self.grid_group = GridGroup()
        self.static_objects = GridGroup()
        
        self.actions = {'up':False, 'left':False, 'down':False, 'right':False, 'fire':False}

        self.ui = UI()
        self.black_screen = BlackScreen()

        self.enemy_cooldow = 2500
        self.enemy_time = 0

        self.stage_number = 0
        self.new_gamestate()

        self.player = Player([self.visible_sprites], self.gamestate.set_player())
    
    def new_gamestate(self):
        _stage_data = stage_data[self.stage_number%5]
        self.static_objects.clear()
        if _stage_data['stage_type'] is StageType.normal: self.gamestate = Gamestate(self)
        else: self.gamestate = DeepDark(self)
        self.static_objects.add_list(self.walls.sprites())
        self.gamestate.mob_spawner.spawn(_stage_data['opponents'], _stage_data['bosses'])

    def render(self, screen):
        self.visible_sprites.custom_draw(self.player)
        self.player.gun.render(screen, self.player)
        self.gamestate.render(screen)
        if self.player.moving_down: self.black_screen.play(screen, self.new_level, self.player)
        self.ui.show_gun(self.player.gun.image_origin.copy(), screen)
        self.ui.show_gun_stats(screen, self.player.gun.damage, self.player.gun.based_stats['ammo'])
        self.ui.show_player_hp(self.player.hp, screen)
        self.ui.show_player_ammo(self.player.gun.current_ammo, screen)
        self.ui.show_map(self.gamestate.gamestate, screen, self.player.rect)
        self.ui.show_boss_hp(screen, self.gamestate.mob_spawner.boss, self.player.rect.center)
        self.ui.reload(screen, self.player)

    def kill_entity(self):
        for item in self.items.sprites(): item.kill()
        for enemy in self.enemies.sprites(): enemy.kill()
        for bullet in self.bullets.sprites(): bullet.kill()
        for floor in self.floor: floor.kill()

    def new_level(self):
        self.stage_number += 1
        self.kill_entity()
        self.gamestate.delete_gamestate()
        self.new_gamestate()
        self.player.hitbox.center = self.gamestate.set_player()
    
    def key_color(self):
        return self.gamestate.key_color
            
    def update(self):
        self.gamestate.kill_boss([self.visible_sprites, self.items])
        self.player.update(self.actions, self)
        self.particles.update()
        self.enemies.update(self) 
        self.bullets.update(self)
        self.gamestate.update(self.player.rect)
        self.grid_group.update(self)
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
            sprite.pos_on_screen = sprite.rect.center - self.offset
            self.display_surface.blit(sprite.image, offset_pos, special_flags = sprite.special_flag)