import pygame
from font.FontManager import FontManager
from items.Item import Item
from items.equipment.equipment import Equipment
from overlay.Overlay import Overlay
import config

from player import player
from ui.GuiItem import GuiItem
from ui.items.InventoryEquipmentToolTip import InventoryEquipmentToolTip
from ui.items.InventoryItemToolTip import InventoryItemToolTip
from ui.items.Slot import Slot
from ui.items.ToolTip import ToolTip

from Manager import Manager

class InventoryOverlay(Overlay):
    def __init__(self):
        super().__init__()

        self.top_padding = 300
        self.left_padding = 100

        self.spacing = 5

        self.tile_size = 50

        self.first_load = True

        self.rects = []

        self.hoveringItem = player.inventory.items[0]

        self.lastclickpos = 0, 0
    
        self.selectedItem = player.inventory.items[0]
        self.selectedSlotPos = None

        self.titlefont = FontManager.VT323_42
        self.subtitlefont = FontManager.VT323_32
        self.statfont = FontManager.VT323_24
        
        self.selectedItemTitleText = self.getSelectedItemTitleText()
        self.selectedItemImage = self.getSelectedItemImage()
        self.selectedItemRarityText = self.getSelectedItemRarityText()
        
        self.propertiesHeader = self.subtitlefont.render("Properties", config.ANTIALIASING, (255, 0, 0))
        self.selectedItemProperties = self.getSelectedItemProperties("get_player_buffs")

        self.attributesHeader = self.subtitlefont.render("Attributes", config.ANTIALIASING, (255, 0, 0))
        self.selectedItemAttributes = self.getSelectedItemProperties("get_modifiers")

        self.helmetslot = None
        self.chestplateslot = None
        self.bootsslot = None
        self.spellbookslot = None
        self.weaponslot = None

        self.inventoryslots:list[Slot] = []

    def item_equip(self, item, index, *args):
        type = item.json["type"].lower()

        before = getattr(player.inventory.equipment, type)

        setattr(player.inventory.equipment, type, item)
        player.inventory.set_item(index, None)
        self.inventoryslots[index].item = None
        self.inventoryslots[index].tooltip = None

        if isinstance(before, Equipment):
            i = player.inventory.give_item(before)
            self.inventoryslots[i].item = before

    def item_unequip(self, item, *args):
        type = item.json["type"].lower()
        setattr(player.inventory.equipment, type, None)
        index = player.inventory.give_item(item)
        self.inventoryslots[index].item = item

    def draw_equipment(self, screen, item, rect):
        extracted_item = getattr(player.inventory.equipment, item)

        if isinstance(extracted_item, Equipment):
            if "image" in extracted_item.__dict__.keys():
                img = extracted_item.image
                screen.blit(img, img.get_rect(center=rect.center))

    def getSelectedItemTitleText(self):
        return self.titlefont.render(self.selectedItem.json["name"] if isinstance(self.selectedItem, Item) else "", config.ANTIALIASING, self.selectedItem.rarity.colour if isinstance(self.selectedItem, Item) else (255, 0, 0))

    def getSelectedItemImage(self) -> pygame.Surface|None:
        image = self.selectedItem.previewimage if isinstance(self.selectedItem, Item) and "previewimage" in self.selectedItem.__dict__.keys() else None

        # if isinstance(image, pygame.Surface):
        #     temp = image.copy()
        #     temp.fill((*(player.inventory.items[self.selectedItemIndex].rarity.colour if isinstance(player.inventory.items[self.selectedItemIndex], Equipment) else (255, 0, 0)), config.ITEM_RARITY_BLEND_AMOUNT), special_flags=config.ITEM_RARITY_BLEND)
        #     temp.fill((255, 255, 255, config.ITEM_ADDITIONAL_LIGHTENING), special_flags=pygame.BLEND_RGBA_MULT)
        #     image = temp

        return image

    def getSelectedItemRarityText(self) -> pygame.Surface|None:
        return self.subtitlefont.render(self.selectedItem.rarity.name, config.ANTIALIASING, self.selectedItem.rarity.colour) if isinstance(self.selectedItem, Item) else None

    def getSelectedItemProperties(self, call:str) -> list[pygame.Surface]:
        propertystrings = []

        if isinstance(self.selectedItem, Item):
            pb = getattr(self.selectedItem, call)()

            propertystrings = [str(x).replace("_", " ") + " " + str(pb[x]).replace("*", "x") for i, x in enumerate(pb.keys())]

        propertiestexts = [self.statfont.render(propertiesstr, config.ANTIALIASING, (255, 0, 0)) for propertiesstr in propertystrings if propertiesstr != ""]

        return propertiestexts

    def update(self, screen, events, keys, dt, dungeon):
        _x = 0
        _y = 0

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.lastclickpos = event.pos

        mousepos = pygame.mouse.get_pos()
        mousex = mousepos[0]
        mousey = mousepos[1]

        for slot in [x for x in self.gui_items if isinstance(x, Slot)]:
            if isinstance(slot.item, Item):
                rect = pygame.Rect(slot.x, slot.y, self.tile_size, self.tile_size)

                tooltips = [not (x.tooltip.mouse_hovering_tooltip() and x.tooltip.activated) for x in self.gui_items if isinstance(x, GuiItem) and isinstance(x.tooltip, ToolTip)]

                if(all(tooltips)):
                    if rect.collidepoint(mousex, mousey):
                        self.hoveringItem = slot.item

                    if rect.collidepoint(*self.lastclickpos):
                        self.lastclickpos = (-1000, -1000)
                        self.selectedSlotPos = (rect.x, rect.y)
                        self.selectedItem = slot.item
                        self.selectedItemTitleText = self.getSelectedItemTitleText()
                        self.selectedItemImage = self.getSelectedItemImage()
                        self.selectedItemRarityText = self.getSelectedItemRarityText()
                        self.selectedItemProperties = self.getSelectedItemProperties("get_player_buffs")
                        self.selectedItemAttributes = self.getSelectedItemProperties("get_modifiers")
                    
        for item_number, item in enumerate(player.inventory.items):
            if item_number % 9 == 0:
                _y += 1
                _x = 0

            _x += 1

            x = _x * self.tile_size + self.left_padding + self.spacing*_x
            y = _y*self.tile_size + self.top_padding + self.spacing*_y

            rect = pygame.Rect(x, y, self.tile_size, self.tile_size)

            self.rects.append(rect)

            if self.first_load:
                slot = Slot(self, x, y, item)

                if isinstance(item, Equipment):
                    slot.apply_tooltip(ToolTip(slot, [InventoryItemToolTip(None, x+self.tile_size, y+self.tile_size, item, item_number, lambda *args: self.item_equip(*args))]))

                self.inventoryslots.append(slot)

        for slotnum, slot in enumerate(self.inventoryslots):
            if slot.tooltip is None:
                if isinstance(player.inventory.items[slotnum], Equipment):
                    slot.apply_tooltip(ToolTip(slot, [InventoryItemToolTip(None, slot.x+self.tile_size, slot.y+self.tile_size, player.inventory.items[slotnum], slotnum, lambda *args: self.item_equip(*args))]))

        equipmentrect = pygame.Rect(0, 0, 250, 325)
        equipmentrect.left = 25
        equipmentrect.centery = 175

        if self.helmetslot is not None:
            self.helmetslot.item = player.inventory.equipment.helmet
            if self.helmetslot.item is not None:
                if self.helmetslot.tooltip is None:
                    self.helmetslot.apply_tooltip(ToolTip(self.helmetslot, [InventoryEquipmentToolTip(None, self.helmetslot.x+self.tile_size, self.helmetslot.y+self.tile_size, player.inventory.equipment.helmet, lambda *args: self.item_unequip(*args))]))
            else:
                self.helmetslot.tooltip = None

        if self.chestplateslot is not None:
            self.chestplateslot.item = player.inventory.equipment.chestplate
            if self.chestplateslot.item is not None:
                if self.chestplateslot.tooltip is None:
                    self.chestplateslot.apply_tooltip(ToolTip(self.chestplateslot, [InventoryEquipmentToolTip(None, self.chestplateslot.x+self.tile_size, self.chestplateslot.y+self.tile_size, player.inventory.equipment.chestplate, lambda *args: self.item_unequip(*args))]))
            else:
                self.chestplateslot.tooltip = None

        if self.bootsslot is not None:
            self.bootsslot.item = player.inventory.equipment.boots
            if self.bootsslot.item is not None:
                if self.bootsslot.tooltip is None:
                    self.bootsslot.apply_tooltip(ToolTip(self.bootsslot, [InventoryEquipmentToolTip(None, self.bootsslot.x+self.tile_size, self.bootsslot.y+self.tile_size, player.inventory.equipment.boots, lambda *args: self.item_unequip(*args))]))
            else:
                self.bootsslot.tooltip = None

        if self.weaponslot is not None:
            self.weaponslot.item = player.inventory.equipment.weapon
            if self.weaponslot.item is not None:
                if self.weaponslot.tooltip is None:
                    self.weaponslot.apply_tooltip(ToolTip(self.weaponslot, [InventoryEquipmentToolTip(None, self.weaponslot.x+self.tile_size, self.weaponslot.y+self.tile_size, player.inventory.equipment.weapon, lambda *args: self.item_unequip(*args))]))
            else:
                self.weaponslot.tooltip = None

        if self.spellbookslot is not None:
            self.spellbookslot.item = player.inventory.equipment.spell_book
            if self.spellbookslot.item is not None:
                if self.spellbookslot.tooltip is None:
                    self.spellbookslot.apply_tooltip(ToolTip(self.spellbookslot, [InventoryEquipmentToolTip(None, self.spellbookslot.x+self.tile_size, self.spellbookslot.y+self.tile_size, player.inventory.equipment.spell_book, lambda *args: self.item_unequip(*args))]))
            else:
                self.spellbookslot.tooltip = None
                
        if self.first_load:
            helmetrect = pygame.Rect(0, 0, 50, 50)
            helmetrect.centerx = equipmentrect.centerx
            helmetrect.centery = equipmentrect.top + (equipmentrect.centery-equipmentrect.top)/2
            self.helmetslot = Slot(self, helmetrect.x, helmetrect.y, player.inventory.equipment.helmet)

            chestplaterect = pygame.Rect(0, 0, 50, 50)
            chestplaterect.centerx = equipmentrect.centerx
            chestplaterect.top = helmetrect.bottom + 5
            self.chestplateslot = Slot(self, chestplaterect.x, chestplaterect.y, player.inventory.equipment.chestplate)

            bootsrect = pygame.Rect(0, 0, 50, 50)
            bootsrect.centerx = equipmentrect.centerx
            bootsrect.top = chestplaterect.bottom + 5
            self.bootsslot = Slot(self, bootsrect.x, bootsrect.y, player.inventory.equipment.boots)

            weaponrect = pygame.Rect(0, 0, 50, 50)
            weaponrect.right = chestplaterect.left - 5
            weaponrect.centery = chestplaterect.centery
            self.weaponslot = Slot(self, weaponrect.x, weaponrect.y, player.inventory.equipment.weapon)

            spellbookrect = pygame.Rect(0, 0, 50, 50)
            spellbookrect.left = chestplaterect.right + 5
            spellbookrect.centery = chestplaterect.centery
            self.spellbookslot = Slot(self, spellbookrect.x, spellbookrect.y, player.inventory.equipment.spell_book)

        statrect = pygame.Rect(0, 0, 250, 325)
        statrect.centerx = 400
        statrect.centery = 175

        titlerect = self.selectedItemTitleText.get_rect(centerx=statrect.centerx, centery=statrect.top+45)
        screen.blit(self.selectedItemTitleText, titlerect)

        if isinstance(self.selectedItemImage, pygame.Surface):
            imagerect = self.selectedItemImage.get_rect(centerx=statrect.centerx, top=titlerect.bottom)
            screen.blit(self.selectedItemImage, imagerect)

            if isinstance(self.selectedItemRarityText, pygame.Surface):
                raritytextrect = self.selectedItemRarityText.get_rect(centerx=statrect.centerx, centery=imagerect.bottom+15)
                screen.blit(self.selectedItemRarityText, raritytextrect)

        propertiesheaderrect = self.propertiesHeader.get_rect(left=statrect.right+50, top=titlerect.top)
        if self.selectedItemProperties.__len__() > 0:
            screen.blit(self.propertiesHeader, propertiesheaderrect)

        propertiesrect = pygame.Rect(statrect.right + 50, titlerect.bottom, 100, propertiesheaderrect.height)

        for index, property in enumerate(self.selectedItemProperties):
            if isinstance(property, pygame.Surface):
                statsrect = property.get_rect(left=statrect.right + 50, top=propertiesheaderrect.bottom+15+(index*25))
                propertiesrect.height += statsrect.height
                screen.blit(property, statsrect)

        attributesheaderrect = self.attributesHeader.get_rect(left=statrect.right+50, top=propertiesrect.bottom+35)
        if self.selectedItemAttributes.__len__() > 0:
            screen.blit(self.attributesHeader, attributesheaderrect)

        attributesrect = pygame.Rect(statrect.right + 50, propertiesrect.bottom+30, 100, 0)

        for index, attribute in enumerate(self.selectedItemAttributes):
            if isinstance(attribute, pygame.Surface):
                statsrect = attribute.get_rect(left=statrect.right + 25, top=attributesheaderrect.bottom+15+(index*25))
                attributesrect.height += statsrect.height
                screen.blit(attribute, statsrect)

        super().update(screen, events, keys, dt, dungeon)

        if self.selectedSlotPos is not None:
            pygame.draw.rect(screen, (255, 255, 255), (self.selectedSlotPos[0], self.selectedSlotPos[1], 50, 50), 1)

        for tooltip in [x.tooltip for x in self.gui_items if isinstance(x, Slot)]:
            if tooltip is not None:
                tooltip.update(screen, events, keys, dt, dungeon)

        self.first_load = False