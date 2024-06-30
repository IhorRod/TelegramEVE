from base.db import User as DBUSer, CharacterSubscribers as DBCharacterSubscribers


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


class CharacterSubscribers:
    """
    Character subscribers model
    """

    def __init__(self, subscriber: DBCharacterSubscribers):
        self.id = subscriber.id
        self.user_id = subscriber.user_id
        self.target = subscriber.target
        self.char_id = subscriber.char_id
        self.filter = subscriber.filter
