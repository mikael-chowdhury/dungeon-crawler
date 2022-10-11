import pygame
from items.equipment.weapons.Weapon import Weapon

class SolarStaff(Weapon):
    def __init__(self) -> None:
        super().__init__(Weapon.load_data_from_file("SolarStaff"))

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                circle = 