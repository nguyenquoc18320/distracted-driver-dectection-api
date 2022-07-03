from sqlalchemy import Column, String, Integer
from entity_model.base import Base

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key = True)
    name = Column(String(10), nullable=False, unique=True)

    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name        