import os
import pygame

from util.ResourceLocation import ResourceLocation

class Animation():
    def __init__(self, foldername, framewidth=32, frameheight=32) -> None:
        self.loadedframes = []

        self.framewidth = framewidth
        self.frameheight = frameheight

        self.animationdir = os.path.join(ResourceLocation("assets/textures/animations").__str__(), foldername)

        self.unloadedframes = [x.replace(".png", "") for x in os.listdir(self.animationdir)]
        
        self.current_frame = -1

        self.fps = 1
        self.ms = 1000/self.fps

        self.elapsed = pygame.time.get_ticks()

        for frame in os.listdir(self.animationdir):
            self.loadedframes.append(pygame.transform.scale(pygame.image.load(os.path.join(self.animationdir, frame)), (self.framewidth, self.frameheight)).convert_alpha())

    def inc(self):
        if self.current_frame > -1:
            self.current_frame += 1
            if self.current_frame >= len(self.loadedframes):
                self.current_frame = -1

    def get_frame(self):
        self.inc()
        return self.loadedframes[self.current_frame - 1]

    def play_at(self, x, y, ms):
        self.x = x
        self.y = y
        self.ms = ms
        return self
        
    @staticmethod
    def update_animations(screen, list):
        for animation in list:
            # print(animation)
            if animation.current_frame == -1:
                animation.current_frame = 0

            if pygame.time.get_ticks() - animation.elapsed > 1000/animation.fps:
                animation.elapsed = pygame.time.get_ticks()
                animation.inc()

            if animation.current_frame > -1:
                frame = animation.loadedframes[animation.current_frame]
                if frame is not None:
                    rect = frame.get_rect(center=(animation.x, animation.y))
                    screen.blit(frame, rect)