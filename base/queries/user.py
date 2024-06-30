from typing import Optional, List
from sqlalchemy import desc, asc

from base.db import User, Session
from base.model import User as UserModel


def nickname(nick: str) -> Optional[UserModel]:
    """
    Get user by nickname

    :param nick: Telegram nickname

    :return: User instance
    """

    session = Session()
    ruser = None
    user = session.query(User).filter(User.nickname == nick).first()
    if user:
        ruser = UserModel(user)
    session.close()
    return ruser


def users(offset: Optional[int] = None, limit: Optional[int] = None) -> List[UserModel]:
    """
    Get all users from the database

    :return: list of User instances
    """

    session = Session()
    users = (session.query(User)
             .order_by(asc(User.id))
             .offset(offset)
             .limit(limit)
             .all())
    rusers = [UserModel(user) for user in users]
    session.close()
    return rusers


def count() -> int:
    """
    Get the number of users in the database

    :return: number of users
    """

    session = Session()
    count = session.query(User).count()
    session.close()
    return count
