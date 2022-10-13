import pygame

pygame.init()

screen = pygame.display.set_mode((800, 800))

image = pygame.image.load("./assets/textures/animations/ElectricBeam/skeleton-animation_0.png")

rotated = pygame.transform.rotate(image, 90)

isRunning = True

while isRunning:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            isRunning = False
    
    screen.fill((0, 0, 0))

    screen.blit(rotated)