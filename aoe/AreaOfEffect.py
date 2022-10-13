import random
import pygame

from player import player
from util.ResourceLocation import ResourceLocation

class AreaOfEffect:
    def __init__(self, x, y, size, imagename) -> None:
        self.x = x
        self.y = y

        self.cameraX = player.cameraX
        self.cameraY = player.cameraY

        self.image = pygame.transform.scale(pygame.image.load(ResourceLocation(f"assets/textures/abilities/items/{imagename}.png")), (size*2, size*2)).convert_alpha()
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.sprite.rect = pygame.Rect(self.x+self.cameraX-player.cameraX-size, self.y+self.cameraY-player.cameraY-size, size*2, size*2)
        self.sprite.mask = pygame.mask.from_surface(self.image)

        self.size = size

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        screen.blit(self.image, (self.x+self.cameraX-player.cameraX-self.size, self.y+self.cameraY-player.cameraY-self.size))

        for monster in dungeon.monsters:
            mask = pygame.mask.from_surface(monster.image)
            sprite = pygame.sprite.Sprite()
            sprite.rect = pygame.Rect(0, 0, monster.rect.width, monster.rect.height)
            sprite.rect.x = monster.rect.x - player.cameraX
            sprite.rect.y = monster.rect.y - player.cameraY
            sprite.mask = mask

            pygame.draw.rect(screen, (255, 0, 0), sprite.rect)

            collision = pygame.sprite.collide_mask(self.sprite, sprite)
            if collision is not None:
                print(f"collision {random.randrange(0, 10000)}")