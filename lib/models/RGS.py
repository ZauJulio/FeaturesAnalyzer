from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from lib.models import Base, Model


class RGS(Base, Model):
    __tablename__ = 'rgs'

    uuid = Column(String(length=36), ForeignKey('data.uuid'), primary_key=True, nullable=False)
    deg = Column(Integer, nullable=False)
    type = Column(String, nullable=False)

    data = relationship('Data')

    def __repr__(self):
        return f"""
            uuid : {self.uuid},
            deg : {self.deg},
            type : {self.type},
        """
