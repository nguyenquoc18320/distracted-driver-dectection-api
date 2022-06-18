from sqlalchemy import Column, ForeignKey, String, Date, Integer, Boolean
from entity_model.base import Base
from sqlalchemy.orm import relationship
from entity_model.role import Role

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    gender = Column(Boolean)
    birthday = Column(Date)
    phone = Column(String(20))
    driver_license = Column(String(50),  nullable=False, unique =True)
    #one to many 
    # distractions = relationship("Distraction")

    #many to one
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship('Role', backref='role')


    def __init__(self, name, gender, birthday, phone, driver_license, role ) -> None:
        self.name = name
        self.gender = gender
        self.birthday = birthday
        self.phone = phone
        self.driver_license = driver_license
        self.role = role

    