from math import cos, degrees, sin, atan2, pi
import pygame
from entities.Entity import Entity
from font.FontManager import FontManager
from pathfinding.Pathfinder import Pathfinder

from player import player

class Monster(Entity):
    def __init__(self, name, x, y, image_path=None):
        super().__init__(x, y)

        self.image_path = image_path

        if image_path is not None:
            self.original_image = pygame.transform.smoothscale(pygame.image.load(image_path), (self.width, self.height)).convert_alpha()

        self.image = self.original_image
        
        self.name = name

        self.default_pathfinder = Pathfinder(self.x, self.y, player, self.speed)

        self.hp_font = FontManager.VT323_28
        
        self.rotation_padding = 0

    def update_image(self):
        if self.image is not None:
            self.image = pygame.transform.smoothscale(pygame.image.load(self.image_path), (self.width, self.height)).convert_alpha()

    def update_pathfinder(self):
        self.default_pathfinder = Pathfinder(self.x, self.y, player, self.speed)

    def draw_health_bar(self, screen, cameraX, cameraY):
        startx = self.x+self.width*0.1-cameraX
        starty = self.y+self.height*0.7-cameraY
        endy = self.y+self.height*0.7-cameraY

        health_percent = self.health / self.max_health

        pygame.draw.line(screen, (255, 0, 0), (startx, starty), (self.x+self.width*0.9*health_percent-cameraX, endy), 5)

    def get_angle(self, origin, destination):
        x_dist = destination[0] - origin[0]
        y_dist = destination[1] - origin[1]
        return atan2(-y_dist, x_dist) % (2 * pi)

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        angle = self.get_angle((self.rect.centerx-cameraX, self.rect.centery-cameraY), player.rect.center)
        self.image = self.rot_center(self.original_image, degrees(angle)+self.rotation_padding).convert_alpha()

        super().update(screen, events, keys, dt, dungeon, cameraX, cameraY)
        
        self.draw_health_bar(screen, cameraX, cameraY)