from entities.monster.Monster import Monster
from util.ResourceLocation import ResourceLocation

class Wizard(Monster):
    def __init__(self, x, y):
        super().__init__("Wizard", x, y, image_path=ResourceLocation("assets/models/Wizard.png"))

        self.speed = 0.01

        self.width = 50
        self.height = 50

        self.health = 50
        self.max_health = 50

        self.rotation_padding = 90

        self.update_image()
        self.update_rect()
        self.update_pathfinder()