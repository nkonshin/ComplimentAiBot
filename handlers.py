import random
import os
from datetime import datetime

from aiogram import types
from aiogram.types import InputFile
from aiogram.dispatcher import FSMContext

from keyboards import answer_kb, END_QUIZ_KB, MAIN_KB, START_QUIZ_KB
from texts import bot_answers as ba, flirting, stikers, quiz
from utils import current_question, get_random_photo, get_random_photo_flirt, get_random_photo_girl, QuizState
from database import log_interaction, get_logs as db_get_logs

QUIZ_LENGTH = len(quiz.IT)


async def cmd_start(message: types.Message):
    # Путь к фотографии
    photo_path = 'original.png'  # Укажите путь к фотографии
    
    # Отправка фотографии с подписью
    await message.reply_photo(photo=InputFile(photo_path),
                              caption=ba.HELP_CMD,
                              reply_markup=MAIN_KB,
                              parse_mode="HTML")
    log_interaction(message.from_user.id, message.from_user.username, 'start')


async def end_quiz(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply(text='Викторина окончена.', reply_markup=MAIN_KB)
    log_interaction(message.from_user.id, message.from_user.username, 'end_quiz')


async def send_photo(message: types.Message):
    await message.answer_photo(photo=types.InputFile(get_random_photo_girl()))
    log_interaction(message.from_user.id, message.from_user.username, 'send_photo')


async def send_flirt(message: types.Message):
    random_flirt = random.choice(flirting.FLIRT)
    await message.answer_photo(photo=types.InputFile(get_random_photo_flirt()),
                               caption=random_flirt)
    log_interaction(message.from_user.id, message.from_user.username, 'send_flirt')


async def send_compliment(message: types.Message):
    random_compliment = random.choice(flirting.COMPLIMENTS)
    await message.answer_photo(photo=types.InputFile(get_random_photo()),
                               caption=random_compliment)
    log_interaction(message.from_user.id, message.from_user.username, 'send_compliment')


async def start_quiz(message: types.Message, state: FSMContext):
    await QuizState.start_quiz.set()
    await message.answer(f'Количество вопросов: {len(quiz.IT)}',
                         reply_markup=END_QUIZ_KB)
    await message.answer(text=ba.QUIZ_DESCRIPTION,
                         reply_markup=START_QUIZ_KB)
    log_interaction(message.from_user.id, message.from_user.username, 'start_quiz')


async def first_question(callback_query: types.CallbackQuery,
                         state: FSMContext):
    user_id = callback_query.from_user.id
    async with state.proxy() as data:
        data['user_id'] = user_id
        data['question_index'] = 0

    await QuizState.next()
    question_text, list_answers, correct_answer = current_question(0)
    keyboard = answer_kb(list_answers, correct_answer)
    await callback_query.message.edit_text(text=question_text,
                                           reply_markup=keyboard)
    log_interaction(callback_query.from_user.id, callback_query.from_user.username, 'first_question')


async def next_question(callback_query: types.CallbackQuery,
                        state: FSMContext):
    user_id = callback_query.from_user.id
    async with state.proxy() as data:
        data['question_index'] += 1

    question_index = data['question_index']

    if question_index < QUIZ_LENGTH:
        question_text, list_answers, correct_answer = current_question(question_index)
        keyboard = answer_kb(list_answers, correct_answer)
        await callback_query.message.edit_text(text=question_text,
                                               reply_markup=keyboard)
        log_interaction(callback_query.from_user.id, callback_query.from_user.username, 'next_question')
    else:
        await state.finish()
        await callback_query.message.edit_text(text='Викторина окончена.', reply_markup=MAIN_KB)
        log_interaction(callback_query.from_user.id, callback_query.from_user.username, 'quiz_finished')


async def losing_quiz(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.message.answer(text=ba.LOSING_QUIZ,
                                        reply_markup=MAIN_KB)
    await callback_query.message.delete()


async def echo(message: types.Message):
    await message.answer(text=ba.ONLY_BUTTONS)


async def get_logs(message: types.Message):
    admin_id = os.getenv('ADMIN_ID')
    if str(message.from_user.id) == admin_id:
        logs = db_get_logs()
        log_text = '\n'.join([f'{log[1]} - {log[2]} - {log[3]} - {log[4]}' for log in logs])
        await message.reply(f'<pre>{log_text}</pre>', parse_mode='HTML')
    else:
        await message.reply('You are not authorized to view the logs.')


async def log_user_id(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    await message.reply(f"Your user ID is {user_id}")
    logging.info(f"User ID: {user_id}, Username: {username}")
