from Manager import Manager

import os

from util.ResourceLocation import ResourceLocation
import importlib

class DungeonManager(Manager):
    def __init__(self):
        super().__init__()
        self.current_dungeon = None

        self.dungeons = self.get_dungeons()

    def get_dungeons(self):
        dungeons = []
        for file in os.listdir(ResourceLocation("dungeon/impl")):
            if file.endswith(".py"):
                name = file.replace('.py', '')
                module = importlib.import_module(f"dungeon.impl")
                dungeon = getattr(module, name)
                if type(dungeon) == type:
                    dungeons.append(dungeon())
        
        return dungeons

    def draw_current_dungeon(self, screen, events, keys, dt, no_draw=False):
        if self.current_dungeon is not None:
            self.current_dungeon.update(screen, events, keys, dt, no_draw=no_draw)