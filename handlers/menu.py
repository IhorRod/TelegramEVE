from aiogram import Router, types
from handlers.util.filters import NicknameFilter
from handlers.util.keyboards import KeyboardButtons, InlineButtons
from aiogram import F
from base.queries.user import users as get_users
from aiogram.types import InlineKeyboardMarkup

"""
This module contains the menu handler.
"""

router = Router(name='menu')
router.message.filter(NicknameFilter())


@router.message(F.text == KeyboardButtons.Whitelist.text)
async def whitelist(message: types.Message):
    users = get_users(0, 10)
    text = 'Whitelist\n\n'
    for user in users:
        text += f'{user.fullname} - {user.nickname}\n'

    if len(users) == 10:
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineButtons.next({'from': 10, 'to': 20})
        ]])
        await message.answer(text, reply_markup=kb)
    else:
        await message.answer(text)


@router.callback_query(F.text == InlineButtons.NEXT.text)
async def next_user(callback_query: types.CallbackQuery, callback_data: str):
    data = InlineButtons.decode(callback_data)
    users = get_users(data['from'], data['to'])
    text = 'Whitelist\n\n'
    for user in users:
        text += f'{user.fullname} - {user.nickname}\n'

    if len(users) == 10:
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineButtons.next({'from': data['to'], 'to': data['to'] + 10}),
            InlineButtons.previous({'from': data['from'], 'to': data['from'] - 10})
        ]])
        await callback_query.message.edit_text(text, reply_markup=kb)
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineButtons.previous({'from': data['from'], 'to': data['from'] - 10})
        ]])
        await callback_query.message.edit_text(text, reply_markup=kb)


@router.callback_query(F.text == InlineButtons.PREVIOUS.text)
async def previous_user(callback_query: types.CallbackQuery, callback_data: str):
    data = InlineButtons.decode(callback_data)
    users = get_users(data['from'], data['to'])
    text = 'Whitelist\n\n'
    for user in users:
        text += f'{user.fullname} - {user.nickname}\n'

    if len(users) == 10:
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineButtons.next({'from': data['to'], 'to': data['to'] + 10}),
            InlineButtons.previous({'from': data['from'], 'to': data['from'] - 10})
        ]])
        await callback_query.message.edit_text(text, reply_markup=kb)
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineButtons.previous({'from': data['from'], 'to': data['from'] - 10})
        ]])
        await callback_query.message.edit_text(text, reply_markup=kb)
