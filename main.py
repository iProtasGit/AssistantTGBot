import asyncio
import logging
import yaml
import logging.config
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from config.config import load_config
from keyboards.set_menu import set_main_menu
from lexicon.lexicon_ru import user_ru
from lexicon.lexicon_en import user_en
from middlewares.i18n import TranslatorMiddleware

from handlers import user
 
async def main(): 
    with open('config/logging_config.yaml', 'rt') as f:
        log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)

    config = load_config()
    
    translations = {
        'default': 'ru',
        'ru': user_ru,
        'en': user_en
    }

    logger.info('Starting bot')
    bot = Bot(
        config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    await set_main_menu(bot)

    logger.info('Connecting routers')
    dp.include_routers(user.router)

    logger.info('Connecting middlewares')
    dp.update.middleware(TranslatorMiddleware())
    
    dp.workflow_data.update(translations=translations)
    

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())