import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from datetime import time
import config
import os

from handlers import start, countdown, mood, diary, secret, content, owner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(countdown.router)
dp.include_router(mood.router)
dp.include_router(diary.router)
dp.include_router(secret.router)
dp.include_router(content.router)
dp.include_router(owner.router)

async def send_daily_message(chat_id: int):
    from utils.timer import format_countdown
    from handlers.content import PHRASES, COMPLIMENTS, QUOTES, FUNNY_PHRASES
    import random
    
    countdown_text = format_countdown()
    all_phrases = PHRASES + COMPLIMENTS + QUOTES + FUNNY_PHRASES
    phrase = random.choice(all_phrases)
    
    message_text = f"🌅 Доброе утро, любимая!\n\n{phrase}\n\n{countdown_text}"
    
    photos_dir = "data/photos"
    if os.path.exists(photos_dir):
        photos = [f for f in os.listdir(photos_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if photos:
            from aiogram.types import FSInputFile
            photo_path = os.path.join(photos_dir, random.choice(photos))
            try:
                await bot.send_photo(chat_id, FSInputFile(photo_path), caption=message_text)
                return
            except Exception as e:
                logger.error(f"Failed to send photo: {e}")
    
    await bot.send_message(chat_id, message_text)

async def schedule_daily_messages():
    from datetime import datetime, timedelta
    from database import db
    
    schedule_1 = config.DAILY_SCHEDULE_1
    schedule_2 = config.DAILY_SCHEDULE_2
    
    hour1, minute1 = map(int, schedule_1.split(':'))
    hour2, minute2 = map(int, schedule_2.split(':'))
    
    while True:
        now = datetime.now()
        target_time1 = now.replace(hour=hour1, minute=minute1, second=0, microsecond=0)
        target_time2 = now.replace(hour=hour2, minute=minute2, second=0, microsecond=0)
        
        if now >= target_time1 and now < target_time1 + timedelta(minutes=1):
            try:
                db.cursor.execute("SELECT user_id FROM users LIMIT 1")
                result = db.cursor.fetchone()
                if result:
                    user_id = result[0]
                    await send_daily_message(user_id)
            except Exception as e:
                logger.error(f"Failed to send daily message: {e}")
        
        if now >= target_time2 and now < target_time2 + timedelta(minutes=1):
            try:
                db.cursor.execute("SELECT user_id FROM users LIMIT 1")
                result = db.cursor.fetchone()
                if result:
                    user_id = result[0]
                    await send_daily_message(user_id)
            except Exception as e:
                logger.error(f"Failed to send daily message: {e}")
        
        await asyncio.sleep(60)

async def main():
    logger.info("Бот запущен!")
    
    asyncio.create_task(schedule_daily_messages())
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
