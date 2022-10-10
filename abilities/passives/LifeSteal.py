from abilities.passives.Passive import Passive
from items.equipment.Rarities import Rarities

class LifeSteal(Passive):
    def __init__(self):
        super().__init__("Life Steal", "lifesteal", Rarities.MYTHICAL, ["every attack your hp goes up by 5% of", "the damage dealt (stackable)"])

    def apply(self, multiplier, player):
        player.lifesteal += 0.05