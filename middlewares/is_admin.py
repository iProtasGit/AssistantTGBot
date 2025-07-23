from typing import Any, Awaitable, Callable
from logging import getLogger

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User


class IsAdminMiddleware(BaseMiddleware):

    async def __call__(
        self, 
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: dict[str, Any]
        ) -> Any:

        log = getLogger(__name__)

        log.debug("IsAdminMiddleware called")

        user: User | None  = data.get("event_from_user") 

        if user is None:
            return await handler(event, data)

        if user.id not in data.get("admins"): # type: ignore
             log.warning(f"User {user.username} with id:" \
                        f"{user.id} try command \"/admin\" without permission")
             return await handler(event, data)
        
        data["is_admin"] = True
        
        return await handler(event, data)
                