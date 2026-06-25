import pyodbc
from audio import tts

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
# RUN SESSION (TEST MODE)
# ----------------------------
def run_session(plan, set_id: int):
    print("\n==============================")
    print(f"SA_02 TEST SESSION | SET ID: {set_id}")
    print("==============================\n")

    for idx, item in enumerate(plan, start=1):

        print(f"\n[{idx}] PHRASE:")
        print(f"TEXT   : {item['text']}")
        print(f"SPEED  : {item['speed']}")
        print(f"PAUSE  : {item['pause']} ms")
        print(f"REPEAT : {item['repeat']}")

        print("→ EXECUTION LOOP:")

        for r in range(item["repeat"]):
            print(f"   ▶ repeat {r+1}/{item['repeat']} -> {item['text']}")

            tts.speak(item["text"])

        print("✓ done\n")


# ----------------------------
# MAIN
# ----------------------------
def main():
    set_id = 1  # твой тестовый set

    conn = pyodbc.connect(CONNECTION_STRING)

    try:
        plan = load_training_plan(conn, set_id)

        if not plan:
            print("No data found for set:", set_id)
            return

        run_session(plan, set_id)

    finally:
        conn.close()


if __name__ == "__main__":
    main()