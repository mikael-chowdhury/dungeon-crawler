import random

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

    RARITIES = [(JUNK, 50), (UNCOMMON, 20), (RARE, 15), (EPIC, 10), (LEGENDARY, 4), (MYTHICAL, 1)]

    @staticmethod
    def get_random_rarity()->Rarity:
        _list = []

        for rarity in Rarities.RARITIES:
            for _ in range(rarity[1]):
                _list.append(rarity[0])

        return random.choice(_list)