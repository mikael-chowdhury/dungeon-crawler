import time
import pygame
from inventory.EntityInventory import EntityInventory

class Entity():
    def __init__(self, x, y):
        self.health = 100
        self.max_health = 100
        
        self.physical_damage = 15
        self.magical_damage = 20

        self.mana = 100
        self.max_mana = 100
        self.mana_gain_speed = 2

        self.critical_chance = 15
        self.critical_multiplier = 2

        self.attackspeedmultiplier = 1

        self.width = 100
        self.height = 100

        self.inventory = EntityInventory()

        self.speed = 0.5

        self.x = x
        self.y = y

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.default_pathfinder = None

        self.image = None

        self.position_facing = (0, 0)

        self.follow_camera = False

        self.projectiles:list = []

    # def get_stat(self, stat):
    #     return getattr(self, stat)

    def fire_projectile(self, projectile):
        self.projectiles.append(projectile)

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def set_rect(self, rect):
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self.width = rect.width
        self.height = rect.height

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        self.inventory.update_inventory(screen, events, keys, dt, dungeon, cameraX, cameraY)

        for projectile in self.projectiles:
            projectile.update(screen, events, keys, dt, dungeon, cameraX, cameraY)

        self.projectiles = [x for x in self.projectiles if not x.destroyed]

        if self.default_pathfinder is not None:
            x, y = self.default_pathfinder.get_new_position(self.x, self.y, dt)
            self.x = x
            self.y = y
            self.update_rect()
        
        if self.image is None:
            if self.follow_camera:
                pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, self.width, self.height))
                pygame.draw.rect(screen, (0,0,0), (self.x, self.y, self.width, self.height), 1)
            else:
                pygame.draw.rect(screen, (255, 255, 0), (self.x-cameraX, self.y-cameraY, self.width, self.height))
                pygame.draw.rect(screen, (0,0,0), (self.x-cameraX, self.y-cameraY, self.width, self.height), 1)

        else:
            if self.follow_camera:
                screen.blit(self.image, (self.x, self.y))
            else:
                screen.blit(self.image, (self.x-cameraX, self.y-cameraY))