# phrase_engine.py

import time
import pygame


class PhraseEngine:

    def __init__(
        self,
        player,
        controller
    ):
        self.player = player
        self.controller = controller

    def play_phrase(self, phrase):

        repeats = phrase.get("repeats", 1)
        pause_between = phrase.get(
            "pause_between",
            1.0
        )
        pause_after = phrase.get(
            "pause_after",
            2.0
        )

        audio = phrase["audio"]

        for i in range(repeats):

            print(
                f"   ▶ repeat {i+1}/{repeats}"
                f" -> {phrase['text']}"
            )

            self.player.play(audio)

            while self.player.is_busy():
                pygame.time.wait(100)

            if i < repeats - 1:
                time.sleep(
                    pause_between
                )

        time.sleep(pause_after)

        return self.controller.get_command()