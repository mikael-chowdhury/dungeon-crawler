import os
import time
import xdrlib
import pygame
from animation.Animation import Animation

from player import player

class Projectile():
    def __init__(self, x, y, w, h, image_path, harms_player=True):
        self.animationlist = []
        self.collisionanimation = None
        self.playing_collision_animation = False

        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.harms_player = harms_player

        if image_path is not None:
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "textures", "projectiles", image_path + ".png")), (w, h))

        self.rotation = 0
        self.last_rotation = self.rotation

        self.creation_time = time.time()

        if "image" in self.__dict__.keys():
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
        
        if self.harms_player and not self.playing_collision_animation:
            prect = pygame.Rect(player.x, player.y, player.width, player.height)
            self.psprite.rect = prect

            collision = pygame.sprite.collide_mask(self.sprite, self.psprite)

            if collision is not None:
                self.oncollide(screen, events, keys, dt, dungeon, cameraX, cameraY)

                if self.collisionanimation is None:
                    self.destroyed = True
                else:
                    self.playing_collision_animation = True
                    self.collisionanimation.play_at(player.rect.centerx, player.rect.centery, self.collisionanimation.ms)

        t = time.time()

        if len(self.animationlist) > 0:
                Animation.update_animations(screen, self.animationlist)

        if t-self.creation_time >= self.max_air_time and not self.playing_collision_animation:
            self.destroyed = True

        if self.playing_collision_animation:
            Animation.update_animations(screen, [self.collisionanimation])

            if self.collisionanimation.current_frame == -1:
                self.collisionanimation = None
                self.playing_collision_animation = False

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def oncollide(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        player.recieve_damage(self.collisiondamage)