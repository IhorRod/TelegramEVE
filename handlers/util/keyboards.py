from copy import deepcopy
from typing import Dict, Any
import json

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import KeyboardButtonPollType

"""
This module contains the keyboards used in the bot.
"""


class KeyboardButtons:
    Whitelist = KeyboardButton(text='📋 Whitelist')
    Menu = KeyboardButton(text='📋 Menu')
    Back = KeyboardButton(text='🔙 Back')
    Add = KeyboardButton(text='➕ Add')
    Remove = KeyboardButton(text='➖ Remove')
    Update = KeyboardButton(text='🔄 Update')
    Cancel = KeyboardButton(text='❌ Cancel')
    Confirm = KeyboardButton(text='✅ Confirm')


class InlineButtons:
    PLUS = InlineKeyboardButton(text='➕')
    MINUS = InlineKeyboardButton(text='➖')
    UPDATE = InlineKeyboardButton(text='🔄')
    CANCEL = InlineKeyboardButton(text='❌')
    NEXT = InlineKeyboardButton(text='➡️')
    PREVIOUS = InlineKeyboardButton(text='⬅️')

    @staticmethod
    def __encode(data: Dict[str, Any]) -> str:
        return json.dumps(data)

    @staticmethod
    def decode(data: str) -> Dict[str, Any]:
        return json.loads(data)

    @staticmethod
    def plus(data: Dict[str, Any]):
        plus_temp = deepcopy(InlineButtons.PLUS)
        plus_temp.callback_data = InlineButtons.__encode(data)
        return plus_temp

    @staticmethod
    def minus(data: Dict[str, Any]):
        minus_temp = deepcopy(InlineButtons.MINUS)
        minus_temp.callback_data = InlineButtons.__encode(data)
        return minus_temp

    @staticmethod
    def update(data: Dict[str, Any]):
        update_temp = deepcopy(InlineButtons.UPDATE)
        update_temp.callback_data = InlineButtons.__encode(data)
        return update_temp

    @staticmethod
    def cancel(data: Dict[str, Any]):
        cancel_temp = deepcopy(InlineButtons.CANCEL)
        cancel_temp.callback_data = InlineButtons.__encode(data)
        return cancel_temp

    @staticmethod
    def next(data: Dict[str, Any]):
        next_temp = deepcopy(InlineButtons.NEXT)
        next_temp.callback_data = InlineButtons.__encode(data)
        return next_temp

    @staticmethod
    def previous(data: Dict[str, Any]):
        previous_temp = deepcopy(InlineButtons.PREVIOUS)
        previous_temp.callback_data = InlineButtons.__encode(data)
        return previous_temp


class ReplyKeyboards:
    MenuKeyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                       one_time_keyboard=True,
                                       keyboard=[
                                           [KeyboardButtons.Whitelist]
                                       ])
