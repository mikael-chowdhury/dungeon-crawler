from loot.Loot import Loot, LootItem, LootPassive
from rarity.Rarities import Rarities, Rarity
from rarity.RaritySpread import RaritySpread

import random

class LootTable():
    def __init__(self, lootlist=[], rarity_spread=RaritySpread.DEFAULT) -> None:
        self.lootlist: list[LootItem|LootPassive] = lootlist
        self.rarity_spread = rarity_spread

    def get_items_of_rarity(self, rarity:Rarity):
        return [x for x in self.lootlist if x.loot.rarity == rarity]

    def get_random_item(self):
        # rarity = Rarities.get_random_rarity(spread=self.rarity_spread)
        # item = random.choice(self.get_items_of_rarity(rarity))
        # return item
        pass