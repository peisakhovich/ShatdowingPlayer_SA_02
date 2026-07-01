import asyncio
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

cn = pyodbc.connect(CONNECTION_STRING)

cursor = cn.cursor()


async def load():

    voices = await edge_tts.list_voices()

    locales = {}

    for v in voices:

        locale = v["Locale"]

        if locale not in locales:

            parts = locale.split("-")

            language = parts[0]
            country = parts[1] if len(parts) > 1 else ""

            locales[locale] = (
                locale,
                language,
                country,
                locale,
                locale
            )

    # ---------- languages ----------

    for row in locales.values():

        cursor.execute("""

IF NOT EXISTS
(
SELECT 1
FROM dbo.languages
WHERE locale=?
)

INSERT INTO dbo.languages
(
locale,
language_code,
country_code,
english_name,
native_name
)

VALUES
(
?,?,?,?,?
)

""", row[0], *row)

    # ---------- voices ----------

    for v in voices:

        cursor.execute("""

MERGE dbo.tts_voices AS T

USING
(
SELECT
? AS short_name
) S

ON T.short_name=S.short_name

WHEN MATCHED THEN

UPDATE SET

display_name=?,
locale=?,
gender=?,
voice_type='Neural',
friendly_name=?,
status='Active'

WHEN NOT MATCHED THEN

INSERT
(
short_name,
display_name,
locale,
gender,
voice_type,
friendly_name,
status
)

VALUES
(
?,
?,
?,
?,
'Neural',
?,
'Active'
);

""",

v["ShortName"],
v["FriendlyName"],
v["Locale"],
v["Gender"],
v["FriendlyName"],

v["ShortName"],
v["FriendlyName"],
v["Locale"],
v["Gender"],
v["FriendlyName"]
)

    cn.commit()


asyncio.run(load())

cursor.close()
cn.close()