from abilities.passives.Passive import Passive
from items.equipment.Rarities import Rarities

class Berserker(Passive):
    def __init__(self):
        super().__init__("Berserker", "berserker", Rarities.EPIC, ["+20% attack damage (stackable)", "+20% attack speed (stackable)"])

    def apply(self, multiplier, player):
        player.physical_damage = player.physical_damage * 1.2
        player.attackspeedmultiplier = player.attackspeedmultiplier * 1.2

        super().apply(multiplier, player)