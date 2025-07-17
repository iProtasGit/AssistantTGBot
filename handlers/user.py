import logging
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, or_f
from aiogram.types import Message, CallbackQuery

from keyboards.start_keyboard import yes_help_kb, weather_yes_no_kb
from keyboards.settings_inline_keyboard import settings_kb
from lexicon.lexicon_ru import user_ru

router = Router()
logger = logging.getLogger('OnFuture')

@router.message(CommandStart())
async def process_start_command(message: Message, i18n: dict[str, str | dict]):
    logger.info('Start command')
    await message.answer(
        text=i18n['commands']['start'], 
        reply_markup=yes_help_kb)
    
    
@router.message(or_f(Command(commands='help'), F.text == user_ru['buttons']['help']))
async def process_help_command(message: Message, i18n):
    logger.info('Help command')
    await message.answer(text=i18n['commands']['help'])
    
    
@router.message(Command('settings'))
async def process_settings(message: Message, i18n):
    logger.info(f'Settings command {i18n["commands"]["settings"]}')
    await message.answer(text=i18n['commands']['settings'], reply_markup=settings_kb)
    
    
@router.callback_query(
    F.data == user_ru['inline_buttons']['turn_on_weather']['callback_data']
    )
async def process_turn_on_weather_button_click(callback: CallbackQuery, i18n):
    await callback.answer(text=i18n['answers']['turn_on_weather']) 
    
    
@router.callback_query(
    F.data == user_ru['inline_buttons']['turn_off_weather']['callback_data']
    )
async def process_turn_off_weather_button_click(callback: CallbackQuery, i18n):
    await callback.answer(text=i18n['answers']['turn_off_weather'])
     
     
@router.message(F.text == user_ru['buttons']['yes'])
async def process_yes_button(message: Message, i18n):
    logger.info('Start yes button')
    await message.answer(text=i18n['answers']['ready'], reply_markup=weather_yes_no_kb)
    
    
@router.message(F.text == user_ru['buttons']['weather_no'])
async def process_weather_no_button(message: Message, i18n):
    logger.info('Weather no button')
    await message.answer(text=i18n['answers']['no_weather'])
    
    
@router.message()
async def send_echo(message: Message):
    try:
        logger.info(f'{message.message_id}')
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        logger.info(f'{message.message_id}')
        await message.reply(text='Ну что за глупость?!')