import tts
from runner.trainer import train

print("TTS FILE:", tts.__file__)
print("DIR:", dir(tts))

phrases = [
    "Dzien dobry",
    "Jak sie masz",
    "Mam na imie Andrzej",
    "Poprosze kawe"
]

tts.list_voices()

input("Нажмите Enter для начала тренировки...")

train(phrases)