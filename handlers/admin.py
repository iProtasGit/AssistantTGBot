import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from filters.is_admin import IsAdminFilter

router = Router()

log = logging.getLogger(__name__)

'''Tested admin command handler'''

@router.message(Command(commands="admin"), IsAdminFilter())
async def process_admin_command(message: Message):
    log.info("Admin command started")
    await message.answer(
        text="Добро пожаловать господин")
    