from enum import Enum
from json.encoder import INFINITY
from math import pi
from dataclasses import dataclass

TILE_SIZE = 64

class Action(Enum):
    up = 1
    down = 2
    left = 3
    right = 4
    fire = 5
    _reload = 6

class RoomType(Enum):
    normal = 0
    _enter = 1
    _exit = 2
    chest = 3
    boss = 4

class Status(Enum):
    enemy = 1
    player = 2

class Direction(Enum):
    vertical = 1
    horizontal = 2

class Border(Enum):
    top = (0, -1)
    bottom = (0, 1)
    left = (-1, 0)
    right = (1, 0)

class ItemType(Enum):
    gun = 1
    shotgun = 2
    wallgun = 3
    gilded_hydra = 4
    ice_braker = 5
    rocket_launcher = 6
    double_gun = 7
    shotgun_m3 = 8
    modifier = 9
    fragment_gun = 10
    fragment_shotgun = 11
    shotgun_m3_last_bullet = 12

class BulletType(Enum):
    normal = 1
    orbit = 2
    explosive = 3
    fragment = 4

class LocationType(Enum):
    gameplay = 1
    exit_screen = 2

class ObjectType(Enum):
    player = 1
    enemy = 2
    bullet = 3
    wall = 4
    raisable = 5
    chest = 6
    stairs = 7
    shadow = 8

class ChestStatus(Enum):
    closed = 1
    opened = 2

class StageType(Enum):
    normal = 1
    deepdark = 2

@dataclass
class colors:
    black = '#000000'
    white = '#ffffff'
    light_gray = '#a0a0a0'
    lighter_gray = '#828282'
    boss_gray = '#333333'
    orange = '#fa821e'
    light_blue = '#b0fffc'
    dark_green = '#07571c'
    lime_green = '#1fab00'
    red_gray = '#8f4d49'
    marble_gray = '#b2a6a6'
    crimson = '#c21a00'
    navy_blue = '#0028ad'
    dirty_green = '#526e56'
    dirty_blue = '#3b6d87'
    sea_green = '#2ca887'
    golden = '#ff9900'
    dark_gray = '#202020'
    yellow = '#ebc034'
    smoke_gray = '#9c9c9c'
    cyanic = '#00918c'
    dark_brown = '#25131a'
    seaweed_green = '#090716'
    blue_gray = '#1d1d21'
    crimson_background = '#2f0b00'
    deepdark_keycolor = '#000706'
    glowstone = '#ecd13e'

