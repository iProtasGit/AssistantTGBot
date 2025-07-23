import aiohttp
from logging import getLogger

from msgspec import Struct
from msgspec import DecodeError
from msgspec.json import decode

log = getLogger(__name__)


class Condition(Struct):
    text: str


class Current(Struct):
    temp_c: float
    temp_f: float
    feelslike_c: float
    feelslike_f: float
    condition: Condition

    def __post_init__(self):
        self.temp_c = int(round(self.temp_c))
        self.temp_f = int(round(self.temp_f))
        self.feelslike_c = int(round(self.feelslike_c))
        self.feelslike_f = int(round(self.feelslike_f))


class WeatherData(Struct):
    current: Current
    
class CurrentWeather():
    def __init__(self, key: str, base_url: str, session: aiohttp.ClientSession | None = None):
        self.BASE_URL = base_url
        self.ENDPOINT: str = "/current.json"
        self.params: dict[str, str] = {
            "key": key,
            "q": "55.557037,37.708760",
            "lang": "ru",
        }
        self.session = session

        log.debug(f"Initialized CurrentWeather with session: {self.session!r}")

    async def _get_weather(self) -> WeatherData:
        log.debug("Entering _get_weather")
        log.debug(f"URL: {self.BASE_URL+self.ENDPOINT}")
        try:
            async with self.session.get( # type: ignore
                url=self.BASE_URL+self.ENDPOINT, 
                params=self.params
                ) as resp:
                log.debug(f"Response status: {resp.status}")

                if resp.status != 200:
                    error_text = await resp.text()
                    log.error(f"Failed to fetch weather: {resp.status} - {error_text}")
                    raise aiohttp.ClientResponseError(
                        resp.request_info, 
                        resp.history, 
                        status=resp.status, 
                        message=f"Failed to fetch weather data: {resp.status}"
                    )
                
                resp_data: bytes = await resp.read()
                return decode(resp_data, type=WeatherData)
        except aiohttp.ClientConnectionError as e:
            log.fatal(f"Network error in _get_weather: {e}")
            raise
        except DecodeError as e:
            log.fatal(f"JSON decode error in _get_weather: {e}")
            raise
    
    async def get_text_current_weather(self) -> str:
        weather_data: WeatherData = await self._get_weather()
        text: str = f"🏙️Сейчас в вашем городе " \
                    f"{weather_data.current.condition.text.lower()}, " \
                    f"{weather_data.current.temp_c}°C, ощущается, как " \
                    f"{weather_data.current.feelslike_c}°C"
        return text
