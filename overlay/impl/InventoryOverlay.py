from copy import deepcopy
import random
import pygame
from equipment.equipment import Equipment
from overlay.Overlay import Overlay
import config

from player import player
from ui.GuiItem import GuiItem

class InventoryOverlay(Overlay):
    def __init__(self):
        super().__init__()

        self.top_padding = 300
        self.left_padding = 100

        self.spacing = 5

        self.tile_size = 50

        self.first_load = True

        self.rects = []

        self.hoveringItemIndex = 0
        self.hoveringItem = player.inventory.items[0]

        self.selectedItemIndex = 0
        self.selectedItem = player.inventory.items[0]

        self.lastclickpos = 0, 0

        self.titlefont = pygame.font.SysFont("Arial", 32)
        self.subtitlefont = pygame.font.SysFont("Arial", 24)
        self.statfont = pygame.font.SysFont("Arial", 16)
        
        self.selectedItemTitleText = self.getSelectedItemTitleText()
        self.selectedItemImage = self.getSelectedItemImage()
        self.selectedItemRarityText = self.getSelectedItemRarityText()
        
        self.propertiesHeader = self.subtitlefont.render("Properties", config.ANTIALIASING, (255, 0, 0))
        self.selectedItemProperties = self.getSelectedItemProperties("get_player_buffs")

        self.attributesHeader = self.subtitlefont.render("Attributes", config.ANTIALIASING, (255, 0, 0))
        self.selectedItemAttributes = self.getSelectedItemProperties("get_modifiers")

    def getSelectedItemTitleText(self):
        return self.titlefont.render(player.inventory.items[self.selectedItemIndex].json["name"] if isinstance(player.inventory.items[self.selectedItemIndex], Equipment) else "", config.ANTIALIASING, self.selectedItem.rarity.colour if isinstance(self.selectedItem, Equipment) else (255, 0, 0))

    def getSelectedItemImage(self) -> pygame.Surface|None:
        image = player.inventory.items[self.selectedItemIndex].previewimage if isinstance(player.inventory.items[self.selectedItemIndex], Equipment) else None

        # if isinstance(image, pygame.Surface):
        #     temp = image.copy()
        #     temp.fill((*(player.inventory.items[self.selectedItemIndex].rarity.colour if isinstance(player.inventory.items[self.selectedItemIndex], Equipment) else (255, 0, 0)), config.ITEM_RARITY_BLEND_AMOUNT), special_flags=config.ITEM_RARITY_BLEND)
        #     temp.fill((255, 255, 255, config.ITEM_ADDITIONAL_LIGHTENING), special_flags=pygame.BLEND_RGBA_MULT)
        #     image = temp

        return image

    def getSelectedItemRarityText(self) -> pygame.Surface|None:
        return self.subtitlefont.render(player.inventory.items[self.selectedItemIndex].rarity.name, config.ANTIALIASING, player.inventory.items[self.selectedItemIndex].rarity.colour) if isinstance(player.inventory.items[self.selectedItemIndex], Equipment) else None

    def getSelectedItemProperties(self, call:str) -> list[pygame.Surface]:
        propertystrings = []

        if isinstance(self.selectedItem, Equipment):
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
        
        for item_number, item in enumerate(player.inventory.items):
            if item_number % 9 == 0:
                _y += 1
                _x = 0

            _x += 1

            x = _x * self.tile_size + self.left_padding + self.spacing*_x
            y = _y*self.tile_size + self.top_padding + self.spacing*_y

            mousepos = pygame.mouse.get_pos()
            mousex = mousepos[0]
            mousey = mousepos[1]

            rect = pygame.Rect(x, y, self.tile_size, self.tile_size)

            if rect.collidepoint(mousex, mousey):
                self.hoveringItem = item
                self.hoveringItemIndex = item_number

            if rect.collidepoint(*self.lastclickpos):
                self.lastclickpos = (-1000, -1000)
                self.selectedItem:Equipment = item
                self.selectedItemIndex = item_number
                self.selectedItemTitleText = self.getSelectedItemTitleText()
                self.selectedItemImage = self.getSelectedItemImage()
                self.selectedItemRarityText = self.getSelectedItemRarityText()
                self.selectedItemProperties = self.getSelectedItemProperties("get_player_buffs")
                self.selectedItemAttributes = self.getSelectedItemProperties("get_modifiers")

            if self.selectedItemIndex == item_number:
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)
            elif self.hoveringItemIndex == item_number:
                pygame.draw.rect(screen, (255, 165, 165), rect, 1)
            else:
                pygame.draw.rect(screen, (255, 0, 0), rect, 1)

            self.rects.append(rect)

            if self.first_load:
                if isinstance(item, Equipment):
                    if "image" in item.__dict__.keys():
                        # temp = item.image.copy()
                        # temp.fill((*item.rarity.colour, config.ITEM_RARITY_BLEND_AMOUNT), special_flags=config.ITEM_RARITY_BLEND)
                        # temp.fill((255, 255, 255, config.ITEM_ADDITIONAL_LIGHTENING), special_flags=pygame.BLEND_RGBA_MULT)
                        self.gui_items.append(GuiItem(self, x, y, self.tile_size, self.tile_size, background_image=item.image, text=""))

        statrect = pygame.Rect(0, 0, 250, 325)
        statrect.centerx = 400
        statrect.centery = 175

        titlerect = self.selectedItemTitleText.get_rect(centerx=statrect.centerx, centery=statrect.top+45)
        screen.blit(self.selectedItemTitleText, titlerect)

        if isinstance(self.selectedItemImage, pygame.Surface):
            imagerect = self.selectedItemImage.get_rect(centerx=statrect.centerx, top=titlerect.bottom+10)
            screen.blit(self.selectedItemImage, imagerect)

            if isinstance(self.selectedItemRarityText, pygame.Surface):
                raritytextrect = self.selectedItemRarityText.get_rect(centerx=statrect.centerx, centery=imagerect.bottom+15)
                screen.blit(self.selectedItemRarityText, raritytextrect)

        propertiesheaderrect = self.propertiesHeader.get_rect(left=statrect.right+25, top=titlerect.top)
        if self.selectedItemProperties.__len__() > 0:
            screen.blit(self.propertiesHeader, propertiesheaderrect)

        propertiesrect = pygame.Rect(statrect.right + 25, titlerect.bottom, 100, propertiesheaderrect.height)

        for index, property in enumerate(self.selectedItemProperties):
            if isinstance(property, pygame.Surface):
                statsrect = property.get_rect(left=statrect.right + 25, top=propertiesheaderrect.bottom+15+(index*25))
                propertiesrect.height += statsrect.height
                screen.blit(property, statsrect)

        attributesheaderrect = self.attributesHeader.get_rect(left=statrect.right+25, top=propertiesrect.bottom+35)
        if self.selectedItemAttributes.__len__() > 0:
            screen.blit(self.attributesHeader, attributesheaderrect)

        attributesrect = pygame.Rect(statrect.right + 25, propertiesrect.bottom+30, 100, 0)

        for index, attribute in enumerate(self.selectedItemAttributes):
            if isinstance(attribute, pygame.Surface):
                statsrect = attribute.get_rect(left=statrect.right + 25, top=attributesheaderrect.bottom+15+(index*25))
                attributesrect.height += statsrect.height
                screen.blit(attribute, statsrect)

        pygame.draw.rect(screen, (255, 0, 0), statrect, 1)

        super().update(screen, events, keys, dt, dungeon)

        self.first_load = False