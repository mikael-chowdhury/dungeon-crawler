import pygame
from items.Item import Item
from ui.GuiItem import GuiItem

class Slot(GuiItem):
    def __init__(self, gui, x, y, item:Item|None) -> None:
        super().__init__(gui, x, y, 50, 50, no_text=True, no_background=True)

        self.item = item

    def update(self, screen, events, keys, dt, dungeon):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.w, self.h), 1)

        if isinstance(self.item, Item):
            if "image" in self.item.__dict__.keys():
                screen.blit(self.item.image, (self.x, self.y))