bullets = [
    # player
    {'id': 0, 'color': colors.orange, 'speed': 10, 'acceleration': 0, 'type': BulletType.normal, 'size': (11, 11), 'light_rad': 75},
    {'id': 1, 'color': colors.light_blue, 'speed': 10, 'acceleration': 0, 'type': BulletType.normal, 'size': (11, 11), 'light_rad': 75},
    {'id': 2, 'color': colors.light_blue, 'speed': 7, 'acceleration': 0.25, 'type': BulletType.explosive, 'size': (27, 27), 'light_rad': 75},
    {'id': 3, 'color': colors.orange, 'speed': 3, 'acceleration': 0.5, 'type': BulletType.explosive, 'size': (27, 27), 'light_rad': 75},
    {'id': 4, 'color': colors.dark_green, 'speed': 3, 'acceleration': 0.5, 'type': BulletType.explosive, 'size': (27, 27), 'light_rad': 75},
    {'id': 5, 'color': colors.orange, 'speed': 10, 'acceleration': 0, 'type': BulletType.orbit, 'size': (11, 11), 'rotate_speed': pi/18, 'bullet_radius': 30, 'light_rad': 75},
    {'id': 6, 'color': colors.orange, 'speed': 10, 'acceleration': 0, 'type': BulletType.orbit, 'size': (11, 11), 'rotate_speed': 0, 'bullet_radius': 50, 'light_rad': 75},
    {'id': 7, 'color': colors.orange, 'speed': 10, 'acceleration': 0.2, 'type': BulletType.orbit, 'size': (15, 15), 'rotate_speed': pi/12, 'bullet_radius': 30, 'light_rad': 75},
    {'id': 8, 'color': colors.lime_green, 'speed': 10, 'acceleration': 0, 'type': BulletType.normal, 'size': (11, 11), 'light_rad': 75},
    {'id': 9, 'color': colors.red_gray, 'speed': 10, 'acceleration': 0.1, 'type': BulletType.orbit, 'size': (15, 15), 'rotate_speed': pi/18, 'bullet_radius': 30, 'light_rad': 75},
    {'id': 10, 'color': colors.red_gray, 'speed': 10, 'acceleration': 0, 'type': BulletType.orbit, 'size': (11, 11), 'rotate_speed': 0, 'bullet_radius': 30, 'light_rad': 75},
    {'id': 11, 'color': colors.red_gray, 'speed': 10, 'acceleration': 0, 'type': BulletType.normal, 'size': (11, 11), 'light_rad': 75},
    {'id': 12, 'color': colors.red_gray, 'speed': 15, 'acceleration': 0, 'type': BulletType.orbit, 'size': (11, 11), 'rotate_speed': pi/18, 'bullet_radius': 30, 'light_rad': 75},
    {'id': 13, 'color': colors.red_gray, 'speed': 15, 'acceleration': 0, 'type': BulletType.normal, 'size': (11, 11), 'light_rad': 75},
    {'id': 14, 'color': colors.marble_gray, 'speed': 15, 'acceleration': 0, 'type': BulletType.normal, 'size': (11, 11), 'light_rad': 75},
    {'id': 15, 'color': colors.marble_gray, 'speed': 3, 'acceleration': 0.25, 'type': BulletType.normal, 'size': (11, 11), 'light_rad': 75},
    {'id': 16, 'color': colors.marble_gray, 'speed': 10, 'acceleration': 0, 'type': BulletType.orbit, 'size': (11, 11), 'rotate_speed': pi/72, 'bullet_radius': 200, 'light_rad': 75},
    {'id': 17, 'color': colors.marble_gray, 'speed': 10, 'acceleration': 1, 'type': BulletType.normal, 'size': (15, 15), 'light_rad': 75},
    {'id': 18, 'color': colors.orange, 'speed': 10, 'acceleration': 0, 'type': BulletType.fragment, 'size': (15, 15), 'bullets_inside': 4, 'bullets_inside_id': 0, 'light_rad': 75},
    {'id': 19, 'color': colors.orange, 'speed': 10, 'acceleration': 0.5, 'type': BulletType.fragment, 'size': (15, 15), 'bullets_inside': 8, 'bullets_inside_id': 23, 'light_rad': 75},
    {'id': 20, 'color': colors.white, 'speed': 12, 'acceleration': 0, 'type': BulletType.orbit, 'size': (11, 11), 'rotate_speed': pi/72, 'bullet_radius': 30, 'light_rad': 75},
    {'id': 21, 'color': colors.white, 'speed': 5, 'acceleration': 0, 'type': BulletType.fragment, 'size': (20, 20), 'bullets_inside': 4, 'bullets_inside_id': 14, 'light_rad': 75},
    {'id': 22, 'color': colors.white, 'speed': 0, 'acceleration': 0, 'type': BulletType.normal, 'size': (32, 32), 'light_rad': 75},
    {'id': 23, 'color': colors.orange, 'speed': 10, 'acceleration': 0.5, 'type': BulletType.normal, 'size': (11, 11), 'light_rad': 75},
    {'id': 24, 'color': colors.orange, 'speed': 5, 'acceleration': 0, 'type': BulletType.fragment, 'size': (31, 31), 'bullets_inside': 8, 'bullets_inside_id': 25, 'light_rad': 75},
    {'id': 25, 'color': colors.orange, 'speed': 7, 'acceleration': 0, 'type': BulletType.fragment, 'size': (23, 23), 'bullets_inside': 16, 'bullets_inside_id': 26, 'light_rad': 75},
    {'id': 26, 'color': colors.orange, 'speed': 10, 'acceleration': 0, 'type': BulletType.normal, 'size': (17, 17), 'light_rad': 75},
    {'id': 27, 'color': colors.glowstone, 'speed': 0, 'acceleration': 0, 'type': BulletType.orbit, 'size': (17, 17), 'rotate_speed': pi/48, 'bullet_radius': 320, 'light_rad': 150},
    {'id': 28, 'color': colors.glowstone, 'speed': 12, 'acceleration': 0, 'type': BulletType.orbit, 'size': (17, 17), 'rotate_speed': pi/48, 'bullet_radius': 100, 'light_rad': 150},
    {'id': 29, 'color': colors.glowstone, 'speed': 12, 'acceleration': 0, 'type': BulletType.orbit, 'size': (17, 17), 'rotate_speed': -pi/48, 'bullet_radius': 100, 'light_rad': 150},
    {'id': 30, 'color': colors.glowstone, 'speed': 10, 'acceleration': 0, 'type': BulletType.orbit, 'size': (11, 11), 'rotate_speed': pi/48, 'bullet_radius': 30, 'light_rad': 75},
    {'id': 31, 'color': colors.glowstone, 'speed': 10, 'acceleration': 0, 'type': BulletType.orbit, 'size': (11, 11), 'rotate_speed': -pi/48, 'bullet_radius': 30, 'light_rad': 75},
    {'id': 32, 'color': colors.glowstone, 'speed': 12, 'acceleration': -0.3, 'type': BulletType.normal, 'size': (21, 21), 'light_rad': 125},
    {'id': 33, 'color': colors.glowstone, 'speed': 10, 'acceleration': 0, 'type': BulletType.normal, 'size': (15, 15), 'light_rad': 75},
    {'id': 34, 'color': colors.white, 'speed': 15, 'acceleration': -0.2, 'type': BulletType.normal, 'size': (13, 13), 'light_rad': 75},
    {'id': 35, 'color': colors.white, 'speed': 3, 'acceleration': 0.2, 'type': BulletType.fragment, 'size': (31, 31), 'bullets_inside': 4, 'bullets_inside_id': 36, 'light_rad': 75},
    {'id': 36, 'color': colors.white, 'speed': 7, 'acceleration': 0, 'type': BulletType.fragment, 'size': (23, 23), 'bullets_inside': 16, 'bullets_inside_id': 37, 'light_rad': 75},
    {'id': 37, 'color': colors.white, 'speed': 10, 'acceleration': 0, 'type': BulletType.normal, 'size': (17, 17), 'light_rad': 75},
]

