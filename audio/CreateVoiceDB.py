import asyncio
import json
import os
import edge_tts
import pyodbc

from dotenv import load_dotenv

load_dotenv("config.env")

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

# ==========================================================
# Database
# ==========================================================

def connect_db():

    print("Connecting to SQL Server...")

    conn = pyodbc.connect(CONNECTION_STRING)

    print("Connected.")

    return conn


# ==========================================================
# Очистка таблиц
# ==========================================================

def clear_database(cursor):

    print("Clearing tables...")

    cursor.execute("DELETE FROM dbo.languages")
    cursor.execute("DELETE FROM dbo.tts_voices")

    print("Done.")


# ==========================================================
# Импорт одного голоса
# ==========================================================

def insert_voice(cursor, voice):

    voice_tag = voice.get("VoiceTag", {})

    personalities = ";".join(
        voice_tag.get("VoicePersonalities", [])
    )

    categories = ";".join(
        voice_tag.get("ContentCategories", [])
    )

    locale = voice.get("Locale", "")

    language_code = locale.split("-")[0]

    cursor.execute(
        """
        INSERT INTO dbo.tts_voices
        (
            short_name,
            locale,
            language_code,
            gender,
            friendly_name,
            status,
            codec,
            personalities,
            categories,
            raw_json
        )
        VALUES
        (
            ?,?,?,?,?,?,?,?,?,?
        )
        """,

        voice.get("ShortName"),

        locale,

        language_code,

        voice.get("Gender"),

        voice.get("FriendlyName"),

        voice.get("Status"),

        voice.get("SuggestedCodec"),

        personalities,

        categories,

        json.dumps(
            voice,
            ensure_ascii=False
        )
    )


# ==========================================================
# Импорт голосов
# ==========================================================

async def import_voices(cursor):

    print()

    print("Loading voices from Microsoft...")

    voices = await edge_tts.list_voices()

    print(f"Found {len(voices)} voices")

    print()

    language_map = {}

    count = 0

    for voice in voices:

        insert_voice(cursor, voice)

        locale = voice["Locale"]

        language = locale.split("-")[0]

        if language not in language_map:

            language_map[language] = {

                "locale": locale,

                "default_voice": voice["ShortName"]

            }

        count += 1

        if count % 100 == 0:

            print(f"{count} voices imported...")

    print()

    print(f"Imported {count} voices")

    return language_map

# ==========================================================
# Импорт таблицы languages
# ==========================================================

def insert_languages(cursor, language_map):

    print()
    print("Importing languages...")

    count = 0

    for language_code in sorted(language_map.keys()):

        item = language_map[language_code]

        cursor.execute(
            """
            INSERT INTO dbo.languages
            (
                language_code,
                locale,
                language_name,
                native_name,
                country,
                default_voice,
                enabled
            )
            VALUES
            (
                ?,?,?,?,?,?,1
            )
            """,

            language_code,
            item["locale"],
            language_code.upper(),     # временно
            None,
            None,
            item["default_voice"]
        )

        count += 1

    print(f"Imported {count} languages")


# ==========================================================
# Main
# ==========================================================

async def main():

    conn = connect_db()
    cursor = conn.cursor()

    try:

        clear_database(cursor)

        language_map = await import_voices(cursor)

        insert_languages(cursor, language_map)

        conn.commit()

        print()
        print("=" * 50)
        print("Import completed successfully")
        print("=" * 50)
        print(f"Voices    : {cursor.execute('SELECT COUNT(*) FROM dbo.tts_voices').fetchone()[0]}")
        print(f"Languages : {cursor.execute('SELECT COUNT(*) FROM dbo.languages').fetchone()[0]}")

    except Exception as ex:

        conn.rollback()
        print()
        print("ERROR:")
        print(ex)

    finally:

        cursor.close()
        conn.close()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    asyncio.run(main())