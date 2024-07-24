from typing import Optional, List
from sqlalchemy import asc

from ..db import TgUser, Session
from ..model import User as UserModel


def get_id(user_id: int) -> Optional[UserModel]:
    """
    Get user by id

    :param user_id: Telegram user id

    :return: TgUser instance
    """

    session = Session()
    ruser = None
    user = session.query(TgUser).filter(TgUser.id == user_id).first()
    if user:
        ruser = UserModel(user)
    session.close()
    return ruser

def nickname(nick: str) -> Optional[UserModel]:
    """
    Get user by nickname

    :param nick: Telegram nickname

    :return: TgUser instance
    """

    session = Session()
    ruser = None
    user = session.query(TgUser).filter(TgUser.nickname == nick).first()
    if user:
        ruser = UserModel(user)
    session.close()
    return ruser


def users(offset: Optional[int] = None, limit: Optional[int] = None) -> List[UserModel]:
    """
    Get all users from the database

    :return: list of TgUser instances
    """

    session = Session()
    fusers = (session.query(TgUser)
              .order_by(asc(TgUser.id))
              .offset(offset)
              .limit(limit)
              .all())
    rusers = [UserModel(user) for user in fusers]
    session.close()
    return rusers


def count() -> int:
    """
    Get the number of users in the database

    :return: number of users
    """

    session = Session()
    counter = session.query(TgUser).count()
    session.close()
    return counter