weapon = [
    {'name': 'VoidShotgun', 'dmg': 10, 'ammo': 10, 'fire_rate': 200, 'reload_time': 600, 'offset': pi/18, 'number_of_bullets_in_one_shot': 3, 'path': 'graphics/guns/VoidShotgun.png', 'item_type': ItemType.shotgun, 'bullets': bullets[0]},
    {'name': 'Gilded_hydra', 'dmg': 10, 'ammo': 1, 'fire_rate': 550, 'reload_time': 2000, 'offset': pi/18, 'number_of_bullets_in_one_shot': 7, 'path': 'graphics/guns/Gilded_hydra.png', 'item_type': ItemType.gilded_hydra, 'bullets': bullets[0]},
    {'name': 'Ice_braker', 'dmg': 15, 'ammo': 3, 'fire_rate': 400, 'reload_time': 600, 'offset': pi/24, 'number_of_bullets_in_one_shot': 3, 'path': 'graphics/guns/Ide_braker.png', 'item_type': ItemType.ice_braker, 'bullets': [bullets[1], bullets[2]]},
    {'name': 'Ratter', 'dmg': 10, 'ammo': 7, 'fire_rate': 500, 'reload_time': 1000, 'offset': pi/24, 'number_of_bullets_in_one_shot': 5, 'path': 'graphics/guns/Ratter.png', 'item_type': ItemType.shotgun, 'bullets': bullets[0]},
    {'name': 'Freeze_ray', 'dmg': 10, 'ammo': 20, 'fire_rate': 90, 'reload_time': 1000, 'offset': pi/24, 'path': 'graphics/guns/Freeze_Ray.png', 'item_type': ItemType.gun, 'bullets': bullets[1]},
    {'name': 'Dragun_fire', 'dmg': 10, 'ammo': 30, 'fire_rate': 150, 'reload_time': 1000, 'offset': pi/18, 'path': 'graphics/guns/Dragun_fire.png', 'item_type': ItemType.gun, 'bullets': bullets[0]},
    {'name': 'Gungine', 'dmg': 10, 'ammo': 100, 'fire_rate': 20, 'reload_time': 5000, 'offset': pi/6, 'path': 'graphics/guns/Gungine.png', 'item_type': ItemType.gun, 'bullets': bullets[0]},
    {'name': 'Proton_backpack', 'dmg': 10, 'ammo': 60, 'fire_rate': 0, 'reload_time': 5000, 'offset': 0, 'path': 'graphics/guns/Proton_backpack.png', 'item_type': ItemType.gun, 'bullets': bullets[0]},
    {'name': 'Slinger', 'dmg': 20, 'ammo': 6, 'fire_rate': 300, 'reload_time': 500, 'offset': pi/18, 'path': 'graphics/guns/Slinger.png', 'item_type': ItemType.gun, 'bullets': bullets[0]},
    {'name': 'Railgun', 'dmg': 6, 'ammo': 50, 'fire_rate': 80, 'reload_time': 2000, 'offset': 0, 'number_of_bullets_in_one_shot': 2, 'path': 'graphics/guns/Railgun.png', 'item_type': ItemType.shotgun_m3, 'bullets': bullets[5]},
    {'name': 'Triple_gun', 'dmg': 10, 'ammo': 3, 'fire_rate': 20, 'reload_time': 100, 'offset': pi/18, 'path': 'graphics/guns/Triple_gun.png', 'item_type': ItemType.gun, 'bullets': bullets[0]},
    {'name': 'AC-15', 'dmg': 9, 'ammo': 10, 'fire_rate': 300, 'reload_time': 1200, 'offset': 0, 'number_of_bullets_in_one_shot': 5, 'path': 'graphics/guns/AC-15.png', 'item_type': ItemType.wallgun, 'bullets': bullets[0]},
    {'name': 'Rubenstein_Monster', 'dmg': 50, 'ammo': 5, 'fire_rate': 700, 'reload_time': 3000, 'offset': 0, 'number_of_bullets_in_one_shot': 2, 'path': 'graphics/guns/Rubenstein_Monster.png', 'item_type': ItemType.shotgun_m3, 'bullets': bullets[7]},
    {'name': 'Fightsabre', 'dmg': 5, 'ammo': 10, 'fire_rate': 180, 'reload_time': 1500, 'offset': 15, 'number_of_bullets_in_one_shot': 5, 'path': 'graphics/guns/Fightsabre.png', 'item_type': ItemType.wallgun, 'bullets': bullets[0]},
    {'name': 'Rc_Rocket', 'dmg': 70, 'ammo': 3, 'fire_rate': 1000, 'reload_time': 2100, 'offset': pi/24, 'path': 'graphics/guns/Rc_Rocket.png', 'item_type': ItemType.gun, 'bullets': bullets[3]},
    {'name': 'Combined_Rifle', 'parts': [16, 17], 'item_type': ItemType.double_gun},
    {'name': 'Combined_Rifle_1', 'dmg': 15, 'ammo': 20, 'fire_rate': 90, 'reload_time': 1500, 'offset': pi/24, 'path': 'graphics/guns/Combined_Rifle_1.png', 'item_type': ItemType.gun, 'bullets': bullets[0]},
    {'name': 'Combined_Rifle_2', 'dmg': 50, 'ammo': 3, 'fire_rate': 600, 'reload_time': 1700, 'offset': pi/24, 'path': 'graphics/guns/Combined_Rifle_2.png', 'item_type': ItemType.gun, 'bullets': bullets[4]},
    {'name': 'PulseCannon', 'dmg': 5, 'ammo': 4, 'fire_rate': 1200, 'reload_time': 1500, 'offset': 0, 'number_of_bullets_in_one_shot': 16, 'path': 'graphics/guns/PulseCannon.png', 'item_type': ItemType.shotgun_m3, 'bullets': bullets[6]},
    {'name': 'Hegemony_Carbine', 'dmg': 40, 'ammo': 5, 'fire_rate': 1000, 'reload_time': 1500, 'offset': pi/24, 'path': 'graphics/guns/Hegemony_Carbine.png', 'item_type': ItemType.gun, 'bullets': bullets[18]},
    {'name': 'Thr_Emperor', 'dmg': 20, 'ammo': 10, 'fire_rate': 350, 'reload_time': 2000, 'offset': pi/12, 'number_of_bullets_in_one_shot': 3, 'path': 'graphics/guns/The_Emperor.png', 'item_type': ItemType.shotgun, 'bullets': bullets[19]},
    {'name': 'BSG', 'dmg': 150, 'ammo': 1, 'fire_rate': 0, 'reload_time': 3500, 'offset': 0, 'path': 'graphics/guns/BSG.png', 'item_type': ItemType.gun, 'bullets': bullets[24]},
    {'name': 'bron_testowa', 'dmg': INFINITY, 'ammo': INFINITY, 'fire_rate': 100, 'reload_time': 200, 'offset': 15, 'number_of_bullets_in_one_shot': 5, 'path': 'graphics/guns/bron_testowa.png', 'item_type': ItemType.wallgun, 'bullets': bullets[0]},
    # enemy guns
    # dungeon
    #19
    {'name': 'Enemy_Gun1', 'dmg': 1, 'ammo': 5, 'fire_rate': 600, 'reload_time': 2500, 'offset': 0, 'path': None, 'item_type': ItemType.gun, 'bullets': bullets[8]},
    {'name': 'Enemy_Gun2', 'dmg': 1, 'ammo': 3, 'fire_rate': 2500, 'reload_time': 4000, 'offset': pi/12, 'number_of_bullets_in_one_shot': 5, 'path': None, 'item_type': ItemType.shotgun, 'bullets': bullets[8]},
    {'name': 'Enemy_Gun3', 'dmg': 1, 'ammo': 2, 'fire_rate': 150, 'reload_time': 4000, 'offset': pi/12, 'number_of_bullets_in_one_shot': 3, 'path': None, 'item_type': ItemType.shotgun, 'bullets': bullets[8]},
    {'name': 'Boss_gun1', 'dmg': 1, 'ammo': 6, 'fire_rate': 1400, 'reload_time': 4000, 'offset': pi/16, 'number_of_bullets_in_one_shot': 32, 'path': None, 'item_type': ItemType.shotgun, 'bullets': bullets[8]},
    {'name': 'Boss_gun2', 'dmg': 1, 'ammo': 200, 'fire_rate': 25, 'reload_time': 4000, 'offset': pi/6, 'path': None, 'item_type': ItemType.gun, 'bullets': bullets[8]},
    # abyss
    {'name': 'Enemy_Gun4', 'dmg': 1, 'ammo': 5, 'fire_rate': 1000, 'reload_time': 3000, 'offset': 0, 'number_of_bullets_in_one_shot': 2, 'path': None, 'item_type': ItemType.shotgun_m3, 'bullets': bullets[9]},
    {'name': 'Enemy_Gun5', 'dmg': 1, 'ammo': 4, 'fire_rate': 1200, 'reload_time': 1500, 'offset': 0, 'number_of_bullets_in_one_shot': 8, 'path': None, 'item_type': ItemType.shotgun_m3, 'bullets': bullets[10]},
    {'name': 'Enemy_Gun6', 'dmg': 1, 'ammo': 1, 'fire_rate': 1500, 'reload_time': 1500, 'offset': pi/12, 'number_of_bullets_in_one_shot': 7, 'path': None, 'item_type': ItemType.shotgun, 'bullets': bullets[11]},
    {'name': 'Boss_gun3', 'dmg': 1, 'ammo': 120, 'fire_rate': 40, 'reload_time': 3000, 'offset': 0, 'number_of_bullets_in_one_shot': 2, 'path': None, 'item_type': ItemType.shotgun_m3, 'bullets': bullets[12]},
    {'name': 'Boss_gun4', 'dmg': 1, 'ammo': 10, 'fire_rate': 500, 'reload_time': 1200, 'offset': 5, 'number_of_bullets_in_one_shot': 15, 'path': None, 'item_type': ItemType.wallgun, 'bullets': bullets[13]},
    # cave
    {'name': 'Enemy_Gun7', 'dmg': 1, 'ammo': 15, 'fire_rate': 250, 'reload_time': 4500, 'offset': pi/24, 'path': None, 'item_type': ItemType.gun, 'bullets': bullets[14]},
    {'name': 'Enemy_Gun8', 'dmg': 1, 'ammo': 7, 'fire_rate': 700, 'reload_time': 3900, 'offset': 0, 'number_of_bullets_in_one_shot': 3, 'path': None, 'item_type': ItemType.wallgun, 'bullets': bullets[14]},
    {'name': 'Enemy_Gun9', 'dmg': 1, 'ammo': 15, 'fire_rate': 600, 'reload_time': 5000, 'offset': pi/12, 'number_of_bullets_in_one_shot': 3, 'path': None, 'item_type': ItemType.shotgun, 'bullets': bullets[15]},
    {'name': 'Boss_gun5', 'dmg': 1, 'ammo': 5, 'fire_rate': 1200, 'reload_time': 3000, 'offset': 0, 'number_of_bullets_in_one_shot': 32, 'path': None, 'item_type': ItemType.shotgun_m3, 'bullets': bullets[16]},
    {'name': 'Boss_gun6', 'dmg': 1, 'ammo': 8, 'fire_rate': 450, 'reload_time': 2000, 'offset': 0, 'number_of_bullets_in_one_shot': 11, 'path': None, 'item_type': ItemType.wallgun, 'bullets': bullets[17]},
     #deepdark
    {'name': 'Enemy_Gun13', 'dmg': 1, 'ammo': 1, 'fire_rate': 0, 'reload_time': 2500, 'offset': 0, 'number_of_bullets_in_one_shot': 1, 'path': None, 'item_type': ItemType.shotgun_m3_last_bullet, 'bullets': (bullets[30], bullets[31])},
    {'name': 'Enemy_Gun14', 'dmg': 1, 'ammo': 5, 'fire_rate': 1000, 'reload_time': 2500, 'offset': pi/16, 'path': None, 'item_type': ItemType.gun, 'bullets': bullets[32]},
    {'name': 'Enemy_Gun15', 'dmg': 1, 'ammo': 7, 'fire_rate': 700, 'reload_time': 3900, 'offset': 10, 'number_of_bullets_in_one_shot': 3, 'path': None, 'item_type': ItemType.wallgun, 'bullets': bullets[33]},
    {'name': 'Boss_gun9', 'dmg': 1, 'ammo': 2, 'fire_rate': 1500, 'reload_time': 4500, 'offset': 0, 'number_of_bullets_in_one_shot': 5, 'path': None, 'item_type': ItemType.shotgun_m3, 'bullets': bullets[27]},
    {'name': 'Boss_gun10', 'dmg': 1, 'ammo': 3, 'fire_rate': 2000, 'reload_time': 3200, 'offset': 0, 'number_of_bullets_in_one_shot': 6, 'path': None, 'item_type': ItemType.shotgun_m3_last_bullet, 'bullets': (bullets[28], bullets[29])},
    #crimson
    {'name': 'Enemy_Gun10', 'dmg': 1, 'ammo': 5, 'fire_rate': 1200, 'reload_time': 3000, 'offset': 0, 'number_of_bullets_in_one_shot': 3, 'path': None, 'item_type': ItemType.shotgun_m3, 'bullets': bullets[20]},
    {'name': 'Enemy_Gun11', 'dmg': 1, 'ammo': 3, 'fire_rate': 1500, 'reload_time': 2000, 'offset': pi/8, 'number_of_bullets_in_one_shot': 3, 'path': None, 'item_type': ItemType.shotgun, 'bullets': bullets[21]},
    {'name': 'Enemy_Gun12', 'dmg': 1, 'ammo': 15, 'fire_rate': 250, 'reload_time': 4500, 'offset': 0, 'path': None, 'item_type': ItemType.gun, 'bullets': bullets[22]},
    {'name': 'Boss_gun11', 'dmg': 1, 'ammo': 3, 'fire_rate': 1400, 'reload_time': 4000, 'offset': pi/16, 'number_of_bullets_in_one_shot': 32, 'path': None, 'item_type': ItemType.shotgun, 'bullets': bullets[34]},
    {'name': 'Boss_gun12', 'dmg': 1, 'ammo': 1, 'fire_rate': 0, 'reload_time': 4500, 'offset': 0, 'path': None, 'item_type': ItemType.gun, 'bullets': bullets[35]},
]

