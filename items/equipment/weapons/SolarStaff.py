import pygame
from items.equipment.weapons.Weapon import Weapon

from aoe.AreaOfEffect import AreaOfEffect

class SolarStaff(Weapon):
    def __init__(self) -> None:
        super().__init__(Weapon.load_data_from_file("SolarStaff"))

        self.effects:list[AreaOfEffect] = []

    def create_effect(self, x, y):
        self.effects.append(AreaOfEffect(x, y, 100))

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.create_effect(*event.pos)

        for effect in self.effects:
            effect.update(screen, events, keys, dt, dungeon, cameraX, cameraY)