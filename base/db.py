from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///eve.db', echo=False)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tgid = Column(Integer, unique=True, nullable=True)
    name = Column(String, nullable=True)
    fullname = Column(String, nullable=True)
    nickname = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<User(id={self.id}, tgid={self.tgid}, name={self.name}, fullname={self.fullname}, nickname={self.nickname})>"


class CharacterTargets(Enum):
    MAIL = 1
    NOTIFICATIONS = 2


class CharacterSubscribers(Base):
    __tablename__ = 'notification_subs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    target = Column(Enum(CharacterTargets), nullable=False)
    char_id = Column(Integer, nullable=False)
    filter = Column(String, nullable=True)

    def __repr__(self):
        return f"<CharacterSubscribers(id={self.id}, user_id={self.user_id}, target={self.target}, char_id={self.char_id}, filter={self.filter})>"


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
