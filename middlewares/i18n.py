from typing import Any, Awaitable, Callable
from logging import getLogger

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: dict[str, Any]
        ) -> Any:
        
        log = getLogger(__name__) 

        log.debug("TranslatorMiddleware called")
        
        user: User | None = data.get("event_from_user") 
        
        if user is None:
            return await handler(event, data)
        
        user_lang: str | None = user.language_code

        if user_lang is None:
            user_lang = "en"

        translations: dict[str, dict] = data.get("translations") # type: ignore

        i18n: str = translations.get(user_lang) # type: ignore

        match i18n:
            case 'ru':
                data["i18n"] = translations.get("ru") # type: ignore
            case '!en': # temporarily unavailable
                data["i18n"] = translations.get("ru") # type: ignore
            case _:
                log.warning(f"Unsupported language '{user_lang}', using default")
                data["i18n"] = translations.get("ru") # type: ignore
        
        return await handler(event, data)