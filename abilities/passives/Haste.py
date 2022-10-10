from abilities.passives.Passive import Passive
from items.equipment.Rarities import Rarities

class Haste(Passive):
    def __init__(self):
        super().__init__("Haste", "haste", Rarities.EPIC, ["+20% movement speed (stackable)"])

    def apply(self, multiplier, player):
        player.speed *= 1.2