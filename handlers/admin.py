import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from filters.is_admin import IsAdminFilter

router = Router()
logger = logging.getLogger('OnFuture')

@router.message(Command(commands='admin'), IsAdminFilter())
async def process_admin_command(message: Message):
    logger.info('Admin command')
    await message.answer(
        text='Добро пожаловать господин')
    