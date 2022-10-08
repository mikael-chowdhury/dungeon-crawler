import pygame

class Passive:
    def __init__(self, name, icon_path):
        self.name = name
        self.icon = pygame.image.load(icon_path).convert_alpha()

        self.applied = False

        self.level = 1

    def apply(self, multiplier):
        self.applied = True

    def update(self, screen, events, keys, dt, dungeon):
        pass