from typing import Optional

from ..db import TgUser, Session
from aiogram.types.user import User as TelegramUser
from ..model import User as UserModel
from ..queries.user import nickname as get_user_by_nickname


def add(tid: Optional[int], name: Optional[str], fullname: Optional[str], nickname: str) -> Optional[UserModel]:
    """
    Add user to database

    :param tid: ID of the user in Telegram
    :param name: Name of the user
    :param fullname: Full name of the user
    :param nickname: Telegram nickname

    :return: TgUser model instance
    """

    session = Session()
    user = TgUser(tgid=tid, name=name, fullname=fullname, nickname=nickname)
    session.add(user)
    session.commit()
    session.close()
    return get_user_by_nickname(nickname)


def update(user: TelegramUser) -> Optional[UserModel]:
    """
    Update user in database by Telegram nickname

    :param user: TgUser instance
    """

    session = Session()
    ruser = None
    db_user = session.query(TgUser).filter(TgUser.nickname == user.username).first()
    if db_user:
        db_user.tgid = user.id
        db_user.name = user.first_name
        db_user.fullname = user.full_name
        ruser = UserModel(db_user)
        session.commit()
    session.close()
    return ruser
