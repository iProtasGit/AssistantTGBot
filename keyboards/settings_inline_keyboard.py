from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import user

kb_builder = InlineKeyboardBuilder()

weather_turn_on_button = InlineKeyboardButton(text=user['inline_buttons']['turn_on_weather'], callback_data=user['inline_buttons']['turn_on_weather'])
weather_turn_off_button = InlineKeyboardButton(text=user['inline_buttons']['turn_off_weather'], callback_data=user['inline_buttons']['turn_off_weather'])

kb_builder.row(weather_turn_on_button, weather_turn_off_button, width=2)

settings_kb: InlineKeyboardMarkup = kb_builder.as_markup() 

