import logging
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, or_f
from aiogram.types import Message, CallbackQuery

from keyboards.keyboard_utils import use_inline_keyboard
from lexicon.lexicon_ru import user_ru

router = Router()
logger = logging.getLogger('OnFuture')

@router.message(CommandStart())
async def process_start_command(message: Message, i18n: dict[str, str | dict]):
    logger.debug('Start command started')
    await message.answer(
        text=i18n['commands']['start'], 
        reply_markup=use_inline_keyboard(2, 'who_i_am'))
    
    
@router.message(or_f(Command(commands='help')))
async def process_help_command(message: Message, i18n):
    logger.debug('Help command started')
    await message.answer(text=i18n['commands']['help'])
    
    
@router.message(Command('settings'))
async def process_settings(message: Message, i18n):
    logger.debug('Settings command started')
    await message.answer(text=i18n['commands']['settings'], 
                         reply_markup=use_inline_keyboard(2, 'settings'))

@router.callback_query(F.data.in_(user_ru['inline_buttons']['who_i_am'].keys()))
async def process_named(callback: CallbackQuery, i18n):
    await callback.message.edit_text(
        text=i18n['answers']['named'], 
        reply_markup=use_inline_keyboard(2, 'weather'))
    
    
@router.callback_query(F.data == 'turn_weather')
async def process_turn_on_weather_button_click(callback: CallbackQuery, i18n):
    await callback.answer(text=i18n['answers']['turn_on_weather']) 
    
    
@router.callback_query(F.data == 'turn_on_weather')
async def process_turn_off_weather_button_click(callback: CallbackQuery, i18n):
    await callback.answer(text=i18n['answers']['turn_off_weather'])
     
     
@router.callback_query(F.data == 'yes_weather')
async def process_yes_button(callback: CallbackQuery, i18n):
    logger.debug('Start yes button')
    await callback.message.edit_text(
        text=i18n['answers']['ready'],
        reply_markup=use_inline_keyboard(2, 'city_of_weather'))
    

@router.callback_query(
    F.data.in_(user_ru['inline_buttons']['city_of_weather'].keys()))
async def process_city_of_weather_button(callback: CallbackQuery, i18n):
    logger.debug('City of weather selected')
    await callback.message.answer(text=i18n['answers']['selected_city_of_weather'])
    
    
@router.callback_query(F.data == 'no_weather')
async def process_weather_no_button(callback: CallbackQuery, i18n):
    logger.debug('Weather no button')
    await callback.answer(text=i18n['answers']['no_weather'])
    
    
@router.message()
async def send_echo(message: Message):
    try:
        logger.info(f'{message.message_id}')
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        logger.info(f'{message.message_id}')
        await message.reply(text='Ну что за глупость?!')