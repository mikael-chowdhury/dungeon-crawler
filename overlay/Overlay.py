class Overlay:
    def __init__(self):
        self.gui_items = []

    def update(self, screen, events, keys, dt, dungeon):
        for gui_item in self.gui_items:
            gui_item.update(screen, events, keys, dt, dungeon)