from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, ARRAY, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from lib.models import Base, Model


class SOMMetrics(Base, Model):
    __tablename__ = 'som_metrics'

    uuid = Column(String(length=36), ForeignKey(
        'Data.uuid'), primary_key=True, nullable=False)
    samples = Column(ARRAY(SmallInteger), nullable=False)
    dotproductmean = Column(ARRAY(Float(precision=16)), nullable=False)
    dotproductvar = Column(ARRAY(Float(precision=16)), nullable=False)
    dotproductstd = Column(ARRAY(Float(precision=16)), nullable=False)
    variancemean = Column(ARRAY(Float(precision=16)), nullable=False)
    clustermean = Column(ARRAY(Float(precision=16)), nullable=False)
    stdmean = Column(ARRAY(Float(precision=16)), nullable=False)
    qemean = Column(ARRAY(Float(precision=16)), nullable=False)
    rmsemean = Column(ARRAY(Float(precision=16)), nullable=False)
    maemean = Column(ARRAY(Float(precision=16)), nullable=False)
    silhouettescore = Column(Float(precision=16), nullable=False)
    daviesbouldinscore = Column(Float(precision=16), nullable=False)
    calinskiharabaszscore = Column(Float(precision=16), nullable=False)

    data = relationship('Data')

    def __repr__(self):
        return f"""
            uuid : {self.uuid},
            samples : {self.samples},
            dotproductmean : {self.dotproductmean},
            dotproductvar : {self.dotproductvar},
            dotproductstd : {self.dotproductstd},
            variancemean : {self.variancemean},
            clustermean : {self.clustermean},
            stdmean : {self.stdmean},
            qemean : {self.qemean},
            rmsemean : {self.rmsemean},
            maemean : {self.maemean},
            silhouettescore : {self.silhouettescore},
            daviesbouldinscore : {self.daviesbouldinscore},
            calinskiharabaszscore : {self.calinskiharabaszscore},
        """
