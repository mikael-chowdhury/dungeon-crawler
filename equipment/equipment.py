from copy import deepcopy
import os
import random
import pygame

from equipment.Rarities import Rarities


class Equipment:
    def __init__(self, json, basejson) -> None:
        self.basejson = deepcopy(basejson)
        self.set_base()

        self.json = json

        self.rarity = Rarities.get_random_rarity()

        self.level = 0
        self.upgradecost = 1000

        self.rand_multiplier = self.random_decimal(0.95, 1.15)
        
        if "texture" in dict(json).keys():
            self.image = pygame.transform.smoothscale(pygame.image.load(os.path.join("assets", "models", json["texture"] + ".png")), (50, 50))
            self.previewimage = pygame.transform.smoothscale(pygame.image.load(os.path.join("assets", "models", json["texture"] + ".png")), (200, 200))

    def set_base(self):
        for key in self.basejson.keys():
            setattr(self, key, self.basejson[key])
    
    def random_decimal(self, start, stop):
        return random.randrange(start*1000, stop*1000)/1000

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        pass

    def get_player_buffs(self):
        return self.json["player-buffs"] if "player-buffs" in self.json.keys() else {}

    def get_modifiers(self) -> dict:
        return self.json["modifiers"] if "modifiers" in self.json.keys() else {}