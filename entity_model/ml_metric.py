from enum import unique
from matplotlib.collections import Collection
from entity_model.base import Base
from sqlalchemy import Column, Integer, String

class ML_metric(Base):
    __tablename__ = 'ml_metric'

    id = Column(Integer, primary_key = True)
    name = Column(String(500), nullable=False, unique=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name