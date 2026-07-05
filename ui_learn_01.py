import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("SA_02")

running = True
clock = pygame.time.Clock()

while running:

    dt = clock.tick(60) / 1000

    for event in pygame.event.get():

        print(event)
        print(dt)
        if event.type == pygame.QUIT:
            running = False

pygame.quit()