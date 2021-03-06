from entity_model.base import Base
from sqlalchemy import Column, ForeignKey, Integer, DateTime, String, BOOLEAN
from sqlalchemy.orm import relationship


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key = True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    status = Column(BOOLEAN, nullable= False)
    #one to one
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref="account")

    def __init__(self, username, password, status, user):
        self.username = username
        self.password = password
        self.user = user
        self.status = status
