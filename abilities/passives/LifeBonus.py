from math import ceil
from abilities.passives.Passive import Passive
from rarity.Rarities import Rarities

class LifeBonus(Passive):
    def __init__(self):
        super().__init__("Life Bonus", "lifebonus", Rarities.RARE, ["+10% HP (stackable)"])

    def apply(self, multiplier, player):        
        new = player.max_health * 1.1
        multiplier = ceil(new) / ceil(player.max_health)

        player.max_health = ceil(new)

        if not self.applied:
            player.health = int(player.health * round(multiplier, 1))

        super().apply(multiplier, player)