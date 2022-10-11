import os
import time
import pygame

from player import player

class Projectile():
    def __init__(self, x, y, w, h, image_path, harms_player=True):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.harms_player = harms_player

        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "textures", "projectiles", image_path + ".png")), (w, h))

        self.rotation = 0
        self.last_rotation = self.rotation

        self.creation_time = time.time()

        self.mask = pygame.mask.from_surface(self.image)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.sprite.mask = self.mask

        self.psprite = pygame.sprite.Sprite()
        self.psprite.image = player.image
        self.psprite.mask = pygame.mask.from_surface(player.image)

        self.destroyed = False
        
        self.max_air_time = 10

        self.collisiondamage = 100

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        if self.rotation != self.last_rotation:
            self.rot_center(self.image, self.rotation)

        rect = self.image.get_rect(center=(self.x-cameraX, self.y-cameraY))
        self.sprite.rect = rect
        screen.blit(self.image, rect)

        if self.harms_player:
            prect = pygame.Rect(player.x, player.y, player.width, player.height)
            self.psprite.rect = prect

            collision = pygame.sprite.collide_mask(self.sprite, self.psprite)

            self.psprite.mask.outline()

            if collision is not None:
                self.oncollide(screen, events, keys, dt, dungeon, cameraX, cameraY)
                self.destroyed = True

        t = time.time()

        if t-self.creation_time >= self.max_air_time:
            self.destroyed = True

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def oncollide(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        player.recieve_damage(self.collisiondamage)