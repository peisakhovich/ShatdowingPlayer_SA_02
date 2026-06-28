import asyncio
import os
import tempfile

import edge_tts
import pygame


VOICE = "pl-PL-MarekNeural"

# Инициализируем mixer один раз при импорте модуля
if not pygame.mixer.get_init():
    pygame.mixer.init()


async def _speak_async(Item: dict):
    # Создаём временный mp3-файл
    fd, filename = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)

    try:
        
        rate_value = (Item["speed"] - 1) * 100
        rate_str = f"{rate_value:+.0f}%"
        communicate = edge_tts.Communicate(Item["text"], VOICE,  rate=rate_str)
        await communicate.save(filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        # Ждём окончания воспроизведения
        while pygame.mixer.music.get_busy():
            pygame.time.wait(Item["pause"])

    finally:
        # На всякий случай освобождаем файл
        pygame.mixer.music.unload()

        if os.path.exists(filename):
            try:
                os.remove(filename)
            except PermissionError:
                # Иногда Windows ещё держит файл долю секунды
                pygame.time.wait(100)
                if os.path.exists(filename):
                    os.remove(filename)


def speak(Item: dict):
    asyncio.run(_speak_async(Item))

def list_voices():
    print("Доступные голоса (примеры):")
    print("pl-PL-MarekNeural")
    print("pl-PL-ZofiaNeural")
    print("en-US-GuyNeural")
    print("en-US-JennyNeural")