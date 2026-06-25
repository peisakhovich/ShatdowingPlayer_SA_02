import edge_tts
import asyncio
import os
from playsound import playsound

VOICE = "pl-PL-MarekNeural"   # польский голос (можно поменять)


async def _speak_async(text: str):
    filename = "temp.mp3"

    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)

    playsound(filename)

    os.remove(filename)


def speak(text: str):
    asyncio.run(_speak_async(text))


def list_voices():
    print("Примеры голосов:")
    print("pl-PL-MarekNeural")
    print("pl-PL-ZofiaNeural")
    print("en-US-JennyNeural")
    print("en-US-GuyNeural")