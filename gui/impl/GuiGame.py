import pygame
from abilities.passives.Berserker import Berserker
from abilities.passives.LifeBonus import LifeBonus
from gui.Gui import Gui
from Manager import Manager
from init.ItemInit import ItemInit
from overlay.impl.InventoryOverlay import InventoryOverlay
from overlay.impl.PassiveOverlay import PassiveOverlay

from player import player

class GuiGame(Gui):
    def __init__(self):
        super().__init__()

        player.inventory.equipment.helmet = ItemInit.COPPER_HELMET
        player.inventory.equipment.chestplate = ItemInit.COPPER_CHESTPLATE
        player.inventory.equipment.boots = ItemInit.COPPER_BOOTS

        player.inventory.equipment.weapon = ItemInit.COPPER_SWORD

        player.passives[0] = Berserker()
        player.passives[1] = LifeBonus()

        player.passiveInventory[0] = Berserker()
        player.passiveInventory[1] = LifeBonus()

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
                        self.overlay_manager.clear_stack()
                        self.overlay_manager.add_to_stack(InventoryOverlay())

                if event.key == pygame.K_u:
                    if self.overlay_manager.on_top_of_stack(PassiveOverlay):
                        self.overlay_manager.pop_stack()
                    else:
                        self.overlay_manager.clear_stack()
                        self.overlay_manager.add_to_stack(PassiveOverlay())

        screen.fill((0, 0, 0))

        self.dungeon_manager.draw_current_dungeon(screen, events, keys, dt, no_draw=len(self.overlay_manager.stack) > 0)