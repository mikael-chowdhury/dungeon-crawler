from abilities.passives.Passive import Passive
from items.equipment.Rarities import Rarities

from player import player

class LifeBonus(Passive):
    def __init__(self):
        super().__init__("Life Bonus", "lifebonus", Rarities.RARE, ["+10% HP"])

    def apply(self, multiplier):
        new = int(player.max_health * 1.1)
        multiplier = new / player.max_health
        player.max_health = new
        player.health = int(player.health * multiplier)