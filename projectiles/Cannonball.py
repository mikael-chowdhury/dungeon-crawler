import math
from animation.Animation import Animation
from projectiles.Projectile import Projectile

class Cannonball(Projectile):
    def __init__(self, x, y, direction, size=100):
        super().__init__(x, y, size, size, "cannon-ball")

        self.direction = direction
        
        self.speed = 0.25

        length = math.hypot(*self.direction)
        if length == 0.0:
            self.direction = (0, -1)
        else:
            self.direction = (self.direction[0]/length, self.direction[1]/length)

        angle = math.degrees(math.atan2(-self.direction[1], self.direction[0]))

        self.collisionanimation = Animation("CannonballExplosion", 300, 300)
        self.collisionanimation.fps = 10

        self.rotation = angle

    def oncollide(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        super().oncollide(screen, events, keys, dt, dungeon, cameraX, cameraY)

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        self.x += self.direction[0]*self.speed*dt
        self.y += self.direction[1]*self.speed*dt

        super().update(screen, events, keys, dt, dungeon, cameraX, cameraY)