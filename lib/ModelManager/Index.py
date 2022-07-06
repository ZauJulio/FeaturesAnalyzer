import uuid

import pandas as pd
from lib.Adapter import Sqlite3, Postgres
from lib.ModelManager.errors import InvalidDBOptions
from lib.util.path import bar, index_path


class Index(object):

    def __init__(self, dataParms: dict = {}, modelParms: dict = {}, typeModel: str = "",
                 db: str = "sqlite", dbAcessParms: dict = {"path": index_path+bar+"models.db"}):
        """ Index management

        Parameters
        ----------
            dataParms: dict
                parameters of data
            modelParms: dict
                parameters of model
            typeModel: str()
                type of model, [rgs, som, mlp]
        """
        self.id = ""
        self.typeModel = typeModel
        self.dataParms = dataParms
        self.modelParms = modelParms
        self.__dbAcessMode = db
        self.__dbAcessParms = dbAcessParms

        if len(self.dataParms.keys()) != 0 and len(self.modelParms.keys()) != 0:
            self.formatID()

    @staticmethod
    def __getDBAdapter(db, dbAcessParms):
        """  """
        if db.lower() == "sqlite":
            db = Sqlite3(dbAcessParms)
        elif db.lower() == "postgres":
            db = Postgres(dbAcessParms)
        else:
            raise InvalidDBOptions

        return db

    def formatID(self):
        self.id = self.dictJoin(self.dataParms, self.modelParms)
        self.id = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(self.id)))

    def updateIndexesWithUUID(self):
        """  """
        self.dataParms = self.dictJoin({'uuid': self.id}, self.dataParms)
        self.modelParms = self.dictJoin({'uuid': self.id}, self.modelParms)

    @staticmethod
    def dictJoin(x: dict, y: dict) -> dict:
        """ Join dictionaries """
        return {**x, **y}

    @staticmethod
    def getUUIDFromParms(dataParms: dict, modelParms: dict) -> str:
        """ Return UUID from parms

        Parameters
        ----------
            dataParms: dict
                parameters of data
            modelParms: dict
                parameters of model

        Returns
        -------
            str()
        """
        return Index(dataParms, modelParms).id

    def getModelParms(self, uuid: str, typeModel: str = None):
        """  """
        return self.__getDBAdapter(
            self.__dbAcessMode,
            self.__dbAcessParms
        ).getModelParms(uuid, typeModel)

    def getMetricsFromModel(self, typeModel: str = None, uuid: str = None) -> pd.DataFrame:
        """  """
        if typeModel is None:
            typeModel = self.typeModel

        if uuid is None:
            uuid = self.id

        return self.__getDBAdapter(
            self.__dbAcessMode,
            self.__dbAcessParms
        ).getMetrics(uuid, typeModel)

    def getTableMetrics(self, typeModel: str = None) -> pd.DataFrame:
        """  """
        if typeModel is None:
            typeModel = self.typeModel

        return self.__getDBAdapter(
            self.__dbAcessMode,
            self.__dbAcessParms
        ).getTable(typeModel, metrics=True)

    def getTableOfModel(self) -> pd.DataFrame:
        """  """
        return self.__getDBAdapter(
            self.__dbAcessMode,
            self.__dbAcessParms
        ).getTable(self.typeModel)

    def getTableOfDataParms(self) -> pd.DataFrame:
        """  """
        return self.__getDBAdapter(
            self.__dbAcessMode,
            self.__dbAcessParms
        ).getTable("data")

    def save(self):
        """  """
        self.__getDBAdapter(
            self.__dbAcessMode,
            self.__dbAcessParms
        ).insertModelParms(
            self.dataParms,
            self.modelParms,
            self.typeModel
        )

    def saveMetrics(self, metrics) -> bool:
        """  """
        return self.__getDBAdapter(
            self.__dbAcessMode,
            self.__dbAcessParms
        ).insertModelMetrics(
            metrics,
            self.typeModel
        )

    def updateMetrics(self, metrics) -> bool:
        """  """
        return self.__getDBAdapter(
            self.__dbAcessMode,
            self.__dbAcessParms
        ).updateModelMetrics(
            metrics,
            self.typeModel
        )
