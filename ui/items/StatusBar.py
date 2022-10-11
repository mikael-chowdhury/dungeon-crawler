import pygame
from config import ANTIALIASING
from font.FontManager import FontManager
from ui.GuiItem import GuiItem

class StatusBar(GuiItem):
    def __init__(self, gui, x, y, w, h, center=(None, None), background_colour=(255, 255, 255), background_image=None, bar_colour=(0, 255, 0), status=0, total=0, line_start=0, line_end=0) -> None:
        super().__init__(gui, x, y, w, h, center, background_colour, background_image, no_text=True)

        self.bar_colour = bar_colour
        
        self.status = status
        self.total = total
        self.line_start = line_start
        self.line_end = line_end

        self.font = FontManager.VT323_24

    def update(self, screen, events, keys, dt, dungeon):
        percent = (self.status/self.total)
        pygame.draw.line(screen, self.bar_colour, (self.x+self.line_start, self.y+self.h/2), (self.x+self.line_start+self.line_end*percent, self.y+self.h/2), 5)

        text_surf = self.font.render(str(int(self.status)) + "/" + str(int(self.total)), ANTIALIASING, self.bar_colour)
        rect = text_surf.get_rect(centery=self.y+self.h/2)
        screen.blit(text_surf, (self.x + self.line_start + self.line_end + 25, rect.y))
        super().update(screen, events, keys, dt, dungeon)