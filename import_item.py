from gun import FragmentationGun, FragmentationShotgun, Gun, Shotgun, ShotgunM3, WallGun, Railgun, GildedHydra, IceBraker, RocketLauncher, DoubleGun
from modifier import Modifier
from settings import ItemType, weapon
from enum import Enum

def import_item(owner:Enum, item_index:int=None) -> Gun:
    if item_index == None:
        item = Modifier()
    else:
        weapon_data = weapon[item_index]
        if weapon_data['item_type'] == ItemType.gun:
            item = Gun(owner, weapon_data)
        elif weapon_data['item_type'] == ItemType.shotgun:
            item = Shotgun(owner, weapon_data)
        elif weapon_data['item_type'] == ItemType.wallgun:
            item = WallGun(owner, weapon_data)
        elif weapon_data['item_type'] == ItemType.railgun:
            item = Railgun(owner, weapon_data)
        elif weapon_data['item_type'] == ItemType.gilded_hydra:
            item = GildedHydra(owner, weapon_data)
        elif weapon_data['item_type'] == ItemType.ice_braker:
            item = IceBraker(owner, weapon_data)
        elif weapon_data['item_type'] == ItemType.rocket_launcher:
            item = RocketLauncher(owner, weapon_data)
        elif weapon_data['item_type'] == ItemType.double_gun:
            item = DoubleGun(owner, weapon_data, import_items(owner, weapon_data['parts']))
        elif weapon_data['item_type'] == ItemType.shotgun_m3:
            item = ShotgunM3(owner, weapon_data)
        elif weapon_data['item_type'] == ItemType.fragment_gun:
            item = FragmentationGun(owner, weapon_data)
        elif weapon_data['item_type'] == ItemType.fragment_shotgun:
            item = FragmentationShotgun(owner, weapon_data)
    return item

def import_items(owner:Enum, item_index_list:list) -> list[Gun]:
    item_list = []
    for item_index in item_index_list:
        item_list.append(import_item(owner, item_index))
    return item_list
        