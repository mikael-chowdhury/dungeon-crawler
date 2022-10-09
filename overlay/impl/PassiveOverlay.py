import pygame
from abilities.passives.Passive import Passive
from overlay.Overlay import Overlay

from player import player
from ui.items.PassiveMenuEquippedToolTip import PassiveMenuEquippedToolTip
from ui.items.SlotPassive import SlotPassive
from ui.items.ToolTip import ToolTip

class PassiveOverlay(Overlay):
    def __init__(self):
        super().__init__()

        self.passiveslot1 = None
        self.passiveslot2 = None
        self.passiveslot3 = None
        self.passiveslot4 = None
        self.passiveslot5 = None

    def passive_unequip(self, passive:Passive, *args):
        print(passive.name)

    def update(self, screen, events, keys, dt, dungeon):
        screen.fill((0, 0, 0))

        rect = pygame.Rect(0, 0, 370, 100)
        rect.centery = 200
        rect.centerx = 200

        xadd = 0

        for i, passive in enumerate(player.passives):
            if passive is not None:
                if not isinstance(getattr(self, f"passiveslot{i+1}"), SlotPassive):
                    slot = SlotPassive(self, rect.x+xadd, rect.y, passive)
                    slot.apply_tooltip(ToolTip(slot, [PassiveMenuEquippedToolTip(None, slot.x+slot.w, slot.y+slot.h, passive, lambda *args: self.passive_unequip(*args))]))

                    setattr(self, f"passiveslot{i+1}", slot)
            else:
                setattr(self, f"passiveslot{i+1}", None)

            xadd += 64+10

        pygame.draw.rect(screen, (255, 0, 0), rect, 1)

        for p in [x for x in [self.passiveslot1, self.passiveslot2, self.passiveslot3, self.passiveslot4, self.passiveslot5] if isinstance(x, SlotPassive)]:
            if isinstance(p, SlotPassive):
                p.update(screen, events, keys, dt, dungeon)

                if isinstance(p.tooltip, ToolTip):
                    p.tooltip.update(screen, events, keys, dt, dungeon)

            pygame.draw.rect(screen, (255, 0, 0), (p.x, p.y, p.w, p.h), 1)