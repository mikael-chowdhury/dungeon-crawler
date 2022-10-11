import pygame
from font.FontManager import FontManager
from gui.Gui import Gui
from gui.GuiManager import GuiManager

from ui.items.Button import Button

import config

class GuiGameOver(Gui):
    def __init__(self):
        super().__init__()

        self.title_font = FontManager.VT323_48
        self.game_over_text = self.title_font.render("Game Over", config.ANTIALIASING, (255, 255, 255))

        self.main_menu = Button(self, 0, 0, 150, 100, self.main_menu_click, center=(400, 450), background_colour=(255, 255, 255), text="main menu")
    
    def main_menu_click(self, *args):
        from Manager import Manager
        from gui.impl.GuiMainMenu import GuiMainMenu
        from player import player
        guimanager:GuiManager = Manager.get_manager("GuiManager")
        player.is_dead = False
        player.health = player.max_health
        guimanager.current_gui = GuiMainMenu()

    def update(self, screen, events, keys, dt, dungeon):
        screen.fill((0, 0, 0))

        super().update(screen, events, keys, dt, dungeon)

        self.main_menu.update(screen, events, keys, dt, dungeon)

        rect = self.game_over_text.get_rect(center=(400, 250))
        screen.blit(self.game_over_text, rect)