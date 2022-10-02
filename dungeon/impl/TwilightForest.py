import pygame

from util.ResourceLocation import ResourceLocation

from dungeon.Dungeon import Dungeon

from entities.monster.impl.Wizard import Wizard
from entities.monster.impl.Zombie import Zombie

class TwilightForest(Dungeon):
    def __init__(self):
        super().__init__("Twilight Forest", 25)

        self.floor = pygame.transform.smoothscale(pygame.image.load(ResourceLocation("assets/tiles/castle_floor.jpg")), (self.tile_size, self.tile_size)).convert_alpha()

        self.width = 25
        self.height = 25

        self.monster_supply.add_multiple(Wizard, 10)
        self.monster_supply.add_multiple(Zombie, 20)