import math
import time

import pygame

from player import player


class Pathfinder:
    def __init__(self, x, y, target, speed):
        self.x = x
        self.y = y

        self.target = target

        self.speed = speed

        self.delay_ms = 100

        self.was_still = False
        self.still_since = 0

    def get_new_position(self, x, y, dt):
        self.x = x
        self.y = y

        distanceX = self.target.x + player.cameraX - self.x
        distanceY = self.target.y + player.cameraY - self.y

        vec = pygame.math.Vector2(distanceX, distanceY)
        if vec.length_squared() > 0 and dt > 0:
            vec.scale_to_length(self.speed*dt)

        return x+vec[0], y+vec[1]