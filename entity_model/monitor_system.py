from traitlets import Int
from entity_model.base import Base
from sqlalchemy import Column, ForeignKey, Integer, Date, Float
from entity_model.ml_metric import ML_metric
from sqlalchemy.orm import relationship


class Monitor_system(Base):
    __tablename__ = 'monitor_system'

    id = Column(Integer, primary_key = True)
    date = Column(Date, nullable=False)
    statistic = Column(Float, nullable=False)
    
    #many to one
    ml_metric_id = Column(Integer, ForeignKey('ml_metric.id'), nullable=False)
    ml_metric = relationship('ML_metric')

    def __init__(self, id, date, statistic, ml_metric_id) -> None:
        self.id = id
        self.date = date
        self.statistic = statistic
        self.ml_metric_id=ml_metric_id