import os
import pygame

from items.equipment.Rarities import Rarity

class Passive:
    def __init__(self, name, icon_path, rarity:Rarity, modifications:list[str]):
        self.name = name

        self.applied = False

        self.level = 1

        self.rarity = rarity

        self.modifications = modifications

        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "textures", "abilities", "passives", icon_path + ".png")), (64, 64))
        self.previewimage = pygame.transform.scale(pygame.image.load(os.path.join("assets", "textures", "abilities", "passives", icon_path + ".png")), (224, 224))

    def apply(self, multiplier, player):
        self.applied = True

    def update(self, screen, events, keys, dt, dungeon):
        pass