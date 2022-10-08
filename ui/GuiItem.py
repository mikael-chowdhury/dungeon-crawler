import uuid
import pygame

from config import ANTIALIASING

class GuiItem:
    def __init__(self, gui, x, y, w, h, center=(None, None), background_colour=(255, 255, 255), background_image=None, text="Default Text", text_font="Arial", text_colour=(0, 0, 0), font_size=24, is_sys_font=True, no_text=False) -> None:
        self.gui = gui

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.center = center

        self.background_colour = background_colour
        self.background_image = background_image 

        self.text = text
        self.text_font = text_font
        self.text_colour = text_colour
        self.font_size = font_size
        self.is_sys_font = is_sys_font
        self.no_text = no_text

        self.uuid = uuid.uuid4()

        self.tooltip = None

        if isinstance(self.center, tuple) and self.center.__len__() == 2 and self.center[0] != None and self.center[1] != None:
            rect = pygame.Rect(self.x, self.y, self.w, self.h)
            rect.center = self.center
            self.x = rect.x
            self.y = rect.y

        if not no_text:
            if self.is_sys_font:
                self.font = pygame.font.SysFont(self.text_font, self.font_size)

            else:
                self.font = pygame.font.Font(self.text_font, self.font_size)

            self.pre_rendered_text = self.font.render(self.text, ANTIALIASING, self.text_colour)

        if gui is not None:
            gui.gui_items.append(self)

    def apply_tooltip(self, tooltip):
        self.tooltip = tooltip

    def set_text(self, text):
        self.text = text
        self.pre_rendered_text = self.font.render(self.text, ANTIALIASING, self.text_colour)

    def scale_image(self):
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.w, self.h))

    def update(self, screen, events, keys, dt, dungeon):
        if self.background_image is not None:
            screen.blit(self.background_image, (self.x, self.y))

        else:
            if self.background_colour is not None:
                pygame.draw.rect(screen, self.background_colour, (self.x, self.y, self.w, self.h))

        if self.text != "" and not self.no_text:
            background = pygame.Rect(self.x, self.y, self.w, self.h)
            text_rect = self.pre_rendered_text.get_rect()
            text_rect.center = background.center

            screen.blit(self.pre_rendered_text, text_rect)

        if self.tooltip is not None:
            self.tooltip.update(screen, events, keys, dt, dungeon)

    def mouse_hovering(self):
        x, y = pygame.mouse.get_pos()

        return x>=self.x and x<=self.x+self.w and y>=self.y and y<=self.y+self.h