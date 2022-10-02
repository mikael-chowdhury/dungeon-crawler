from equipment.equipment import Equipment
from util.ResourceLocation import ResourceLocation

from json import load

class Armour(Equipment):
    def __init__(self, name, json) -> None:
        super().__init__(json, load(open(ResourceLocation("assets/playerdata/default-weapon-stats.json"))))

        self.json = json
        self.name = name

    def instance(self):
        return Armour(self.name, self.json)
    
    @staticmethod
    def load_data_from_file(armour_name):
        return load(open(ResourceLocation(f"assets/itemdata/{armour_name}.json"))) 

    @staticmethod
    def fromRegistryName(name:str):
        return Armour(name, Armour.load_data_from_file(name))