import pygame
from ui.GuiItem import GuiItem

class Button(GuiItem):
    def __init__(self, gui, x, y, w, h, on_click, center=None, background_colour=(255, 255, 255), background_image=None, text="Default Text", text_font="Arial", text_colour=(0, 0, 0), font_size=24, is_sys_font=True) -> None:
        super().__init__(gui, x, y, w, h, center, background_colour, background_image, text, text_font, text_colour, font_size, is_sys_font)

        self.on_click = on_click

    def update(self, screen, events, keys, dt, dungeon):
        super().update(screen, events, keys, dt, dungeon)

        if self.mouse_hovering():
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.on_click(screen, events, keys, dt, dungeon)