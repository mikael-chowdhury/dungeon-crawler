import pygame
from equipment.equipment import Equipment
from ui.GuiItem import GuiItem

from ui.items.Button import Button

class InventoryItemToolTip(GuiItem):
    def __init__(self, gui, x, y, item:Equipment, on_equip) -> None:
        super().__init__(gui, x, y, 125, 150)

        self.item = item

        self.on_equip = on_equip

        self.equipbutton = Button(None, self.x, self.y, self.w, 50, text="test", on_click=lambda *args: self.on_equip(self.item, *args))

    def update(self, screen, events, keys, dt, dungeon):
        super().update(screen, events, keys, dt, dungeon)

        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h))

        self.equipbutton.update(screen, events, keys, dt, dungeon)