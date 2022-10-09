from abilities.passives.Passive import Passive
from items.equipment.Rarities import Rarities

from player import player

class Berserker(Passive):
    def __init__(self):
        super().__init__("Berserker", "berserker", Rarities.EPIC, ["+20% attack damage", "+20% attack speed"])

    def apply(self, multiplier):
        player.physical_damage = player.physical_damage * 1.2
        player.attackspeedmultiplier = player.attackspeedmultiplier * 1.2