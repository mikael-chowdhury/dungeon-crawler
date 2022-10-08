import pygame
from items.equipment.equipment import Equipment
from ui.GuiItem import GuiItem

from ui.items.Button import Button
from ui.items.ToolTip import ToolTip

class InventoryItemToolTip(GuiItem):
    def __init__(self, gui, x, y, item:Equipment, index, on_equip) -> None:
        super().__init__(gui, x, y, 125, 150)

        self.item = item

        self.index = index

        self.on_equip = on_equip

        self.equipbutton = Button(None, self.x, self.y, self.w, 50, text="equip", on_click=self.click)

        self.tt = None

    def click(self, *args):
        if isinstance(self.tt, ToolTip):
            self.tt.activated = False
        self.on_equip(self.item, self.index, *args)

    def update(self, screen, events, keys, dt, dungeon, tt:ToolTip):
        self.tt = tt

        super().update(screen, events, keys, dt, dungeon)

        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h))

        self.equipbutton.update(screen, events, keys, dt, dungeon)