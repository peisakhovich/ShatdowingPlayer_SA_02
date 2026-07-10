import pygame
import pygame_gui
import os

from engine.image_button import ImageButton
from engine.image_loader import ImageLoader
from pygame_gui.elements import UIHorizontalSlider,UILabel,UIPanel
from pygame_gui.elements import UITextBox

# -------------------------
# INIT
# -------------------------
pygame.init()

WIDTH, HEIGHT =850, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SA_02 GUI v2")
#window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
window_surface = screen

background = pygame.Surface((WIDTH, HEIGHT))
background.fill(pygame.Color('#000000'))

InfoData = {"voice_short_name": "pl-PL-MarekNeural",
            "language_code": "pl",
            "phrase_level": "B2",    
            "set_id": 1}

TextItem="Wydaje mi sie, ze problem jest bardziej zlozony."
TextItemTranslate="Мне кажется, проблема гораздо сложнее."


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

BTN_SIZE = (32, 32) # width, height of buttons
BTN_INTERVAL = 10 # Interval between buttons

LEN_BUTTONS = (len(BUTTON_DEFS)+1)*((BTN_SIZE[1]+BTN_INTERVAL))+BTN_INTERVAL
BTN_START = (WIDTH-LEN_BUTTONS,HEIGHT-(BTN_SIZE[1]+BTN_INTERVAL)*4 ) # (x, y) координаты верхнего левого угла начала кнопок
BTN_PARAM = ( BTN_START[0], BTN_START[1], BTN_SIZE[0],BTN_SIZE[1], BTN_INTERVAL)


# -----------
# Панели 
# -----------

# 
TextPanel = UIPanel(
     relative_rect=pygame.Rect(  BTN_SIZE[0]/4
                               , BTN_SIZE[1]/4
                               , WIDTH- BTN_SIZE[0]/2
                               , HEIGHT-BTN_SIZE[0]*6),
     manager=manager
 )


# тонких настроек
TunelPanel = UIPanel(
     relative_rect=pygame.Rect(  BTN_SIZE[0]/4
                               , HEIGHT-BTN_SIZE[0]*6
                               , LEN_BUTTONS-BTN_SIZE[0]
                               , BTN_SIZE[0]*6),
     manager=manager
 )

# Информационная панель (для отображения текущего состояния)  
InfoPanel = UIPanel(
     relative_rect=pygame.Rect(  LEN_BUTTONS-BTN_SIZE[0]
                               , BTN_START[1]+BTN_SIZE[0]*1
                               , WIDTH-LEN_BUTTONS+BTN_SIZE[0]*0.75
                               , BTN_SIZE[1]*4.25),
     manager=manager
 )


# ------------------------- 
# slider(под переменную скорости говорения )
# ------------------------- 

SpeedTune = 1.0   # стартовая скорость (например 1x)
LEN_SLIDER = (len(BUTTON_DEFS)-2)*((BTN_SIZE[0]+BTN_INTERVAL))+BTN_INTERVAL

speed_slider = UIHorizontalSlider(
    relative_rect=pygame.Rect(15+BTN_SIZE[0]*2, 10, LEN_SLIDER-BTN_SIZE[1], BTN_SIZE[0]),
    start_value=SpeedTune,
    value_range=(0.2, 2.0),   # диапазон скорости
    manager=manager,
    container=TunelPanel
)

speed_label = UILabel(
    relative_rect=pygame.Rect(10,12,BTN_SIZE[0]*2,BTN_SIZE[1]-3),
    text=f"{SpeedTune:.2f}",
    manager=manager,
    container=TunelPanel,
    object_id="#speed_label"
)

speed_label_hint = UILabel(
    relative_rect=pygame.Rect(BTN_SIZE[0],BTN_SIZE[1]+10,LEN_SLIDER,BTN_SIZE[1]/2),
    text=f"Tune Speed of Voice:",
    manager=manager,
    container=TunelPanel
)

# ------------------------- 
# slider(под переменную длинны пауз между фразами )
# ------------------------- 

PauseLengthTune = 1.0   # стартовая длина паузы (например 1x)

LEN_SLIDER = (len(BUTTON_DEFS)-2)*((BTN_SIZE[0]+BTN_INTERVAL))+BTN_INTERVAL

pause_slider = UIHorizontalSlider(
    relative_rect=pygame.Rect(15+BTN_SIZE[0]*2, BTN_SIZE[1]*3, LEN_SLIDER-BTN_SIZE[1], BTN_SIZE[0]),
    start_value=PauseLengthTune,
    value_range=(0.2, 2.0),   # диапазон скорости
    manager=manager,
    container=TunelPanel
)

pause_label = UILabel(
    relative_rect=pygame.Rect(10,BTN_SIZE[1]*3,BTN_SIZE[0]*2,BTN_SIZE[1]-3),
    text=f"{PauseLengthTune:.2f}",
    manager=manager,
    container=TunelPanel,
    object_id="#speed_label"
)

pause_label_hint = UILabel(
    relative_rect=pygame.Rect(BTN_SIZE[0],BTN_SIZE[1]*4+5,LEN_SLIDER,BTN_SIZE[1]/2),
    text=f"Tune Length of Pause between phrases:",
    manager=manager,
    container=TunelPanel
)

# -------------------------
# Заполняем Информационную панель
# -------------------------
Infotext = (
    f"Voice: {InfoData['voice_short_name']}"
    f"     Language: {InfoData['language_code']}"
    )
Infotext1 = (    
    f"Phrase Level: {InfoData['phrase_level']}"
    f"     Set ID: {InfoData['set_id']}"
)


info_label = UILabel(
    relative_rect=pygame.Rect(10,10, WIDTH-LEN_BUTTONS,20), 
    text=Infotext,
    manager=manager,
    object_id="#info_label",
    container=InfoPanel 
)
info_label1 = UILabel(
    relative_rect=pygame.Rect(10,30, WIDTH-LEN_BUTTONS,20), 
    text=Infotext1,
    manager=manager,
    object_id="#info_label",
    container=InfoPanel 
)

text_box = UITextBox(
    html_text=TextItem,
    relative_rect=pygame.Rect(10,10,WIDTH-BTN_SIZE[0]*2,150),
    manager=manager,
    object_id="#text_box",
    container=TextPanel 
)
text_box_translate = UITextBox(
    html_text=TextItemTranslate,
    relative_rect=pygame.Rect(10,160,WIDTH-BTN_SIZE[0]*2,100),
    manager=manager,
    object_id="#box_translate",
    container=TextPanel 
)



# -------------------------
# Создание кнопок 
# -------------------------
buttons = [
    (name, CreateImageButton(index, BTN_PARAM, name))
    for name, index in BUTTON_DEFS
]



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
                
            if event.ui_element == pause_slider:
                PauseLengthTune = event.value
                pause_label.set_text(f"{PauseLengthTune:.2f}")
                

        # 📌 Ловим клики по кнопкам
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
    #background.fill(pygame.Color('#000000'))
    #screen.blit(background, (0,0))
    
 

    # buttons
    for _, btn in buttons:
        btn.draw(screen)


    manager.update(dt)
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()