opponents = [
    # dungeon
    {'hp': 50, 'color': colors.white, 'weapon': 23, 'notice_rad': 700, 'speed': 5, 'can_knock': True, 'size': (35, 35)},
    {'hp': 100, 'color': colors.crimson, 'weapon': 24, 'notice_rad': 700, 'speed': 5, 'can_knock': True, 'size': (35, 35)},
    {'hp': 100, 'color': colors.navy_blue, 'weapon': 25, 'notice_rad': 700, 'speed': 5, 'can_knock': True, 'size': (35, 35)},
    # abyss
    {'hp': 100, 'color': colors.dirty_green, 'weapon': 28, 'notice_rad': 1100, 'speed': 5, 'can_knock': True, 'size': (35, 35)},
    {'hp': 150, 'color': colors.dirty_blue, 'weapon': 29, 'notice_rad': 700, 'speed': 5, 'can_knock': True, 'size': (35, 35)},
    {'hp': 150, 'color': colors.sea_green, 'weapon': 30, 'notice_rad': 700, 'speed': 5, 'can_knock': True, 'size': (35, 35)},
    # cave
    {'hp': 150, 'color': colors.white, 'weapon': 33, 'notice_rad': 1100, 'speed': 5, 'can_knock': True, 'size': (35, 35)},
    {'hp': 200, 'color': colors.golden, 'weapon': 34, 'notice_rad': 700, 'speed': 5, 'can_knock': True, 'size': (35, 35)},
    {'hp': 200, 'color': colors.dark_gray, 'weapon': 35, 'notice_rad': 700, 'speed': 5, 'can_knock': True, 'size': (35, 35)},
    # deepdark
    {'hp': 200, 'color': '#83886c', 'weapon': 38, 'notice_rad': 900, 'speed': 5, 'can_knock': True, 'size': (35, 35)},
    {'hp': 220, 'color': '#425a70', 'weapon': 39, 'notice_rad': 900, 'speed': 7, 'can_knock': True, 'size': (35, 35)},
    {'hp': 300, 'color': '#29dfeb', 'weapon': 40, 'notice_rad': 900, 'speed': 5, 'can_knock': True, 'size': (35, 35)},
    # crimson
    {'hp': 150, 'color': '#6f6f6f', 'weapon': 43, 'notice_rad': 900, 'speed': 5, 'can_knock': True, 'size': (35, 35)},
    {'hp': 300, 'color': colors.golden, 'weapon': 44, 'notice_rad': 900, 'speed': 7, 'can_knock': True, 'size': (35, 35)},
    {'hp': 350, 'color': '#6f0000', 'weapon': 45, 'notice_rad': 900, 'speed': 5, 'can_knock': True, 'size': (35, 35)},
]

