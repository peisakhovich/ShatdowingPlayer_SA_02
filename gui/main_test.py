import pygame
import os

from engine.image_button import ImageButton
from engine.image_loader import ImageLoader

# -------------------------
# INIT
# -------------------------
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SA_02 GUI v2")

clock = pygame.time.Clock()

loader = ImageLoader()

# -------------------------
# LAYOUT CONFIG
# -------------------------
BTN_START = (300, 450)
BTN_SIZE = (32, 32)
BTN_INTERVAL = 10

BTN_PARAM = (
    BTN_START[0],
    BTN_START[1],
    BTN_SIZE[0],
    BTN_SIZE[1],
    BTN_INTERVAL
)

# -------------------------
# BUTTON FACTORY
# -------------------------
def CreateImageButton(index, btn_param, image_name):
    return ImageButton(
        rect=(
            btn_param[0] + (btn_param[2] + btn_param[4]) * index,
            btn_param[1],
            btn_param[2],
            btn_param[3]
        ),
        image_normal=loader.load(f"gui/assets/{image_name}.png"),
        image_hover=loader.load(f"gui/assets/{image_name}_hover.png"),
        image_pressed=loader.load(f"gui/assets/{image_name}_pressed.png")
    )

# -------------------------
# UI LAYER: BUTTON BAR
# -------------------------
BUTTON_DEFS = [
    ("start", 1),
    ("prev", 2),
    ("play", 3),
    ("pause", 4),
    ("next", 5),
    ("end", 6),
    ("stop", 7),
]

buttons = [
    (name, CreateImageButton(index, BTN_PARAM, name))
    for name, index in BUTTON_DEFS
]

# -------------------------
# PLACEHOLDER PANELS (под будущую архитектуру)
# -------------------------
class PhrasePanel:
    def draw(self, screen):
        # потом сюда большой текст
        pass

class LogPanel:
    def draw(self, screen):
        # потом сюда лог событий
        pass

phrase_panel = PhrasePanel()
log_panel = LogPanel()

# -------------------------
# MAIN LOOP
# -------------------------
running = True

while running:
    dt = clock.tick(60)

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    # -------------------------
    # EVENTS
    # -------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for _, btn in buttons:
            btn.handle_event(event)

    # -------------------------
    # UPDATE
    # -------------------------
    for _, btn in buttons:
        btn.update(mouse_pos, mouse_pressed)

    # -------------------------
    # CLICK LOGIC
    # -------------------------
    for name, btn in buttons:
        if btn.was_clicked():
            print(name.upper())

    # -------------------------
    # DRAW
    # -------------------------
    screen.fill((30, 30, 30))

    # UI: panels (пока пустые)
    phrase_panel.draw(screen)
    log_panel.draw(screen)

    # buttons
    for _, btn in buttons:
        btn.draw(screen)

    pygame.display.flip()

pygame.quit()