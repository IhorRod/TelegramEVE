from typing import Optional, Tuple

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
