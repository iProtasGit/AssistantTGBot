import asyncio
import logging
import yaml
import logging.config

from redis.asyncio import Redis

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage


from config.config import load_config
from keyboards.set_menu import set_main_menu
from lexicon.lexicon_ru import user_ru
from lexicon.lexicon_en import user_en
from middlewares.i18n import TranslatorMiddleware
from middlewares.is_admin import IsAdminMiddleware

from handlers import user, admin
 
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

    logger.info("Starting Redis")
    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)

    logger.info('Starting bot')
    bot = Bot(
        config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    await set_main_menu(bot)

    logger.info('Connecting routers')
    dp.include_router(admin.router)
    dp.include_router(user.router)

    logger.info('Connecting middlewares')
    admin.router.message.outer_middleware(IsAdminMiddleware())
    dp.update.middleware(TranslatorMiddleware())
    
    dp.workflow_data.update(translations=translations, admins=config.admin_ids.ids)
    

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())