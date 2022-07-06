from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models import Base
from lib.models.Data import Data
from lib.models.SOM import SOM
from lib.models.RGS import RGS
from lib.models.SOM_METRICS import SOMMetrics
# from lib.models.RGS_METRICS import BaseRGS_METRICS
# from lib.models.MLP import BaseMLP
# from lib.models.MLP_MET import BaseMLP_MET


SQLITE = 'sqlite'


class DB:

    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    def __init__(self, dbtype, username='', password='', dbname=''):
        """  """
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.__engine = create_engine(engine_url)
        else:
            raise ValueError(f"Invalid dbtype {dbtype}")

        self.__sessionMaker = sessionmaker(bind=self.__engine)
        self.__session = self.__sessionMaker()

    def createTables(self):
        """  """
        Base.metadata.create_all(self.__engine)

    def create(self, model: Union[Data, SOM, RGS, SOMMetrics, list]):
        """  """
        if type(model) is list:
            self.__session.add_all(model)
        else:
            self.__session.add(model)

        self.__session.commit()

    def update(self, model: Union[Data, SOM, RGS, SOMMetrics]):
        self.__session.add(model)
        self.__session.commit()

    def delete(self, model: Union[Data, SOM, RGS, SOMMetrics]):
        """  """
        self.__session.delete(model)
        self.__session.commit()

    def execute_query(self, query=''):
        """  """
        if query == '':
            return
        
        with self.__engine.connect() as connection:
            connection.execute(query)
