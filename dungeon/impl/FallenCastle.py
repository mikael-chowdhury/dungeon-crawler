import pygame
from dungeon.Dungeon import Dungeon
from entities.monster.Monster import Monster
from entities.monster.impl.Knight import Knight
from entities.monster.impl.Zombie import Zombie
from util.ResourceLocation import ResourceLocation

from entities.monster.impl.Wizard import Wizard

class FallenCastle(Dungeon):
    def __init__(self):
        super().__init__("Fallen Castle", 0)

        self.floor = pygame.transform.smoothscale(pygame.image.load(ResourceLocation("assets/tiles/castle_floor.jpg")), (self.tile_size, self.tile_size)).convert_alpha()

        # self.monster_supply.add_multiple(Knight, 3)
        self.monster_supply.add_multiple(Wizard, 1)