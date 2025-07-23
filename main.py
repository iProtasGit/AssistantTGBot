import asyncio
import logging
import logging.config
import yaml
from typing import Any
from logging import Logger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from redis.asyncio import Redis

from config.config import load_config, Config
from keyboards.set_menu import set_main_menu
from lexicon.lexicon_ru import user_ru
from lexicon.lexicon_en import user_en
from middlewares.i18n import TranslatorMiddleware
from middlewares.is_admin import IsAdminMiddleware
from external_services.weather_api import WeatherAPI
from handlers import user, admin
 
async def main(): 
    
    try:
        with open("config/logging_config.yaml", "rt") as f:
            log_config: Any = yaml.safe_load(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(
            "Logging configuration file not found. " \
            "Please ensure 'config/logging_config.yaml' exists."
            )
    logging.config.dictConfig(log_config)
    log: Logger = logging.getLogger(__name__)
    cfg: Config = load_config()
    
    translations: dict[str, dict] = {
        'ru': user_ru,
        'en': user_en
    }

    log.info("Starting Redis")
    try:
        redis = Redis(host="localhost")
    except Exception as e:
        log.error(f"Failed to connect to Redis: {e}")
        raise ConnectionError("Redis connection failed. Please check your Redis server.")
    storage = RedisStorage(redis=redis)

    weather_api = WeatherAPI(cfg.api.weather_api.weather_key)

    log.info("Starting bot")
    bot = Bot(
        cfg.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    await set_main_menu(bot)

    log.info("Connecting routers")
    dp.include_router(admin.router)
    dp.include_router(user.router)

    log.info("Connecting middlewares")
    admin.router.message.outer_middleware(IsAdminMiddleware())
    dp.update.middleware(TranslatorMiddleware())
    
    log.info("Setting up workflow data")
    dp.workflow_data.update(
        translations=translations, 
        admins=cfg.admin_ids.ids, 
        weather_api=weather_api
        )
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())