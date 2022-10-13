import pygame

from player import player

class AreaOfEffect:
    def __init__(self, x, y, size) -> None:
        self.x = x
        self.y = y

        self.cameraX = player.cameraX
        self.cameraY = player.cameraY

        self.size = size

        self.surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (255, 0, 0, 50), (self.size, self.size), self.size)

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        screen.blit(self.surf, (self.x+self.cameraX-player.cameraX-self.size, self.y+self.cameraY-player.cameraY-self.size))