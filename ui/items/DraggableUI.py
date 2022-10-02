import uuid
import pygame
from ui.GuiItem import GuiItem

class DraggableUI(GuiItem):
    def __init__(self, gui, x, y, w, h, center=(None, None), background_colour=(255, 255, 255), background_image=None, text="Default Text", text_font="Arial", text_colour=(0, 0, 0), font_size=24, is_sys_font=True, no_text=False, locks=[], on_lock=lambda: None) -> None:
        super().__init__(gui, x, y, w, h, center, background_colour, background_image, text, text_font, text_colour, font_size, is_sys_font, no_text)

        self.drag = False
        self.mousedown = False

        self.id = uuid.uuid4()

        self.start = x, y

        self.before = pygame.mouse.get_pos()

        self.locks = locks

        self.rect = pygame.Rect(x, y, w, h)

        self.on_lock = on_lock

        self.mousex = pygame.mouse.get_pos()[0]
        self.mousey = pygame.mouse.get_pos()[1]
    
    def update(self, screen, events, keys, dt, dungeon):
        super().update(screen, events, keys, dt, dungeon)

        if self.mouse_hovering() and not self.mousedown:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousedown = True

                    self.start = self.x, self.y

                    self.before = pygame.mouse.get_pos()

        if self.mousedown:
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    self.drag = True
                    
                    self.x += event.pos[0] - self.before[0]
                    self.y += event.pos[1] - self.before[1]
                    self.before = event.pos
                    self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
                    self.mousex = event.pos[0]
                    self.mousey = event.pos[1]
                
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mousedown = False

                    if self.drag:
                        self.drag = False

                        locked = False
                        for lock in self.locks:
                            if lock.collidepoint(self.mousex, self.mousey):
                                if lock.x != self.x or lock.y != self.y:
                                    self.x = lock.x
                                    self.y = lock.y
                                    locked = True
                                    self.on_lock(self, (lock.x, lock.y))
                                    break

                        if not locked:
                            self.x = self.start[0]
                            self.y = self.start[1]