from abilities.passives.Passive import Passive
from items.Item import Item

class Loot():
    def __init__(self, loot) -> None:
        self.loot = loot

class LootPassive(Loot):
    def __init__(self, passive:Passive) -> None:
        self.loot = passive

class LootItem(Loot):
    def __init__(self, item:Item) -> None:
        self.loot = item