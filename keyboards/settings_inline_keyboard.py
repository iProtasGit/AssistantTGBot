from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import user_ru

kb_builder = InlineKeyboardBuilder()

buttons: list[InlineKeyboardButton] = []

buttons.append(InlineKeyboardButton(
    text=user_ru['inline_buttons']['turn_on_weather']['text'],
    callback_data=user_ru['inline_buttons']['turn_on_weather']['callback_data']
))
buttons.append(InlineKeyboardButton(
    text=user_ru['inline_buttons']['turn_off_weather']['text'],
    callback_data=user_ru['inline_buttons']['turn_off_weather']['callback_data']
))
buttons.append(InlineKeyboardButton(
    text=user_ru['inline_buttons']['call_developer']['text'],
    url=user_ru['inline_buttons']['call_developer']['url']
))

       

kb_builder.row(*buttons, width=2)

settings_kb: InlineKeyboardMarkup = kb_builder.as_markup() 

