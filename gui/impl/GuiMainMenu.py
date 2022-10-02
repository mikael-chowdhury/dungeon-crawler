from gui.Gui import Gui
from gui.impl.GuiDungeonSelect import GuiDungeonSelect

from ui.items.Button import Button

from Manager import Manager

class GuiMainMenu(Gui):
    def __init__(self):
        super().__init__()

        self.gui_manager = Manager.get_manager("GuiManager")

        self.play_button = Button(self, 0, 0, 100, 25, center=(400, 400), background_colour=(255, 255, 255), text="Play", on_click= lambda *args: self.play())

    def play(self):
        self.gui_manager.current_gui=GuiDungeonSelect()

    def update(self, screen, events, keys, dt, dungeon):
        screen.fill((0, 0, 0))

        self.play_button.update(screen, events, keys, dt, dungeon)