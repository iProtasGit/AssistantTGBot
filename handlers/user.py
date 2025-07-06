import logging
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon_ru import user

router = Router()
logger = logging.getLogger('OnFuture')

@router.message(CommandStart())
async def process_start_command(message: Message):
    logger.info('Start command')
    await message.answer(text=user['start'])
    
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    logger.info('Help command')
    await message.answer(text=user['help'])
    
@router.message()
async def send_echo(message: Message):
    try:
        logger.info(f'{message.message_id}')
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        logger.info(f'{message.message_id}')
        await message.reply(text='Ну что за глупость?!')