import os
import random

from dotenv import load_dotenv
from aiogram.dispatcher.filters.state import State, StatesGroup

from texts import quiz

load_dotenv()

# Хранилище для уже показанных фотографий
shown_photos = []


def get_random_photo() -> str:
    photo_dirs = os.getenv('PHOTOS_COMPLIMENT_DIRECTORY')
    if not os.path.exists(photo_dirs):
        raise Exception('No photo directory')

    list_photo = os.listdir(photo_dirs)
    if not list_photo:
        raise Exception('Photo folder is empty')

    random_photo = random.choice(list_photo)
    path_photo = os.path.join(photo_dirs, random_photo)
    return path_photo

def get_random_photo_flirt() -> str:
    photo_dirs = os.getenv('PHOTOS_FLIRT_DIRECTORY')
    if not os.path.exists(photo_dirs):
        raise Exception('No photo directory')

    list_photo = os.listdir(photo_dirs)
    if not list_photo:
        raise Exception('Photo folder is empty')

    random_photo = random.choice(list_photo)
    path_photo = os.path.join(photo_dirs, random_photo)
    return path_photo

def get_random_photo_girl() -> str:
    global shown_photos
    photo_dirs = os.getenv('PHOTOS_GIRL_DIRECTORY')
    if not os.path.exists(photo_dirs):
        raise Exception('No photo directory')

    list_photo = os.listdir(photo_dirs)
    if not list_photo:
        raise Exception('Photo folder is empty')

    # Если все фотографии показаны, сбросить список показанных фотографий
    if len(shown_photos) == len(list_photo):
        shown_photos = []

    # Найти фотографию, которая еще не была показана
    remaining_photos = [photo for photo in list_photo if photo not in shown_photos]
    random_photo = random.choice(remaining_photos)
    
    # Добавить выбранную фотографию в список показанных
    shown_photos.append(random_photo)

    path_photo = os.path.join(photo_dirs, random_photo)
    return path_photo


def current_question(question_number: int) -> tuple[str, list, str]:
    quiz_number = quiz.IT[question_number]
    question_text = quiz_number.get("question")
    list_answers = quiz_number.get("answers")
    correct_answer = quiz_number.get("correct_answer")
    return question_text, list_answers, correct_answer

class QuizState(StatesGroup):
    start_quiz = State()
    number_correct_answers = State()





'''def get_random_photo_girl() -> str:
    photo_dirs = os.getenv('PHOTOS_GIRL_DIRECTORY')
    if not os.path.exists(photo_dirs):
        raise Exception('No photo directory')

    list_photo = os.listdir(photo_dirs)
    if not list_photo:
        raise Exception('Photo folder is empty')

    random_photo = random.choice(list_photo)
    path_photo = os.path.join(photo_dirs, random_photo)
    return path_photo
'''