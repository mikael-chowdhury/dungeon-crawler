from Manager import Manager

class OverlayManager(Manager):
    def __init__(self) -> None:
        super().__init__()

        self.stack = []

    def pop_stack(self):
        self.stack.pop()

    def add_to_stack(self, overlay):
        self.stack.append(overlay)

    def on_top_of_stack(self, overlay):
        return isinstance(self.stack[-1], overlay) if len(self.stack) > 0 else False

    def clear_stack(self):
        self.stack.clear()

    def draw_overlay(self, screen, events, keys, dt, dungeon):
        if len(self.stack) > 0:
            self.stack[-1].update(screen, events, keys, dt, dungeon)