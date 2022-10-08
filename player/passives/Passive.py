import pygame


from player import player

class Passive:
    def __init__(self, name, icon_path):
        self.name = name
        self.icon = pygame.image.load(icon_path).convert_alpha()

        self.level = 1

    def apply(self, multiplier):
        pass

    def update(self, screen, events, keys, dt, dungeon):
        pass