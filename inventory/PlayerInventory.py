import pygame

from items.equipment.equipment import Equipment

from inventory.EntityInventory import EntityInventory

class PlayerInventory(EntityInventory):
    def __init__(self):
        super().__init__(45)

    def update_inventory(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        super().update_inventory(screen, events, keys, dt, dungeon, cameraX, cameraY)