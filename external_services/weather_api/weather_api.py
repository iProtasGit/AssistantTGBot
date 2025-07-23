import aiohttp

from logging import getLogger

from .current_weather import CurrentWeather

log = getLogger(__name__)

class WeatherAPI():
    def __init__(self, key: str):
        self.key = key
        self.BASE_URL: str = "http://api.weatherapi.com/v1"
        self.session: aiohttp.ClientSession | None = aiohttp.ClientSession()
    
    async def close_session(self):
        if self.session:
            log.debug("Closing WeatherAPI session")
            if not self.session.closed:
                await self.session.close()
            else:
                log.debug("Session already closed")

    async def get_current_weather(self):
        current_weather = CurrentWeather(
            key=self.key, 
            base_url=self.BASE_URL, 
            session=self.session)
        return await current_weather.get_text_current_weather()