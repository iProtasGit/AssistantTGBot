import logging
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, or_f
from aiogram.types import Message, CallbackQuery

# from keyboards.keyboard_utils import create_inline_kb
from lexicon.lexicon_ru import user, settings
from keyboards.start_keyboard import yes_help_kb, weather_yes_no_kb
from keyboards.settings_inline_keyboard import settings_kb

router = Router()
logger = logging.getLogger('OnFuture')

@router.message(CommandStart())
async def process_start_command(message: Message):
    logger.info('Start command')
    await message.answer(text=user['start'], reply_markup=yes_help_kb)
    
    
@router.message(or_f(Command(commands='help'), F.text == user['button']['help']))
async def process_help_command(message: Message):
    logger.info('Help command')
    await message.answer(text=user['help'])
    
    
@router.message(Command('settings'))
async def process_settings(message: Message):
    logger.info('Settings command')
    await message.answer(text=user['settings'], reply_markup=settings_kb)
    
    
@router.callback_query(
    F.data == settings['turn_on_weather']['callback_data']
    )
async def process_turn_on_weather_button_click(callback: CallbackQuery):
    await callback.answer(text=settings['answers']['turn_on_weather']) 
    
    
@router.callback_query(
    F.data == settings['turn_off_weather']['callback_data']
    )
async def process_turn_off_weather_button_click(callback: CallbackQuery):
    await callback.answer(text=settings['answers']['turn_off_weather'])
     
     
@router.message(F.text == user['button']['yes'])
async def process_yes_button(message: Message):
    logger.info('Start yes button')
    await message.answer(text=user['ready'], reply_markup=weather_yes_no_kb)
    
    
@router.message(F.text == user['button']['weather_no'])
async def process_weather_no_button(message: Message):
    logger.info('Weather no button')
    await message.answer(text=user['no_weather'])
    
    
@router.message()
async def send_echo(message: Message):
    try:
        logger.info(f'{message.message_id}')
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        logger.info(f'{message.message_id}')
        await message.reply(text='Ну что за глупость?!')