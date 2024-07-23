from aiogram import Router, types
from aiogram.filters import Command
from handlers.util.filters import NicknameFilter
from base.commands.user import add as add_user
from handlers.util.keyboards import ReplyKeyboards

"""
This module contains the command handlers.
"""

router = Router(name='commands')
router.message.filter(NicknameFilter())


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(
        'Welcome to the bot, that helps manage different EVE tasks!',
        reply_markup=ReplyKeyboards.MenuKeyboard)


@router.message(Command('whitelist'))
async def cmd_whitelist(message: types.Message):
    nickname = message.text.split(' ')[1]
    user = add_user(None, None, None, nickname)
    if user:
        await message.answer(f'TgUser {nickname} added to the whitelist')
    else:
        await message.answer(f'Failed to add user {nickname} to the whitelist')
