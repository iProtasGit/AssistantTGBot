from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

import logging

logger = logging.getLogger(__name__)



class IsAdminFilter(BaseFilter):
    async def __call__(self, event: TelegramObject, is_admin: bool):
        if is_admin:
            logger.debug(f"Used filter IsAdminFilter - {event}") 
            return True