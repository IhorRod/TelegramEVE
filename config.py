import os


class Config:
    """
    This class is used to store the configuration of the bot.

    Attributes:
    TOKEN: str
        The token of the bot.

    SEAT_URL: str
        The URL of the SEAT instance.

    SEAT_TOKEN: str
        The token of the SEAT instance API (generated in the SEAT instance).

    BOOTSTRAP_USER: str
        The user that will be used to bootstrap the bot in the Telegram.

    """
    TOKEN = None
    SEAT_URL = None
    SEAT_TOKEN = None
    BOOTSTRAP_USER = None

    def __init__(self):
        self.TOKEN = os.environ.get('TOKEN')

        if not self.TOKEN:
            raise ValueError("TOKEN is not set")

        self.SEAT_URL = os.environ.get('SEAT_URL')

        if not self.SEAT_URL:
            raise ValueError("SEAT_URL is not set")

        self.SEAT_TOKEN = os.environ.get('SEAT_TOKEN')

        if not self.SEAT_TOKEN:
            raise ValueError("SEAT_TOKEN is not set")

        self.BOOTSTRAP_USER = os.environ.get('BOOTSTRAP_USER')

        if not self.BOOTSTRAP_USER:
            raise ValueError("BOOTSTRAP_USER is not set")