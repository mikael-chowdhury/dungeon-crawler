from copy import deepcopy
import os
import random
import uuid

import pygame

from rarity.Rarities import Rarities


class Item:
    def __init__(self, json, basejson) -> None:
        self.basejson = deepcopy(basejson)
        self.set_base()

        self.json = json

        self.rarity = Rarities.get_random_rarity()

        self.level = 0
        self.upgradecost = 1000

        self.uuid = uuid.uuid4()

        self.rand_multiplier = self.random_decimal(0.95, 1.15)
        
        if "texture" in dict(json).keys():
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "textures", "items", json["texture"] + ".png")), (50, 50))
            self.previewimage = pygame.transform.scale(pygame.image.load(os.path.join("assets", "textures", "items", json["texture"] + ".png")), (224, 224))

    def set_base(self):
        for key in self.basejson.keys():
            setattr(self, key, self.basejson[key])
            
    def random_decimal(self, start, stop):
        return random.randrange(start*1000, stop*1000)/1000