import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup

from keyboards.keyboard_utils import use_inline_keyboard
from lexicon.lexicon_ru import user_ru
from external_services.weather_api import WeatherAPI

router = Router()

log = logging.getLogger(__name__)

class FSMStartSettings(StatesGroup):
    select_sex = State()
    select_weather = State()
    select_weather_city = State()


@router.message(Command(commands="help"), StateFilter(default_state))
async def process_help_command(
    message: Message, 
    i18n: dict[str, dict]
    ):
    log.debug("Help command started")

    await message.answer(text=i18n["commands"]["help"],)

@router.message(Command(commands="weather"), StateFilter(default_state))
async def process_weather_command(message: Message, weather_api: WeatherAPI):
    log.debug("Weather command started")

    text: str = await weather_api.get_current_weather()
    if not text:
        text = "Не удалось получить данные о погоде." # add to lexicon_ru
   
    await message.answer(text=text)
    
@router.message(Command("settings"), StateFilter(default_state))
async def process_settings(
    message: Message, 
    i18n: dict[str, dict], 
    ):
    log.debug("Settings command started")

    await message.answer(text=i18n["commands"]["settings"], 
                         reply_markup=use_inline_keyboard(2, "settings"))

@router.callback_query(F.data == "turn_on_weather")
async def process_turn_on_weather_button_click(
    callback: CallbackQuery, 
    i18n: dict[str, dict]
    ):
    log.debug("Turn on weather button clicked")

    await callback.answer(text=i18n["answers"]["turn_on_weather"]) 

@router.callback_query(F.data == "turn_off_weather")
async def process_turn_off_weather_button_click(
    callback: CallbackQuery, 
    i18n: dict[str, dict]
    ):
    log.debug("Turn off weather button clicked")

    await callback.answer(text=i18n["answers"]["turn_off_weather"])

@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(
    message: Message, 
    i18n: dict[str, dict], 
    state: FSMContext
    ):
    log.debug("Start command started for new user")

    await message.answer(
        text=i18n["commands"]["start"], 
        reply_markup=use_inline_keyboard(2, "sex"))
    await state.set_state(FSMStartSettings.select_sex)

@router.callback_query(
        F.data.in_(user_ru["inline_buttons"]["sex"].keys()),
        StateFilter(FSMStartSettings.select_sex))
async def process_select_weather(
    callback: CallbackQuery, 
    i18n: dict[str, dict], 
    state: FSMContext
    ):
    log.debug("Start select weather")

    await state.update_data(selected_sex=callback.data)
    await callback.message.edit_text( # type: ignore
        text=i18n["answers"]["selected_sex"], 
        reply_markup=use_inline_keyboard(2, "weather"))
    await state.set_state(FSMStartSettings.select_weather)

@router.callback_query(
        F.data == "yes_weather", 
        StateFilter(FSMStartSettings.select_weather))
async def process_yes_button(
    callback: CallbackQuery, 
    i18n: dict[str, dict], 
    state: FSMContext
    ):
    log.debug("Start weather yes button")

    await state.update_data(selected_weather=callback.data)
    await callback.message.edit_text( # type: ignore
        text=i18n['answers']['ready'],
        reply_markup=use_inline_keyboard(2, "city_of_weather"))
    await state.set_state(FSMStartSettings.select_weather_city)
    
@router.callback_query(
    F.data.in_(user_ru["inline_buttons"]["city_of_weather"].keys()),
    StateFilter(FSMStartSettings.select_weather_city))
async def process_over_first_settings(
    callback: CallbackQuery, 
    i18n: dict[str, dict], 
    state: FSMContext
    ):
    log.debug("Start select city of weather")

    await state.update_data(selected_city_weather=callback.data)
    info: dict = await state.get_data()
    all_info = f"1.Ваш пол - {info['selected_sex']}\n2.Оповещать о погоде?" \
               f"- {info['selected_weather']}\n" \
               f"3.Выбранный город - {info['selected_city_weather']}"
    result_text = i18n["answers"]["over_first_settings"] + all_info
    await state.clear()
    
    await callback.message.delete() # type: ignore
    await callback.message.answer(text=result_text) # type: ignore
    
@router.callback_query(
        F.data == "no_weather", 
        StateFilter(FSMStartSettings.select_weather))
async def process_weather_no_button(
    callback: CallbackQuery, 
    i18n: dict[str, dict], 
    state: FSMContext
    ):
    log.debug("Weather no button clicked")

    await state.update_data(selected_weather=callback.data)
    info: dict = await state.get_data()
    all_info = f"<i>1.Ваш пол - {info['selected_sex']}\n" \
               f"2.Оповещать о погоде? - {info['selected_weather']}</i>"
    result_text = i18n["answers"]["over_first_settings"] + all_info
    await state.clear()

    await callback.answer(text=result_text)
    
@router.message()
async def send_echo(message: Message):
    try:
        log.info(f"Echo with message id: {message.message_id}")
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        log.info(f"Echo with message id: {message.message_id}")
        await message.reply(text='Ну что за глупость?!')