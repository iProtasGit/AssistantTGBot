import logging
import logging.config
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)
import yaml

from config.config import load_config
 

config = load_config()
BOT_TOKEN = config.bot.token

with open('config/logging_config.yaml', 'rt') as f:
    log_config = yaml.safe_load(f.read())
logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)


# Создаем объекты бота и диспетчера
config = load_config()

logger.debug('Running Bot')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем объекты инлайн-кнопок
big_button_1 = InlineKeyboardButton(
    text='БОЛЬШАЯ КНОПКА 1',
    callback_data='big_button_1_pressed'
)

big_button_2 = InlineKeyboardButton(
    text='БОЛЬШАЯ КНОПКА 2',
    callback_data='big_button_2_pressed'
)

# Создаем объект инлайн-клавиатуры
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_1],
                     [big_button_2]])


# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру с инлайн-кнопками
@dp.message(CommandStart())
async def process_start_command(message: Message):
    logger.error("ALERT TEST")
    await message.answer(
        text='Это инлайн-кнопки. Нажми на любую!',
        reply_markup=keyboard
    )


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_1_pressed'
@dp.callback_query(F.data == 'big_button_1_pressed')
async def process_button_1_press(callback: CallbackQuery):
    if callback.message.text != 'Была нажата БОЛЬШАЯ КНОПКА 1': # type: ignore
        await callback.message.edit_text( # type: ignore
            text='Была нажата БОЛЬШАЯ КНОПКА 1',
            reply_markup=callback.message.reply_markup) # type: ignore
    await callback.answer(
        text='Ура! Нажата кнопка 1',
        show_alert=True
    )


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_2_pressed'
@dp.callback_query(F.data == 'big_button_2_pressed')
async def process_button_2_press(callback: CallbackQuery):
    if callback.message.text != 'Была нажата БОЛЬШАЯ КНОПКА 2': # type: ignore
        await callback.message.edit_text( # type: ignore
            text='Была нажата БОЛЬШАЯ КНОПКА 2',
            reply_markup=callback.message.reply_markup # type: ignore
        )
    await callback.answer(text='Ура! Нажата кнопка 2')


if __name__ == '__main__':
    dp.run_polling(bot)
    