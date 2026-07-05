import os

import pygame
import pygame_gui

from gui.controls import ControlPanel


class MainWindow:

    def __init__(self):

        pygame.init()

        self.size = (900, 600)

        self.screen = pygame.display.set_mode(self.size)

        pygame.display.set_caption("SA_02 Shadowing Player")

        self.manager = pygame_gui.UIManager(
            self.size,
            "gui/theme.json"
        )

        self.controls = ControlPanel(self.manager)
        FULL_NAME=os.path.abspath(__file__)
        print("FULL_NAME", FULL_NAME    )
        BASE_DIR = os.path.dirname(FULL_NAME)
        print("BASE_DIR:", BASE_DIR)
        print("IMG_DIR:",  os.path.join(BASE_DIR, "gui", "images"))


        self.clock = pygame.time.Clock()

        self.running = True

    def run(self):

        while self.running:

            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                self.manager.process_events(event)

                # делегируем обработку UI
                self.controls.handle_event(event)

            self.manager.update(time_delta)

            self.screen.fill((30, 30, 30))

            self.manager.draw_ui(self.screen)

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    MainWindow().run()