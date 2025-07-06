from dataclasses import dataclass
import logging
from environs import Env

logger = logging.getLogger('OnFuture')

@dataclass
class TgBot:
    token: str

@dataclass
class Config:
    bot: TgBot
    
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    logger.debug('initialized config file')
    return Config(
        bot=TgBot(token=env('BOT_TOKEN')),
    )