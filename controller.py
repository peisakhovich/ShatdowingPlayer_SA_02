# controller.py

import pygame


class Controller:

    NEXT = "next"
    PREVIOUS = "previous"
    REPEAT = "repeat"
    QUIT = "quit"
    NONE = "none"

    def get_command(self):

        for event in pygame.event.get():

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_n:
                return self.NEXT

            if event.key == pygame.K_b:
                return self.PREVIOUS

            if event.key == pygame.K_r:
                return self.REPEAT

            if event.key == pygame.K_q:
                return self.QUIT

        return self.NONE