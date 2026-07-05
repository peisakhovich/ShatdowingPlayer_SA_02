import pygame
import os

from engine.image_button import ImageButton
from engine.image_loader import ImageLoader

#print(os.path.abspath("gui/assets/play.png"))
# -------------------------
# INIT
# -------------------------
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ImageButton Engine Test")

clock = pygame.time.Clock()

def CreateImageButton(Index,BTN_PARAM, image_name):
    return ImageButton(
        rect=(BTN_PARAM[0]+(BTN_PARAM[2]+BTN_PARAM[4])*Index, BTN_PARAM[1], BTN_PARAM[2], BTN_PARAM[3]),
        image_normal=loader.load(f"gui/assets/{image_name}.png"),
        image_hover=loader.load(f"gui/assets/{image_name}_hover.png"),
        image_pressed=loader.load(f"gui/assets/{image_name}_pressed.png")
    )


# -------------------------
# ENGINE
# -------------------------
loader = ImageLoader()

BTN_START = (300, 450)
BTN_SIZE = (32, 32)
BTN_INTERVAL = 10

BTN_PARAM=( BTN_START[0], BTN_START[1], BTN_SIZE[0], BTN_SIZE[1],BTN_INTERVAL) 

# -------------------------
# BUTTONS
# -------------------------

button_start = CreateImageButton(  1, BTN_PARAM,    image_name="start" )
button_prev = CreateImageButton(  2, BTN_PARAM,    image_name="prev" )
button_play = CreateImageButton(  3, BTN_PARAM,    image_name="play" )
button_pause= CreateImageButton(  4, BTN_PARAM,    image_name="pause" )     
button_next = CreateImageButton(  5, BTN_PARAM,    image_name="next" )
button_end = CreateImageButton(  6, BTN_PARAM,    image_name="end" )
button_stop = CreateImageButton(  7, BTN_PARAM,    image_name="stop" )



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

        button_start.handle_event(event)
        button_play.handle_event(event)
        button_stop.handle_event(event)
        button_pause.handle_event(event)
        button_prev.handle_event(event)
        button_next.handle_event(event)
        button_end.handle_event(event)



    # -------------------------
    # UPDATE
    # -------------------------
    button_start.update(mouse_pos, mouse_pressed)
    button_play.update(mouse_pos, mouse_pressed)
    button_stop.update(mouse_pos, mouse_pressed)
    button_pause.update(mouse_pos, mouse_pressed)
    button_prev.update(mouse_pos, mouse_pressed)
    button_next.update(mouse_pos, mouse_pressed)
    button_end.update(mouse_pos, mouse_pressed)



    if button_play.was_clicked():
        print("PLAY!")
        
    if button_stop.was_clicked():
        print("STOP!")

    if button_pause.was_clicked():
        print("PAUSE!")

    if button_prev.was_clicked():
        print("PREV!")

    if button_next.was_clicked():
        print("NEXT!")

    if button_end.was_clicked():
        print("END!")

    if button_start.was_clicked():
        print("START!")    



    # -------------------------
    # DRAW
    # -------------------------
    screen.fill((30, 30, 30))

    button_play.draw(screen)
    button_stop.draw(screen)
    button_pause.draw(screen)
    button_prev.draw(screen)
    button_next.draw(screen)
    button_start.draw(screen)
    button_end.draw(screen)

    
    pygame.display.flip()


pygame.quit()