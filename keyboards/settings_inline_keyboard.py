from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import settings

kb_builder = InlineKeyboardBuilder()

buttons: list[InlineKeyboardButton] = []

buttons.append(InlineKeyboardButton(
    text=settings['turn_on_weather']['text'],
    callback_data=settings['turn_on_weather']['callback_data']
))
buttons.append(InlineKeyboardButton(
    text=settings['turn_off_weather']['text'],
    callback_data=settings['turn_off_weather']['callback_data']
))
buttons.append(InlineKeyboardButton(
    text=settings['call_developer']['text'],
    url=settings['call_developer']['url']
))

       

kb_builder.row(*buttons, width=2)

settings_kb: InlineKeyboardMarkup = kb_builder.as_markup() 

