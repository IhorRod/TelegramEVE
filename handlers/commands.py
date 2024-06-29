from aiogram import Router, types
from aiogram.filters import Command
from handlers.filters import NicknameFilter

router = Router(name='commands')
router.message.filter(NicknameFilter())


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Hello!')
