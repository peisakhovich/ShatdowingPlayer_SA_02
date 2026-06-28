# test_runner.py
#--------------
# Version: 0.2.0
#--------------

import pyodbc
import logging
import pygame

from audio import tts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=telegrambotsql.database.windows.net;"
    "DATABASE=telegrambotdb;"
    "UID=tb_admin;"
    "PWD=tb_39226417;"
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
# EVENT STATE
# ----------------------------
def create_event_state():
    return {
        "terminate": False
    }


def process_events(state):
    """
    Returns:
        bool -> continue running
    """
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            state["terminate"] = True
            return False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_END:
                state["terminate"] = True
                return False

    return True


# ----------------------------
# RUN SESSION
# ----------------------------
def run_session(plan: list[dict], set_id: int, state: dict):

    print("\n==============================")
    print(f"SA_02 TEST SESSION | SET ID: {set_id}")
    print("==============================\n")

    idx = 0

    while idx < len(plan):

        item = plan[idx]

        print(f"\n[{idx+1}] PHRASE:")
        print(f"TEXT   : {item['text']}")
        print(f"SPEED  : {item['speed']}")
        print(f"PAUSE  : {item['pause']} ms")
        print(f"REPEAT : {item['repeat']}")

        for r in range(item["repeat"]):

            print(f"   ▶ repeat {r+1}/{item['repeat']}")

            result = tts.speak(item, state)

            if state["terminate"]:
                return

            if result == "NEXT":
                idx += 1
                break

            elif result == "PREVIOUS":
                idx = max(0, idx - 1)
                break

            elif result == "RESTART":
                idx = 0
                break

            elif result == "TERMINATE":
                return

        else:
            idx += 1


# ----------------------------
# MAIN
# ----------------------------
def main():
    set_id = 2
    conn = None

    pygame.init()
    screen = pygame.display.set_mode((500, 120))
    pygame.display.set_caption("Shadowing App")

    state = create_event_state()

    try:
        conn = pyodbc.connect(CONNECTION_STRING)

        plan = load_training_plan(conn, set_id)

        if not plan:
            print("No data found for set:", set_id)
            return

        run_session(plan, set_id, state)

    except pyodbc.Error as e:
        logger.exception("Database error")
        print("DB error:", e)

    except Exception as e:
        logger.exception("Unexpected error")
        print("Unexpected error:", e)

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    print("RUNNING AS SCRIPT")
    main()