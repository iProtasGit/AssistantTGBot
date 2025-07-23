from logging import getLogger

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import user_ru

log = getLogger(__name__)


def use_inline_keyboard(
    width: int,
    name: str
    ) -> InlineKeyboardMarkup | None:
    
    kb_builder = InlineKeyboardBuilder()
    
    buttons: list[InlineKeyboardButton] = []

    if user_ru["inline_buttons"].get(name) is None:
        log.error(f"Inline buttons for '{name}' not found in lexicon.")
        return None
    
    for button, text in user_ru["inline_buttons"][name].items():
        if button.startswith("url:"):
            buttons.append(InlineKeyboardButton(
                text=text,
                url=button[4:]
            ))
        else:
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))
            
    kb_builder.row(*buttons, width=width)
    
    return kb_builder.as_markup()
    
    