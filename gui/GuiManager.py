from Manager import Manager

class GuiManager(Manager):
    def __init__(self):
        super().__init__()

        self.current_gui = None

    def draw_gui(self, screen, events, keys, dt, dungeon):
        if self.current_gui is not None:
            self.current_gui.update(screen, events, keys, dt, dungeon)