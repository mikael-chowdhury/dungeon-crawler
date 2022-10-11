from entities.monster.Monster import Monster
from util.ResourceLocation import ResourceLocation

from projectiles.Cannonball import Cannonball

from player import player

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

    def fire_cannonball(self):
        print("fired cannonball")
        self.fire_projectile(Cannonball(self.x, self.y, (player.rect.centerx-self.x+player.cameraX, player.rect.centery-self.y+player.cameraY)))

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        self.tick += 1

        if self.tick >= 250:
            self.tick = 0
            self.fire_cannonball()

        super().update(screen, events, keys, dt, dungeon, cameraX, cameraY)