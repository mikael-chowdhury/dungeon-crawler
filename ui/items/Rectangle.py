import pygame
from ui.GuiItem import GuiItem

class Rectangle(GuiItem):
    def __init__(self, gui, x, y, w, h, colour) -> None:
        super().__init__(gui, x, y, w, h)

        self.colour = colour

    def update(self, screen, events, keys, dt, dungeon):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.w, self.h))