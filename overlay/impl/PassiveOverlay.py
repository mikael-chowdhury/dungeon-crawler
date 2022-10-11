import pygame
from abilities.passives.Passive import Passive
from overlay.Overlay import Overlay

from player import player
from ui.GuiItem import GuiItem
from ui.items.PassiveMenuEquippedToolTip import PassiveMenuEquippedToolTip
from ui.items.PassiveMenuInventoryToolTip import PassiveMenuInventoryToolTip
from ui.items.SlotPassive import SlotPassive
from ui.items.ToolTip import ToolTip

from font.FontManager import FontManager

import config

class PassiveOverlay(Overlay):
    def __init__(self):
        super().__init__()

        self.passiveslot1 = None
        self.passiveslot2 = None
        self.passiveslot3 = None
        self.passiveslot4 = None
        self.passiveslot5 = None

        self.awaitingselection = False
        self.awaitingselection_passive = None
        self.awaitingselection_inventory_index = -1

        self.lastclickpos = 0, 0

        self.selectedItem = player.passiveInventory[0]
        self.selectedSlotPos = None

        self.titlefont = FontManager.VT323_32
        self.subtitlefont = FontManager.VT323_24
        self.statfont = FontManager.VT323_16
        
        self.selectedItemTitleText = self.getSelectedItemTitleText()
        self.selectedItemImage = self.getSelectedItemImage()
        self.selectedItemRarityText = self.getSelectedItemRarityText()
        self.selectedItemProperties = self.getSelectedItemProperties()

        self.tile_size = 64

        self.top_padding = 300
        self.left_padding = 25

        self.spacing = 5

        self.rects = []

        self.inventoryslots:list[SlotPassive] = []

        self.first_load = True

    def passive_equip(self, passive:Passive, index, *args):
        self.awaitingselection = True
        self.awaitingselection_passive = passive
        self.awaitingselection_inventory_index = index

    def passive_unequip(self, passive:Passive, index, *args):
        for i, slot in enumerate(self.inventoryslots):
            if slot.passive is None:
                passive.applied = False
                slot.passive = passive
                player.passiveInventory[i] = passive
                break

        new:SlotPassive = [*[getattr(self, f"passiveslot{index+1}")]][0]
        new.passive = None
        new.tooltip = None
        player.passives[index] = None

        setattr(self, f"passiveslot{index+1}", new)

    def getSelectedItemTitleText(self):
        return self.titlefont.render(self.selectedItem.name if isinstance(self.selectedItem, Passive) else "", config.ANTIALIASING, self.selectedItem.rarity.colour if isinstance(self.selectedItem, Passive) else (255, 0, 0))

    def getSelectedItemImage(self) -> pygame.Surface|None:
        image = self.selectedItem.previewimage if isinstance(self.selectedItem, Passive) and "previewimage" in self.selectedItem.__dict__.keys() else None
        return image

    def getSelectedItemRarityText(self) -> pygame.Surface|None:
        return self.subtitlefont.render(self.selectedItem.rarity.name, config.ANTIALIASING, self.selectedItem.rarity.colour) if isinstance(self.selectedItem, Passive) else None

    def getSelectedItemProperties(self) -> list[pygame.Surface]:
        propertystrings = []

        if isinstance(self.selectedItem, Passive):
            propertystrings = self.selectedItem.modifications

        propertiestexts = [self.statfont.render(propertiesstr, config.ANTIALIASING, (255, 0, 0)) for propertiesstr in propertystrings if propertiesstr != ""]

        return propertiestexts

    def update(self, screen, events, keys, dt, dungeon): 
        global player

        _x = 0
        _y = 0

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.lastclickpos = event.pos

        mousepos = pygame.mouse.get_pos()
        mousex = mousepos[0]
        mousey = mousepos[1]

        for slot in [x for x in self.gui_items if isinstance(x, SlotPassive)]:
            if isinstance(slot.passive, Passive):
                rect = pygame.Rect(slot.x, slot.y, 64, 64)

                tooltips = [not (x.tooltip.mouse_hovering_tooltip() and x.tooltip.activated) for x in self.gui_items if isinstance(x, GuiItem) and isinstance(x.tooltip, ToolTip)]

                if(all(tooltips)):
                    if rect.collidepoint(mousex, mousey):
                        self.hoveringItem = slot.passive

                    if rect.collidepoint(*self.lastclickpos):
                        self.lastclickpos = (-1000, -1000)
                        self.selectedSlotPos = (rect.x, rect.y)
                        self.selectedItem = slot.passive
                        self.selectedItemTitleText = self.getSelectedItemTitleText()
                        self.selectedItemImage = self.getSelectedItemImage()
                        self.selectedItemRarityText = self.getSelectedItemRarityText()
                        self.selectedItemProperties = self.getSelectedItemProperties()

        if self.awaitingselection:
            for i in range(5):
                selection = getattr(self, f"passiveslot{i+1}")

                if isinstance(selection, SlotPassive):
                    rect = pygame.Rect(selection.x, selection.y, selection.w, selection.h)

                    if rect.collidepoint(self.lastclickpos[0], self.lastclickpos[1]):
                        self.lastclickpos = (-1000, -1000)
                        new = [*[selection]][0]

                        self.awaitingselection_passive.apply(1, player)

                        new.passive = self.awaitingselection_passive
                        setattr(self, f"passiveslot{i+1}", new)
                        player.passives[i] = self.awaitingselection_passive
                        self.inventoryslots[self.awaitingselection_inventory_index].passive = None
                        self.inventoryslots[self.awaitingselection_inventory_index].tooltip = None
                        player.passiveInventory[self.awaitingselection_inventory_index] = None

                        self.awaitingselection = False

        for item_number, item in enumerate(player.passiveInventory):
            if item_number % 9 == 0:
                _y += 1
                _x = 0

            _x += 1

            x = _x * self.tile_size + self.left_padding + self.spacing*_x
            y = _y*self.tile_size + self.top_padding + self.spacing*_y

            rect = pygame.Rect(x, y, self.tile_size, self.tile_size)

            self.rects.append(rect)

            if self.first_load:
                slot = SlotPassive(self, x, y, item)

                if isinstance(item, Passive):
                    slot.apply_tooltip(ToolTip(slot, [PassiveMenuInventoryToolTip(None, x+self.tile_size, y+self.tile_size, item, item_number, lambda *args: self.passive_equip(*args))]))

                self.inventoryslots.append(slot)

        for slotnum, slot in enumerate(self.inventoryslots):
            if slot.tooltip is None:
                if isinstance(player.passiveInventory[slotnum], Passive):
                    slot.apply_tooltip(ToolTip(slot, [PassiveMenuInventoryToolTip(None, slot.x+self.tile_size, slot.y+self.tile_size, player.passiveInventory[slotnum], slotnum, lambda *args: self.passive_equip(*args))]))

        if self.passiveslot1 is not None:
            self.passiveslot1.passive = player.passives[0]
            if self.passiveslot1.passive is not None:
                if self.passiveslot1.tooltip is None:
                    self.passiveslot1.apply_tooltip(ToolTip(self.passiveslot1, [PassiveMenuEquippedToolTip(None, self.passiveslot1.x+self.tile_size, self.passiveslot1.y+self.tile_size, player.passives[0], 0, lambda *args: self.passive_unequip(*args))]))
            else:
                self.passiveslot1.tooltip = None

        if self.passiveslot2 is not None:
            self.passiveslot2.passive = player.passives[1]
            if self.passiveslot2.passive is not None:
                if self.passiveslot2.tooltip is None:
                    self.passiveslot2.apply_tooltip(ToolTip(self.passiveslot2, [PassiveMenuEquippedToolTip(None, self.passiveslot2.x+self.tile_size, self.passiveslot2.y+self.tile_size, player.passives[1], 1, lambda *args: self.passive_unequip(*args))]))
            else:
                self.passiveslot2.tooltip = None

        if self.passiveslot3 is not None:
            self.passiveslot3.passive = player.passives[2]
            if self.passiveslot3.passive is not None:
                if self.passiveslot3.tooltip is None:
                    self.passiveslot3.apply_tooltip(ToolTip(self.passiveslot3, [PassiveMenuEquippedToolTip(None, self.passiveslot3.x+self.tile_size, self.passiveslot3.y+self.tile_size, player.passives[2], 2, lambda *args: self.passive_unequip(*args))]))
            else:
                self.passiveslot3.tooltip = None

        if self.passiveslot4 is not None:
            self.passiveslot4.passive = player.passives[3]
            if self.passiveslot4.passive is not None:
                if self.passiveslot4.tooltip is None:
                    self.passiveslot4.apply_tooltip(ToolTip(self.passiveslot4, [PassiveMenuEquippedToolTip(None, self.passiveslot4.x+self.tile_size, self.passiveslot4.y+self.tile_size, player.passives[3], 3, lambda *args: self.passive_unequip(*args))]))
            else:
                self.passiveslot4.tooltip = None

        if self.passiveslot5 is not None:
            self.passiveslot5.passive = player.passives[4]
            if self.passiveslot5.passive is not None:
                if self.passiveslot5.tooltip is None:
                    self.passiveslot5.apply_tooltip(ToolTip(self.passiveslot5, [PassiveMenuEquippedToolTip(None, self.passiveslot5.x+self.tile_size, self.passiveslot5.y+self.tile_size, player.passives[4], 4, lambda *args: self.passive_unequip(*args))]))
            else:
                self.passiveslot5.tooltip = None

        propertiesRect = pygame.Rect(0, 0, 300, 300)
        propertiesRect.right = screen.get_rect().right - 15
        propertiesRect.top = 15

        if self.selectedItemTitleText is not None:
            rect = self.selectedItemTitleText.get_rect(left=propertiesRect.x, y=propertiesRect.y+15)
            screen.blit(self.selectedItemTitleText, rect)

            for index, property in enumerate(self.selectedItemProperties):
                if isinstance(property, pygame.Surface):
                    statsrect = property.get_rect(left=propertiesRect.x, top=rect.bottom+15+(index*25))
                    propertiesRect.height += statsrect.height
                    screen.blit(property, statsrect)

        rect = pygame.Rect(0, 0, 370, 100)
        rect.centery = 200
        rect.centerx = 200

        xadd = 0

        for i, passive in enumerate(player.passives):
            if not isinstance(getattr(self, f"passiveslot{i+1}"), SlotPassive):
                slot = SlotPassive(self, rect.x+xadd, rect.y, passive)

                if passive is not None:
                    slot.apply_tooltip(ToolTip(slot, [PassiveMenuEquippedToolTip(None, slot.x+slot.w, slot.y+slot.h, passive, i, lambda *args: self.passive_unequip(*args))]))

                setattr(self, f"passiveslot{i+1}", slot)

            xadd += 64+10

        super().update(screen, events, keys, dt, dungeon)

        for p in [x for x in [self.passiveslot1, self.passiveslot2, self.passiveslot3, self.passiveslot4, self.passiveslot5] if isinstance(x, SlotPassive)]:
            if isinstance(p, SlotPassive):
                p.update(screen, events, keys, dt, dungeon)

                if isinstance(p.tooltip, ToolTip):
                    p.tooltip.update(screen, events, keys, dt, dungeon)

            pygame.draw.rect(screen, (255, 0, 0), (p.x, p.y, p.w, p.h), 1)

        for tooltip in [x.tooltip for x in self.gui_items if isinstance(x, SlotPassive)]:
            if tooltip is not None:
                tooltip.update(screen, events, keys, dt, dungeon)

        self.first_load = False