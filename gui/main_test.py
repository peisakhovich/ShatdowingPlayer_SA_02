import pygame
import pygame_gui
import os

from engine.image_button import ImageButton
from engine.image_loader import ImageLoader


# -------------------------
# INIT
# -------------------------
pygame.init()

WIDTH, HEIGHT =900, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SA_02 GUI v2")
#window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
window_surface = screen

background = pygame.Surface((WIDTH, HEIGHT))
background.fill(pygame.Color('#000000'))



clock = pygame.time.Clock()

loader = ImageLoader()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

theme_path = os.path.join(BASE_DIR, "theme.json")





font = pygame.font.Font(
    "gui/assets/fonts/inter/Inter_Regular.ttf",
    64
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

font_dir = os.path.join(
    BASE_DIR,
    "assets",
    "fonts",
    "inter"
)

#print("font_dir",font_dir)
#print(theme_path)
#print(os.path.exists(theme_path))

manager = pygame_gui.UIManager((WIDTH, HEIGHT),theme_path)

manager.add_font_paths(
    "inter_bold",
    os.path.join(font_dir, "Inter_Regular.ttf"),
    bold_path=os.path.join(font_dir, "Inter_Bold.ttf"),
    italic_path=os.path.join(font_dir, "Inter_Italic.ttf"),
    bold_italic_path=os.path.join(font_dir, "Inter_BoldItalic.ttf")
)
manager.get_theme().load_theme(theme_path)


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

# -------------------------
# LAYOUT CONFIG
# -------------------------

BTN_SIZE = (32, 32)
BTN_INTERVAL = 10
LEN_BUTTONS = (len(BUTTON_DEFS)+1)*((BTN_SIZE[0]+BTN_INTERVAL))+BTN_INTERVAL
BTN_START = (WIDTH/2-LEN_BUTTONS/2,HEIGHT-BTN_SIZE[1]-BTN_INTERVAL ) # (x, y) координаты верхнего левого угла кнопок
BTN_PARAM = ( BTN_START[0], BTN_START[1], BTN_SIZE[0],BTN_SIZE[1], BTN_INTERVAL)

buttons = [
    (name, CreateImageButton(index, BTN_PARAM, name))
    for name, index in BUTTON_DEFS
]

# -------------------------
# slider(под переменную скорости говорения )
# ------------------------- 

SpeedTune = 1.0   # стартовая скорость (например 1x)
LEN_SLIDER = (len(BUTTON_DEFS))*((BTN_SIZE[0]+BTN_INTERVAL))+BTN_INTERVAL
# --- slider ---
speed_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((BTN_PARAM[0]+BTN_SIZE[1], BTN_PARAM[1]-BTN_SIZE[1]-BTN_INTERVAL), (LEN_SLIDER, BTN_SIZE[1])),
    start_value=SpeedTune,
    value_range=(0.2, 2.0),   # диапазон скорости
    manager=manager
)

speed_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(280, 20, 70, 70),
    text=f"{SpeedTune:.2f}",
    manager=manager,
    object_id="#speed_label"
)

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

    # -------------------------
    # EVENTS
    # -------------------------

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():

        manager.process_events(event)

        if event.type == pygame.QUIT:
            running = False
            

        # 📌 ловим изменение slider
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == speed_slider:
                SpeedTune = event.value
                speed_label.set_text(f"{SpeedTune:.2f}")
                #print("SpeedTune =", SpeedTune)

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
    
    
    text = font.render("Проверка Inter", True, (255,255,255))
    screen.blit(text, (50,50))

    # UI: panels (пока пустые)
    phrase_panel.draw(screen)
    log_panel.draw(screen)

    # buttons
    for _, btn in buttons:
        btn.draw(screen)




    manager.update(dt)
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()