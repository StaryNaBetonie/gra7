import pygame
from player import Player
from settings import TILE_SIZE, RoomType

class UI:
    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 30)

    def show_player_hp(self, hp, window):
        offset = 0
        for i in range(hp):
            rect = pygame.Rect(1900, 1000-offset, 13, 13)
            pygame.draw.rect(window, 'red', rect)
            offset += rect.height + 5
    
    def show_player_ammo(self, ammo, window):
        offset = 0
        for i in range(ammo):
            rect = pygame.Rect(1880, 1000-offset, 13, 13)
            pygame.draw.rect(window, (250, 130, 30), rect)
            offset += rect.height + 5
    
    def show_map(self, map, window, player):
        player_place = pygame.math.Vector2(int(player.x/15/TILE_SIZE), int(player.y/15/TILE_SIZE))

        for row in map:
            for col in row:
                if col != None:
                    if col.active == True:
                        color = 'gray'
                        if col.room_type == RoomType._enter: color = 'blue'
                        elif col.room_type == RoomType._exit: color = 'red'
                        elif col.room_type == RoomType.chest: color = 'gold'
                        elif col.room_type == RoomType.boss: color = 'purple'

                        pygame.draw.rect(window, color, pygame.Rect(col.place.x*20, col.place.y*20, 17, 17))
                        pygame.draw.rect(window, '#111111', pygame.Rect(player_place.x*20+4, player_place.y*20+4, 9, 9))
    
    def show_gun(self, gun_image, window):
        offset = 20
        image = pygame.transform.scale2x(gun_image)
        if image.get_alpha() != 255: image.set_alpha(255)
        image_rect = pygame.Rect(20, 900, image.get_width(), image.get_height()).inflate(offset, offset)
        pygame.draw.rect(window, '#757575', image_rect)
        pygame.draw.rect(window, '#ffffff', image_rect, 10)
        window.blit(image, (image_rect.left+offset/2, image_rect.top+offset/2))
    
    def show_gun_stats(self, window, damage, ammo):
        damage_str = f'damage: {damage}'
        damage_img = self.font.render(damage_str, False, 'white')
        window.blit(damage_img, (15, 860))

        ammo_str = f'ammo: {ammo}'
        ammo_img = self.font.render(ammo_str, False, 'white')
        window.blit(ammo_img, (15, 840))
    
    def show_boss_hp(self, window, boss, player_pos):
        if boss != None:
            if pygame.Vector2(boss.rect.centerx - player_pos[0], boss.rect.centery - player_pos[1]).magnitude() <= 1000:
                place_rec = pygame.Rect(710, 950, 500, 25)
                pygame.draw.rect(window, '#404040', place_rec)
                multiplier = boss.hp/boss.based_stats['hp']
                hp_rec = pygame.Rect(718, 958, 484 * multiplier, 9)
                pygame.draw.rect(window, '#ffffff', hp_rec)
    
    def reload(self, window: pygame.Surface, player: Player) -> None:
        if player.gun.can_reload == True: return
        if player.gun.current_ammo == player.gun.based_stats['ammo']: return
        if not player.is_not_dodging(): return
        left_border = pygame.Rect(player.on_screen.x-30, player.on_screen.y-40, 5, 10)
        right_border = pygame.Rect(player.on_screen.x+30, player.on_screen.y-40, 5, 10)
        nominator = pygame.time.get_ticks()-player.gun.last_reload_time
        denominator = (player.gun.based_stats['ammo']-player.gun.last_reload_bullets)*(player.gun.can_add_bullet.time_long + 8)
        multiplier = nominator/denominator
        line = pygame.Rect(player.on_screen.x-25, player.on_screen.y-38, 55*multiplier, 6)
        pygame.draw.rect(window, 'white', left_border)
        pygame.draw.rect(window, 'white', right_border)
        pygame.draw.rect(window, 'white', line)

