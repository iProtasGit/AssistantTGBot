import asyncio
import logging
import yaml
import logging.config
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from config.config import load_config
from keyboards.set_menu import set_main_menu

from handlers import user
 
async def main(): 
    with open('config/logging_config.yaml', 'rt') as f:
        log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)

    config = load_config()

    logger.info('Starting bot')
    bot = Bot(
        config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    await set_main_menu(bot)

    logger.info('Connecting routers')
    dp.include_routers(user.router)

    logger.info('Connecting middlewares')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())