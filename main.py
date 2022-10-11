from Manager import Manager
from config import ANTIALIASING
from dungeon.DungeonManager import DungeonManager
from font.FontManager import FontManager
from gui.GuiManager import GuiManager
from overlay.OverlayManager import OverlayManager
from gui.impl.GuiMainMenu import GuiMainMenu

import pygame

pygame.init()

screen = pygame.display.set_mode((800, 800), pygame.DOUBLEBUF, 16)

pygame.event.set_allowed([pygame.MOUSEWHEEL, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.KEYDOWN, pygame.QUIT])

isRunning = True

dungeon_manager = DungeonManager()
gui_manager = GuiManager()
overlay_manager = OverlayManager()
font_manager = FontManager()

gui_manager.current_gui = GuiMainMenu()

clock = pygame.time.Clock()
Manager.set_field("clock", clock)

fps_font = FontManager.VT323_64

while isRunning:
    dt = clock.tick()

    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            isRunning = False

    gui_manager.draw_gui(screen, events, keys, dt, dungeon_manager.current_dungeon)

    fps_text = fps_font.render(str(int(clock.get_fps())), ANTIALIASING, (255, 0, 0))
    rect = fps_text.get_rect(right=800, bottom=800)
    screen.blit(fps_text,rect)

    overlay_manager.draw_overlay(screen, events, keys, dt, dungeon_manager.current_dungeon)

    pygame.display.update()