from base.db import User as DBUSer


class User:
    """
    User model
    """

    def __init__(self, user: DBUSer):
        self.id = user.id
        self.tgid = user.tgid
        self.name = user.name
        self.fullname = user.fullname
        self.nickname = user.nickname
