from abilities.passives.Passive import Passive
from items.equipment.Rarities import Rarities

from player import player

class LifeBonus(Passive):
    def __init__(self):
        super().__init__("Life Bonus", "lifebonus", Rarities.RARE, ["+10% HP"])

    def apply(self, multiplier):
        player.max_health = int(player.max_health * 1.1)