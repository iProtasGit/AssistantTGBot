from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import inline_buttons

def create_new_inline_kb(
    width: int,
    *args: str,
    **kwargs: str) -> InlineKeyboardMarkup:
    
    kb_builder = InlineKeyboardBuilder()
    
    buttons: list[InlineKeyboardButton] = []
    
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=inline_buttons[button] if button in inline_buttons else button,  # type: ignore
                callback_data=button
        ))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))
    
    kb_builder.row(*buttons, width=width)
    
    return kb_builder.as_markup() 