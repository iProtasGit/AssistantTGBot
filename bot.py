import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from os import getenv
from dotenv import load_dotenv

from handlers import startMenu

# dotenv_path = path.join(getcwd(), 'Config', '.env')
load_dotenv()

async def main():
    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(token=getenv('bot_token'), default=DefaultBotProperties(
    parse_mode=ParseMode.HTML
))
    dp = Dispatcher()

    dp.include_routers(startMenu.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())