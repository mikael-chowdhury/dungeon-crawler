from copy import deepcopy
from equipment.Stat import Stat
from equipment.equipment import Equipment
from inventory.Inventory import Inventory

class EntityEquipment:
    def __init__(self):
        self.helmet = None
        self.chestplate = None
        self.leggings = None
        self.boots = None
        self.spell_book = None
        self.weapon = None

    def get_equipment(self):
        return [getattr(self, x) for x in dir(self) if isinstance(getattr(self, x), Equipment)]

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        for equipment in self.get_equipment():
            equipment.update(screen, events, keys, dt, dungeon, cameraX, cameraY)

class EntityInventory(Inventory):
    def __init__(self, size=10):
        super().__init__(size)

        self.equipment = EntityEquipment()

        self.equipped_index = 0
        self.equipped_item = self.items[self.equipped_index]

        self.loaded_stat_boosters = []

        self.hotbar = self.items[:5]

    def set_item(self, index, item):
        self.items[index] = item

        if index == self.equipped_index:
            self.equipped_item = self.items[self.equipped_index]

    def applystat(self, stat, equipment, player, key, obj, default):
        stat_object = {stat: equipment.json[key][stat]}
        
        before = deepcopy(getattr(obj, stat))

        setattr(obj, stat, eval(str(default[stat]) + stat_object[stat]+f"*{equipment.rarity.multiplier}*{equipment.rand_multiplier}"))

        if stat.startswith("max_"):
            _stat = stat.replace("max_", "")

            after = getattr(player, stat)

            multiplier = after/before

            if not _stat in equipment.__dict__.keys():
                setattr(player, _stat, getattr(player, _stat)*multiplier)
            else:
                setattr(equipment, _stat, getattr(equipment, _stat)*multiplier)

    def load_stat_boosters(self, player):
        player.reset_stats()

        for equipment in self.equipment.get_equipment()+[self.equipped_item]:
            if equipment is not None:
                if "player-buffs" in equipment.json.keys():
                    for stat in equipment.json["player-buffs"].keys():
                        self.applystat(stat, equipment, player, "player-buffs", player, player.DEFAULT_STATS)

                if "modifiers" in equipment.json.keys():
                    for stat in equipment.json["modifiers"].keys():
                        self.applystat(stat, equipment, player, "modifiers", equipment, equipment.basejson)
        
    def update_inventory(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        self.hotbar = self.items[:5]
        self.equipment.update(screen, events, keys, dt, dungeon, cameraX, cameraY)