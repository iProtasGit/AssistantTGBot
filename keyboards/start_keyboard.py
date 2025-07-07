from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from lexicon.lexicon_ru import user

button_yes = KeyboardButton(text=user['button']['yes'])
button_help = KeyboardButton(text=user['button']['help'])

yes_help_kb_builder = ReplyKeyboardBuilder()
yes_help_kb_builder.row(button_yes, button_help, width=2)

yes_help_kb: ReplyKeyboardMarkup = yes_help_kb_builder.as_markup(
    one_time_keyboard=True, resize_keyboard=True
)

button_weather_yes = KeyboardButton(text=user['button']['weather_yes'], request_location=True)
button_weather_no = KeyboardButton(text=user['button']['weather_no'])

weather_yes_no_kb_builder = ReplyKeyboardBuilder()
weather_yes_no_kb_builder.row(button_weather_yes, button_weather_no, width=2)

weather_yes_no_kb: ReplyKeyboardMarkup= weather_yes_no_kb_builder.as_markup(
    one_time_keyboard=True, resize_keyboard=True
)

