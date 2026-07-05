# test_runner.py
#--------------
# Version: 0.2.0
#--------------

import pyodbc
import logging
import pygame
import time
import os

from audio import tts
from dotenv import load_dotenv

load_dotenv("config.env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PASS=os.getenv("DB_PASS")

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=telegrambotsql.database.windows.net;"
    "DATABASE=telegrambotdb;"
    "UID=tb_admin;"
    "PWD=" + DB_PASS + ";"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
    "Connection Timeout=30;"
)


# ----------------------------
# LOAD TRAINING SET
# ----------------------------
def load_training_plan(conn, set_id: int):
    cursor = conn.cursor()

    query = """
    SELECT 
        p.text,
        ISNULL(si.repeat_override, p.default_repeat) AS repeat_count,
        ISNULL(si.speed_override, p.default_speed) AS speed,
        ISNULL(si.pause_override, p.default_pause_ms) AS pause,
        si.order_index
    FROM set_items si
    JOIN phrases p ON p.id = si.phrase_id
    WHERE si.set_id = ?
    ORDER BY si.order_index
    """

    cursor.execute(query, set_id)
    rows = cursor.fetchall()

    plan = []
    for r in rows:
        plan.append({
            "text": r.text,
            "repeat": int(r.repeat_count),
            "speed": float(r.speed),
            "pause": int(r.pause),
            "order": r.order_index
        })

    return plan




# ----------------------------
# RUN SESSION
# ----------------------------
def run_session(plan: list[dict], set_id: int):

    print("\n==============================")
    print(f"SA_02 TEST SESSION | SET ID: {set_id}")
    print("==============================\n")

    TimeEndPause = time.time()  # Initialize TimeEndPause to current time
    SpeedTune = 1.0  # Initialize SpeedTune to default value

    idx = 0

    while idx < len(plan):

        item = plan[idx]

        print(f"\n[{idx+1}] PHRASE:")
        print(f"TEXT   : {item['text']}")
        print(f"SPEED  : {item['speed']*SpeedTune}")
        print(f"PAUSE  : {item['pause']} ms")
        #print(f"TIME_PAUSE:{TimeEndPause} ")
        print(f"REPEAT : {item['repeat']}")

        for r in range(item["repeat"]):

            print(f"   ▶ repeat {r+1}/{item['repeat']}")

            result = tts.speak(item,TimeEndPause,SpeedTune)

            if result == "SPEED_INC":
                SpeedTune += 0.1
                break
            if result == "SPEED_DEC":
                SpeedTune -= 0.1
                break    

            if result == "NEXT":
                idx += 1
                break

            elif result == "PREVIOUS":
                idx = max(0, idx - 1)
                break

            elif result == "RESTART":
                idx = 0
                break
            # Set time for PAUSE after done item
            elif result == "DONE":

                TimeEndPause = time.time() + (item["pause"] / 1000)  # Set the end time for the pause   
                
                if r == (item["repeat"]-1 ):
                    idx += 1
                    break
            

            elif result == "TERMINATE":
                return

            else:
                idx += 1




# ----------------------------
# MAIN
# ----------------------------
def main():
    set_id = 1
    conn = None

    pygame.init()
    screen = pygame.display.set_mode((500, 120))
    pygame.display.set_caption("Shadowing App")

    while True:
        try:
            print("Подключаемся к БД AZURE.")
            conn = pyodbc.connect(CONNECTION_STRING)
            print("Соединение установлено.")
        
            plan = load_training_plan(conn, set_id)

            if not plan:
                print("No data found for set:", set_id)
                return

            run_session(plan, set_id)
        
            break

        except pyodbc.Error as e:
            print(f"Ошибка подключения: {e}")
            print(f"Ошибка подключения:")
            print("Повтор через 5 секунд...")
            time.sleep(5)

        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    print("RUNNING AS SCRIPT")
    main()