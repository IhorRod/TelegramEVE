import logging

from aiogram.filters import BaseFilter
from aiogram.types import Message
from base.queries.user import nickname as get_user_by_nickname
from base.commands.user import update as update_user


class NicknameFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user = get_user_by_nickname(message.from_user.username)
        whitelisted = bool(user)
        need_update = user.id != message.from_user.id
        if need_update:
            update_user(message.from_user)
        return whitelisted
