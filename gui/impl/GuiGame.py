import pygame
from gui.Gui import Gui
from Manager import Manager
from init.ItemInit import ItemInit
from overlay.impl.InventoryOverlay import InventoryOverlay

from player import player

class GuiGame(Gui):
    def __init__(self):
        super().__init__()
        player.inventory.set_item(0, ItemInit.HOLY_BLADE.instance())
        player.inventory.set_item(1, ItemInit.FIERY_BLADE.instance())
        player.inventory.set_item(2, ItemInit.ARCTIC_BLADE.instance())
        player.inventory.set_item(3, ItemInit.OCEANIC_BLADE.instance())
        player.inventory.set_item(4, ItemInit.BREATHING_BLADE.instance())

        player.inventory.equipment.helmet = ItemInit.BREATHING_HELMET.instance()

        player.inventory.equipment.chestplate = ItemInit.HOLY_CHESTPLATE.instance()
        player.inventory.load_stat_boosters(player)

        self.dungeon_manager = Manager.get_manager("DungeonManager")
        self.overlay_manager = Manager.get_manager("OverlayManager")

        self.clock = Manager.get_field("clock")

        w = self.dungeon_manager.current_dungeon.width * self.dungeon_manager.current_dungeon.tile_size
        h = self.dungeon_manager.current_dungeon.height * self.dungeon_manager.current_dungeon.tile_size

        player.cameraX = w/2 - 300
        player.cameraY = h/2 - 300

    def update(self, screen, events, keys, dt, dungeon):
        super().update(screen, events, keys, dt, dungeon)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    if self.overlay_manager.on_top_of_stack(InventoryOverlay):
                        self.overlay_manager.pop_stack()
                    else:
                        self.overlay_manager.add_to_stack(InventoryOverlay())

        screen.fill((0, 0, 0))

        self.dungeon_manager.draw_current_dungeon(screen, events, keys, dt, no_draw=len(self.overlay_manager.stack) > 0)