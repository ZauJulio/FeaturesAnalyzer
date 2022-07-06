from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from lib.models import Base, Model


class SOM(Base, Model):
    __tablename__ = 'som'

    uuid = Column(String(length=36), ForeignKey(
        'data.uuid'), primary_key=True, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    inputlen = Column(Integer, nullable=False)
    iterations = Column(Integer, nullable=False)
    sigma = Column(Float(precision=4), nullable=False)
    learningrate = Column(Float(precision=4), nullable=False)
    neighborhoodfunction = Column(String, nullable=False)
    topology = Column(String, nullable=False)
    activationdistance = Column(String, nullable=False)
    weightsinit = Column(String, nullable=False)
    randomorder = Column(String, nullable=False)
    transpose = Column(Boolean, nullable=False)

    data = relationship('Data')

    def __repr__(self):
        return f"""
            uuid : {self.uuid},
            x : {self.x},
            y : {self.y},
            inputlen : {self.inputlen},
            iterations : {self.iterations},
            sigma : {self.sigma},
            learningrate : {self.learningrate},
            neighborhoodfunction : {self.neighborhoodfunction},
            topology : {self.topology},
            activationdistance : {self.activationdistance},
            weightsinit : {self.weightsinit},
            randomorder : {self.randomorder},
            transpose : {self.transpose},
        """
