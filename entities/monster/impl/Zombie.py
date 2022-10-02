from entities.monster.Monster import Monster

from util.ResourceLocation import ResourceLocation


class Zombie(Monster):
    def __init__(self, x, y):
        super().__init__("Zombie", x, y, ResourceLocation("assets/models/Zombie.png"))

        self.speed = 0.05

        self.width = 125
        self.height = 125

        self.health = 150
        self.max_health = 150

        self.rotation_padding = 270

        self.update_image()
        self.update_rect()
        self.update_pathfinder()

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        super().update(screen, events, keys, dt, dungeon, cameraX, cameraY)