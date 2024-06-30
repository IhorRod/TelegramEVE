from typing import Optional

from base.db import User, Session
from aiogram.types.user import User as TelegramUser
from base.model import User as UserModel
from base.queries.user import nickname as get_user_by_nickname


def add(tid: Optional[int], name: Optional[str], fullname: Optional[str], nickname: str) -> Optional[UserModel]:
    """
    Add user to database

    :param tid: ID of the user in Telegram
    :param name: Name of the user
    :param fullname: Full name of the user
    :param nickname: Telegram nickname

    :return: User model instance
    """

    session = Session()
    user = User(tgid=tid, name=name, fullname=fullname, nickname=nickname)
    session.add(user)
    session.commit()
    session.close()
    return get_user_by_nickname(nickname)


def update(user: TelegramUser) -> Optional[UserModel]:
    """
    Update user in database by Telegram nickname

    :param user: User instance
    """

    session = Session()
    ruser = None
    db_user = session.query(User).filter(User.nickname == user.username).first()
    if db_user:
        db_user.tgid = user.id
        db_user.name = user.first_name
        db_user.fullname = user.full_name
        ruser = UserModel(db_user)
        session.commit()
    session.close()
    return ruser
