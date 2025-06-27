from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Добавить')
    kb.button(text='Создать сводку')
    kb.button(text='Админка')
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)