import logging
import os
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types  # Add types here
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
import pytz

from handlers import (
    cmd_start,
    end_quiz,
    send_photo,
    send_flirt,
    send_compliment,
    start_quiz,
    first_question,
    next_question,
    losing_quiz, echo, get_logs, log_user_id,
)
from utils import QuizState

logging.basicConfig(level=logging.INFO)
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

dp.register_message_handler(cmd_start, commands=['start'])
dp.register_message_handler(end_quiz, commands=['cancel'], state='*')
dp.register_message_handler(end_quiz, Text('Закончить викторину'), state='*')
dp.register_message_handler(send_photo, Text('Покажи пупсика 📸'))
dp.register_message_handler(send_flirt, Text('Лучший подкат в твоей жизни 🤭'))
dp.register_message_handler(send_compliment, Text('Получить комплимент 😍'))
dp.register_message_handler(start_quiz, Text('Викторина 🎯'))
dp.register_callback_query_handler(first_question, Text('start_quiz'), state=QuizState.start_quiz)
dp.register_callback_query_handler(next_question, Text('correct_answer'), state=QuizState.number_correct_answers)
dp.register_callback_query_handler(losing_quiz, Text('wrong_answer'), state=QuizState.number_correct_answers)
dp.register_message_handler(get_logs, commands=['get_logs'])
dp.register_message_handler(log_user_id, commands=['get_user_id'])

# Function to send daily message
async def send_daily_message():
    user_id = os.getenv('YOUR_LOVE_ID')  # Replace with the actual numeric user ID
    Bot.set_current(bot)  # Set the current bot instance
    message = types.Message(chat=types.Chat(id=user_id, type='private'), from_user=types.User(id=user_id, is_bot=False, first_name='User'))
    await send_compliment(message)

# Set up the scheduler
scheduler = AsyncIOScheduler()
scheduler.add_job(send_daily_message, CronTrigger(hour=9, minute=0, timezone=pytz.timezone('Europe/Moscow')))
scheduler.start()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
