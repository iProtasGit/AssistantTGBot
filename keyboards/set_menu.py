from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon_ru import main_menu

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in main_menu.items()
    ]
    await bot.set_my_commands(main_menu_commands)