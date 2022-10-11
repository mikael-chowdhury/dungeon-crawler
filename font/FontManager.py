import os
import pygame

from util.ResourceLocation import ResourceLocation

from Manager import Manager

class Font(pygame.font.Font):
    def __init__(self, name, size):
        super().__init__(ResourceLocation(f"assets/fonts/{name}").__str__(), size)

class FontManager(Manager):
    def __init__(self) -> None:
        super().__init__()

        self.applyfonts(
        ("VT323_250", Font("VT323.ttf", 250)),
        ("VT323_64", Font("VT323.ttf", 64)),
        ("VT323_48", Font("VT323.ttf", 48)),
        ("VT323_42", Font("VT323.ttf", 42)),
        ("VT323_36", Font("VT323.ttf", 36)),
        ("VT323_32", Font("VT323.ttf", 32)),
        ("VT323_28", Font("VT323.ttf", 28)),
        ("VT323_24", Font("VT323.ttf", 24)),
        ("VT323_16", Font("VT323.ttf", 16)),
        )

    def applyfonts(self, *fonts):
        print(fonts)
        for f in fonts:
            print(f)
            setattr(FontManager, f[0], f[1])