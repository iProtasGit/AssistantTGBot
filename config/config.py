from dataclasses import dataclass
import logging
from environs import Env

logger = logging.getLogger('OnFuture')

@dataclass
class Tg_bot:
    token: str

@dataclass
class Admins:
    ids: list[int]

@dataclass
class Config:
    bot: Tg_bot
    admin_ids: Admins
    
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        bot=Tg_bot(token=env('BOT_TOKEN')),
        admin_ids=Admins(ids=env.list('ADMIN_IDS', subcast=int, delimiter=','))    
    )