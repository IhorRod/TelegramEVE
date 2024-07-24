from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import enum

engine = create_engine('sqlite:///eve.db', echo=False)
Base = declarative_base()


class TgUser(Base):
    __tablename__ = 'tgusers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tgid = Column(Integer, unique=True, nullable=True)
    name = Column(String, nullable=True)
    fullname = Column(String, nullable=True)
    nickname = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<TgUser(id={self.id}, tgid={self.tgid}, name={self.name}, fullname={self.fullname}, nickname={self.nickname})>"


class SubscriptionTypes(enum.Enum):
    MAIL = 1
    NOTIFICATIONS = 2
    DUMMY = 3


class SubscriptionDelivers(enum.Enum):
    LOG = 1
    TG = 2


class Subscribes(Base):
    __tablename__ = 'subscribes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sub_deliver = Column(Enum(SubscriptionDelivers), nullable=False)
    sub_id = Column(Integer, nullable=True)
    sub_type = Column(Enum(SubscriptionTypes), nullable=False)
    filter = Column(String, nullable=True)  # JSON string


class SubscriptionHistory(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, nullable=False)
    item_type = Column(Enum(SubscriptionTypes), nullable=False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
