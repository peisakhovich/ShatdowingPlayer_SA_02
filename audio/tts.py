import asyncio
import os
import tempfile
import time

import edge_tts
import pygame


VOICE = "pl-PL-MarekNeural"


# ----------------------------
# INIT MIXER
# ----------------------------
if not pygame.mixer.get_init():
    pygame.mixer.init()


# ----------------------------
# ASYNC SPEECH GENERATION
# ----------------------------
async def _speak_async(item: dict, SpeedTune: float):
    fd, filename = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)

    try:
        rate_value = (item["speed"]*SpeedTune-1) * 100
        rate_str = f"{rate_value:+.0f}%"

        communicate = edge_tts.Communicate(
            text=item["text"],
            voice=VOICE,
            rate=rate_str
        )

        await communicate.save(filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        return filename

    except Exception:
        if os.path.exists(filename):
            os.remove(filename)
        raise


# ----------------------------
# MAIN SPEAK FUNCTION
# ----------------------------
def speak(item: dict,TimeEndPause: float,SpeedTune: float):
    filename = asyncio.run(_speak_async(item,SpeedTune))

    paused = False
    last_space = 0  # ✅ FIX: debounce initialization
    paused_manual = False
    
    try:
        while True:

            # ----------------------------
            # 1. EVENT HANDLING
            # ----------------------------
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    return "TERMINATE"

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_KP_PLUS: 
                        pygame.mixer.music.stop()
                        return "SPEED_INC"

                    if event.key == pygame.K_KP_MINUS:
                        pygame.mixer.music.stop()
                        return "SPEED_DEC"

                    # ESC = skip pause after previosly item
                    if event.key == pygame.K_ESCAPE:
                        TimeEndPause = time.time()      

                    # END
                    if event.key == pygame.K_END:
                        pygame.mixer.music.stop()
                        return "TERMINATE"

                    # HOME = restart
                    if event.key == pygame.K_HOME:
                        pygame.mixer.music.stop()
                        return "RESTART"

                    # PAGE DOWN = next
                    if event.key == pygame.K_PAGEDOWN:
                        pygame.mixer.music.stop()
                        return "NEXT"

                    # PAGE UP = previous
                    if event.key == pygame.K_PAGEUP:
                        pygame.mixer.music.stop()
                        return "PREVIOUS"

                    # SPACE = manual pause / resume
                    if event.key == pygame.K_SPACE:

                        now = pygame.time.get_ticks()

                        # debounce
                        if now - last_space < 200:
                            continue

                        last_space = now

                        paused_manual = not paused_manual


            # ----------------------------
            # 2. AUTO PAUSE LOGIC (TIME BASED)
            # ----------------------------
            paused_auto = time.time() < TimeEndPause

            # итоговое состояние паузы
            paused = paused_manual or paused_auto


            # ----------------------------
            # 3. APPLY STATE (без дерганья)
            # ----------------------------
            if paused:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()


            # ----------------------------
            # 4. TRACK END CHECK
            # ----------------------------
            if not pygame.mixer.music.get_busy() and not paused:
                return "DONE"


            # ----------------------------
            # 5. CPU LIMIT
            # ----------------------------
            pygame.time.wait(20)
        # while end
            
    finally:
        try:
            pygame.mixer.music.unload()
        except Exception:
            pass

        if os.path.exists(filename):
            try:
                os.remove(filename)
            except PermissionError:
                pygame.time.wait(100)
                if os.path.exists(filename):
                    os.remove(filename)


# ----------------------------
# VOICES
# ----------------------------
def list_voices():
    print("pl-PL-MarekNeural")
    print("pl-PL-ZofiaNeural")
    print("en-US-GuyNeural")
    print("en-US-JennyNeural")