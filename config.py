import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "RomkaStp")
DEPARTURE_DATE = datetime.fromisoformat(os.getenv("DEPARTURE_DATE", "2026-06-28 22:00"))
RETURN_DATE = datetime.fromisoformat(os.getenv("RETURN_DATE", "2026-08-02"))
DAILY_SCHEDULE_1 = os.getenv("DAILY_SCHEDULE_1", "09:00")
DAILY_SCHEDULE_2 = os.getenv("DAILY_SCHEDULE_2", "20:00")

DB_NAME = "bot_database.db"
