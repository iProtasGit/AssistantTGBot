from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


from keyboards.mainMenuKB import main_menu
from texts.start_text import start_text

router = Router()

@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(
        start_text(),
        reply_markup=main_menu()
    ) 