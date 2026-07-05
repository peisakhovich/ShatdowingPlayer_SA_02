import pygame
import os

pygame.init()

SIZE = (48, 48)

ICONS = {
    "play": "▶",
    "pause": "❚❚",
    "stop": "■",
    "next": "►►",
    "prev": "◄◄"
}

FONT = pygame.font.SysFont("arial", 28, bold=True)

OUT_DIR = "gui/images"

os.makedirs(OUT_DIR, exist_ok=True)

for name, symbol in ICONS.items():

    surface = pygame.Surface(SIZE, pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    text = FONT.render(symbol, True, (255, 255, 255))
    rect = text.get_rect(center=(24, 24))

    surface.blit(text, rect)

    pygame.image.save(surface, os.path.join(OUT_DIR, f"{name}.png"))

print("Icons generated!")