bosses = [
    # dungeon
    {'hp': 2500, 'weapons': [26, 27], 'notice_rad': 1100, 'speed': 3, 'can_knock': False, 'name': 'brimstone_elemental'},
    # abyss
    {'hp': 3000, 'weapons': [31, 32], 'notice_rad': 1100, 'speed': 4, 'can_knock': False, 'name': 'paguebringer'},
    # cave
    {'hp': 4000, 'weapons': [36, 37], 'notice_rad': 1100, 'speed': 2, 'can_knock': False, 'name': 'crabulon'},
    # deepdark
    {'hp': 6500, 'weapons': [41, 42], 'notice_rad': 1100, 'speed': 2, 'can_knock': False, 'name': 'Ceaseless_Void'},
    # crimson
    {'hp': 6000, 'weapons': [46, 47], 'notice_rad': 1100, 'speed': 0, 'can_knock': False, 'name': 'providence'},
]

stage_data = [
    {'name': 'dungeon', 'key_color': colors.dark_brown, 'opponents': [0, 1, 2], 'bosses': 0, 'stage_type': StageType.normal},
    {'name': 'abyss', 'key_color': colors.seaweed_green, 'opponents': [3, 4, 5], 'bosses': 1, 'stage_type': StageType.normal},
    {'name': 'cave', 'key_color': colors.blue_gray, 'opponents': [6, 7, 8], 'bosses': 2, 'stage_type': StageType.normal},
    {'name': 'deepdark', 'key_color': colors.deepdark_keycolor, 'opponents': [9, 10, 11], 'bosses': 3, 'stage_type': StageType.deepdark},
    {'name': 'crimson', 'key_color': colors.crimson_background, 'opponents': [12, 13, 14], 'bosses': 4, 'stage_type': StageType.normal},
]

item_range = {
    'wooden': [4, 5, 10],
    'sea_prism': [2, 3, 6, 7, 19, 21],
    'golden': [0, 1, 11, 14, 20],
    'nigger': [9, 12, 13, 15, 18]
}

