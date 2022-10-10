from entities.monster.Monster import Monster
from util.ResourceLocation import ResourceLocation

class Wizard(Monster):
    def __init__(self, x, y):
        super().__init__("Wizard", x, y, image_path=ResourceLocation("assets/textures/entities/Wizard.png"))

        self.speed = 0.01

        self.width = 50
        self.height = 50

        self.health = 50
        self.max_health = 50

        self.rotation_padding = 90

        self.tick = 0

        self.update_image()
        self.update_rect()
        self.update_pathfinder()

    def fire_fireball(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        self.tick += 1

        if self.tick >= 5000:
            self.tick = 0


        super().update(screen, events, keys, dt, dungeon, cameraX, cameraY)