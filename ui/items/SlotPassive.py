import pygame
from ui.GuiItem import GuiItem

from abilities.passives.Passive import Passive

class SlotPassive(GuiItem):
    def __init__(self, gui, x, y, passive:Passive|None) -> None:
        super().__init__(gui, x, y, 64, 64, no_text=True, no_background=True)

        self.passive = passive

    def update(self, screen, events, keys, dt, dungeon):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.w, self.h), 1)

        if isinstance(self.passive, Passive):
            if "image" in self.passive.__dict__.keys():
                screen.blit(self.passive.image, (self.x, self.y))