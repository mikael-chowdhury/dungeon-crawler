import pygame
from items.equipment.weapons.Weapon import Weapon

from aoe.AreaOfEffect import AreaOfEffect

from player import player

class SolarStaff(Weapon):
    def __init__(self) -> None:
        super().__init__(Weapon.load_data_from_file("SolarStaff"))

        self.effects:list[AreaOfEffect] = []

    def create_effect(self, x, y):
        self.effects.append(AreaOfEffect(x, y, 100, "ring-of-fire"))

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.mana >= 20:
                    self.create_effect(*event.pos)
                    player.mana -= 20

        for effect in self.effects:
            effect.update(screen, events, keys, dt, dungeon, cameraX, cameraY)