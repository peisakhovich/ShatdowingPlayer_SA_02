import pygame
import pygame_gui

pygame.init()

# Минимальное окно + UIManager
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SA_02 - pygame_gui button")

clock = pygame.time.Clock()

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

#Создаём кнопку

button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((200, 150), (200, 50)),
    text='Нажми меня',
    manager=manager
)

button2 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((200, 250), (200, 50)),
    text='Нажми меня тоже',
    manager=manager
)


#Главный цикл + обработка событий
running = True

while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

        # обработка кнопки
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button:
                print(f"Нажата кнопка: {event.ui_element.text}")

            elif event.ui_element == button2:
                print(f"Нажата кнопка: {event.ui_element.text}")
        


    manager.update(time_delta)

    screen.fill((30, 30, 30))
    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()