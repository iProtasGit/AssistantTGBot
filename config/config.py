import logging
from dataclasses import dataclass

from environs import Env

log = logging.getLogger(__name__)

@dataclass(frozen=True)
class WeatherAPI():
    weather_key: str

@dataclass(frozen=True)
class API():
    weather_api: WeatherAPI

@dataclass(frozen=True)
class Tg_bot():
    token: str

@dataclass(frozen=True)
class Admins:
    ids: list[int]

@dataclass(frozen=True)
class Config:
    bot: Tg_bot
    admin_ids: Admins
    api: API
    
def load_config(path: str | None = None) -> Config:
    env = Env()

    try:
        env.read_env(path)
    except FileNotFoundError:
        log.warning(f"Config file {path} not found. Using environment variables.")
        raise Exception(f"Config file {path} not found. Please create it or set environment variables.")
    return Config(
        bot=Tg_bot(token=env("BOT_TOKEN")),
        admin_ids=Admins(ids=env.list("ADMIN_IDS", subcast=int, delimiter=",")),
        api=API(WeatherAPI(env("WEATHER_API_KEY")))   
    )