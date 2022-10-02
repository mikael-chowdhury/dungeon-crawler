from config import ANTIALIASING
from gui.Gui import Gui
from gui.impl.GuiGame import GuiGame

from ui.items.Button import Button
from ui.items.TextBox import TextBox

from Manager import Manager

class GuiDungeonSelect(Gui):
    def __init__(self):
        super().__init__()

        self.gui_manager = Manager.get_manager("GuiManager")

        self.current_dungeon = 0

        self.dungeon_manager = Manager.get_manager("DungeonManager")

        self.dungeon_right = Button(self, 0, 0, 100, 25, center=(500, 200), background_colour=(255, 255, 255), text="->", on_click= lambda *args: self.right())
        self.dungeon_left = Button(self, 0, 0, 100, 25, center=(300, 200), background_colour=(255, 255, 255), text="<-", on_click= lambda *args: self.left())
        self.play_button = Button(self, 0, 0, 100, 25, center=(400, 600), background_colour=(255, 255, 255), text="play", on_click=lambda *args: self.play())

        self.heading = TextBox(self, 0, 0, 100, 100, (400, 125), text=self.dungeon_manager.dungeons[self.current_dungeon].name, font_size=64)

    def update_heading_text(self):
        if self.current_dungeon < len(self.dungeon_manager.dungeons):
            self.heading.set_text(self.dungeon_manager.dungeons[self.current_dungeon].name)

    def left(self):
        self.current_dungeon -= 1
        if self.current_dungeon == -1:
            self.current_dungeon = 0

        else:
            self.update_heading_text()

    def right(self):
        self.current_dungeon += 1
        if self.current_dungeon >= len(self.dungeon_manager.dungeons):
            self.current_dungeon = len(self.dungeon_manager.dungeons) - 1
        else:
            self.update_heading_text()

    def play(self):
        self.dungeon_manager.current_dungeon = self.dungeon_manager.dungeons[self.current_dungeon]
        self.dungeon_manager.current_dungeon.load_monsters()
        self.gui_manager.current_gui=GuiGame()

    def update(self, screen, events, keys, dt, dungeon):
        screen.fill((0, 0, 0))

        self.dungeon_right.update(screen, events, keys, dt, dungeon)
        self.dungeon_left.update(screen, events, keys, dt, dungeon)

        self.heading.update(screen, events, keys, dt, dungeon)

        self.play_button.update(screen, events, keys, dt, dungeon)