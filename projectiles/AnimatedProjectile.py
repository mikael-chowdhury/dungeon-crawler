import pygame
from animation.Animation import Animation
from projectiles.Projectile import Projectile

class AnimatedProjectile(Projectile):
    def __init__(self, x, y, w, h, animation:Animation, harms_player=True):
        super().__init__(x, y, w, h, None, harms_player)

        self.animation = animation

        self.image = self.animation.loadedframes[0]

        self.mask = pygame.mask.from_surface(self.image)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.sprite.mask = self.mask

        self.frames = self.animation.loadedframes

    def oncollide(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        super().oncollide(screen, events, keys, dt, dungeon, cameraX, cameraY)

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        if self.rotation != self.last_rotation:
            self.frames = [pygame.transform.rotate(x, self.rotation) for x in self.animation.loadedframes]

        if not self.playing_collision_animation:
            if pygame.time.get_ticks() - self.animation.elapsed > self.animation.ms:
                self.animation.elapsed = pygame.time.get_ticks()
                self.animation.inc()
            
            if self.animation.current_frame > -1:
                self.image = self.frames[self.animation.current_frame]
            else:
                self.animation.current_frame += 1

        super().update(screen, events, keys, dt, dungeon, cameraX, cameraY)