import pygame

from ui.GuiItem import GuiItem

class ToolTip:
    def __init__(self, triggeritem:GuiItem, guiitems:list) -> None:
        self.guiitems = guiitems
        self.activated = False

        self.triggeritem = triggeritem

        self.x, self.y, self.w, self.h = self.getmetrics(guiitems)

    def getmetrics(self, guiitems:list):
        x = min([x.x for x in guiitems])
        y = min([x.y for x in guiitems])
        w = max([x.x+x.w for x in guiitems])-x
        h = max([x.y+x.h for x in guiitems])-y

        print(x, y, w, h)

        return x, y, w, h

    def mouse_hovering(self):
        x,y = pygame.mouse.get_pos()

        tx = self.triggeritem.x
        ty = self.triggeritem.y
        tw = self.triggeritem.w
        th = self.triggeritem.h

        return x >= tx and x <= tx + tw and y >= ty and y <= ty + th

    def mouse_hovering_tooltip(self):
        x, y = pygame.mouse.get_pos()

        return x >= self.x and x <= self.x + self.w and y >= self.y and y <= self.y + self.h

    def update(self, screen, events, keys, dt, dungeon)->bool:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mouse_hovering():
                    if event.button == 3:
                        self.activated = True
                else:
                    if self.mouse_hovering_tooltip() and self.activated:
                        self.activated = True
                    else:
                        self.activated = False

        if self.activated:
            for guiitem in self.guiitems:
                guiitem.update(screen, events, keys, dt, dungeon)

        return self.activated