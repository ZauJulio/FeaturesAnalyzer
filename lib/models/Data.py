from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ARRAY
from sqlalchemy.orm import relationship

from lib.models import Base, Model

from lib.models.SOM import SOM
from lib.models.RGS import RGS
from lib.models.SOM_METRICS import SOMMetrics
# from lib.models.MLP import MLP
# from lib.models.MLP_METRICS import MLP_METRICS
# from lib.models.RGS_METRICS import RGS_METRICS


class Data(Base, Model):
    __tablename__ = 'data'

    uuid = Column(String(length=36), primary_key=True, nullable=False)
    day = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    field = Column(String(length=2), nullable=False)
    ffill = Column(Boolean, nullable=False)
    bfill = Column(Boolean, nullable=False)
    seeds = Column(ARRAY(Integer), nullable=False)
    drops = Column(ARRAY(String), nullable=False)
    transformations = Column(ARRAY(String), nullable=False)
    type = Column(String(length=3), nullable=False)

    som_models = relationship(SOM, backref="som_models")
    rgs_models = relationship(RGS, backref="rgs_models")
    som_metrics_models = relationship(SOMMetrics, backref="som_metrics_models")

    @classmethod
    def findByUUID(cls, session, uuid):
        return session.query(cls).filter_by(uuid=uuid).all()

    def __repr__(self):
        return f"""
            uuid : {self.uuid},
            day : {self.day},
            start_date : {self.start_date},
            end_date : {self.end_date},
            start_time : {self.start_time},
            end_time : {self.end_time},
            field : {self.field},
            ffill : {self.ffill},
            bfill : {self.bfill},
            seeds : {self.seeds},
            drops : {self.drops},
            transformations : {self.transformations},
            type : {self.type},
        """
