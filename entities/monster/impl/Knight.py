from entities.monster.Monster import Monster

from util.ResourceLocation import ResourceLocation

class Knight(Monster):
    def __init__(self, x, y):
        super().__init__("Knight", x, y, ResourceLocation("assets/textures/entities/knight.png"))

        self.speed = 0.1

        self.width = 150
        self.height = 150

        self.health = 300
        self.max_health = 300

        self.update_image()
        self.update_rect()
        self.update_pathfinder()