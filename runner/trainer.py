import time
from core import config
from audio import tts

def train(phrases):
    for phrase in phrases:
        print(f"\nФраза: {phrase}")

        for i in range(config.REPEAT_COUNT):
            print(f"Повтор {i + 1}")

            tts.speak(phrase)

            if i < config.REPEAT_COUNT - 1:
                time.sleep(config.REPEAT_PAUSE)

        print("Пауза")
        time.sleep(config.USER_PAUSE)