from traitlets import default
from entity_model.base import Base
from sqlalchemy import Column, ForeignKey, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relationship


class Distraction(Base):
    __tablename__ = 'distraction'
    id = Column(Integer, primary_key = True)
    time = Column(DateTime)
    category = Column(String(50), nullable=False)
    image_path = Column(String(500), nullable=False, unique=True)
    no_person = Column(Boolean, default=False)
    #many to one
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref="distraction")

    def __init__(self, time, category, image_path, user, no_person=False):
        self.time = time
        self.category = category
        self.image_path = image_path
        self.user = user
        self.no_person = no_person
