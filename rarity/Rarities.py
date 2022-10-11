import random

from rarity.RaritySpread import RaritySpread

class Rarity():
    def __init__(self, name, colour, multiplier) -> None:
        self.name = name
        self.colour = colour
        self.multiplier = multiplier

class Rarities:
    JUNK = Rarity("JUNK", (126, 126, 126), 1)
    UNCOMMON = Rarity("UNCOMMON", (48, 169, 21), 1.5)
    RARE = Rarity("RARE", (0, 146, 209), 1.75)
    EPIC = Rarity("EPIC", (229, 0, 255), 2)
    LEGENDARY = Rarity("LEGENDARY", (208, 132, 0), 2.5)
    MYTHICAL = Rarity("MYTHICAL", (128, 0, 255), 5)

    RARITIES = [JUNK, UNCOMMON, RARE, EPIC, LEGENDARY, MYTHICAL]

    @staticmethod
    def get_random_rarity(spread=RaritySpread.DEFAULT)->Rarity:
        _list = []

        for index, rarity in enumerate(Rarities.RARITIES):
            for _ in range(spread[index]):
                _list.append(rarity)

        return random.choice(_list)