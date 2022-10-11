from items.equipment.armour.Armour import Armour
from items.equipment.weapons.SolarStaff import SolarStaff
from items.equipment.weapons.Weapon import Weapon

class ItemInit:
    COPPER_HELMET = Armour.fromRegistryName("CopperHelmet")
    COPPER_CHESTPLATE = Armour.fromRegistryName("CopperChestplate")
    COPPER_BOOTS = Armour.fromRegistryName("CopperBoots")
    COPPER_SWORD = Weapon.fromRegistryName("CopperSword")

    SOLAR_STAFF = SolarStaff()