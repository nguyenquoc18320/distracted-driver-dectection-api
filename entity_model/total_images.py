from sqlalchemy import Column, ForeignKey, String, Integer, Date
from entity_model.base import Base
from sqlalchemy.orm import relationship

class Total_images(Base):
    __tablename__ = 'total_images'

    id = Column(Integer, primary_key = True)
    date = Column(Date, nullable=False)
    num_images = Column(Integer, nullable=False)

    #many to one
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref="total_images")

    def __init__(self, id, date, num_images, user) -> None:
        self.id = id
        self.date = date
        self.num_images = num_images
        self.user = user        