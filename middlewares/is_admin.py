from typing import Any, Awaitable, Callable
from logging import getLogger

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User


logger = getLogger('OnFuture') 


class IsAdminMiddleware(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: dict[str, Any]
        ) -> Any:        
        user: User = data.get('event_from_user')

        if user.id not in data.get('admins'):
             logger.warning(f'User {user.username} with id: {user.id} try command "/admin" without permission')
             return await handler(event, data)
        
        logger.info(f'Admin: {user.username} log in')
        
        data['is_admin'] = True
        
        return await handler(event, data)
                