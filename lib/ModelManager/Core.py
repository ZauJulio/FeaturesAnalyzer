import os
import sys
import pickle

sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../../")

import numpy as np
import pandas as pd

from lib.data_manager.data import Data
from lib.util.path import bar, index_path

from lib.ModelManager.Models import Models
from lib.ModelManager.Metrics import Metrics
from lib.ModelManager.Index import Index
from lib.ModelManager.docs import ModelDocs


class ModelManager(Data):
    def __init__(self, db: str = "sqlite",
                 dbAcessParms: dict = {"path": index_path + bar + "models.db"}, **kwargs):
        """ Model manager with indexer

        Parameters
        ----------
            typ: str()
                type of model, [rgs, som, mlp]

            tryLoad: bool()
                Attempt to load model from disk

            db: str(), default="sqlite"
                Must be one of the following modes = [sqlite, postgres]
                    direct    -> Connection in PostgreSQL server (faster and Secure)
                    sqlite    -> Save in local sqlite3 file (fast and a little less secure)

            dbAcessParms: dict()
                if type == "postgres":
                    dbname: str() the database name
                    database: str() the database name (only as keyword argument)
                    user: str() user name used to authenticate
                    password: str() password used to authenticate
                    host: str() database host address (defaults to UNIX socket if not provided)
                    port: str() connection port number (defaults to 5432 if not provided)

                if type == "sqlite":
                    path: str() of local file, default data/models/models.db
        """
        super().__init__(**kwargs)

        self.__index = Index(
            db=db,
            dbAcessParms=dbAcessParms
        )
        self.__pathModel = ""
        self.__modelClass = None

    def create(self, typ: str = None, tryLoad: bool = True, **kwargs):
        """Model creator

        Parameters
        ----------
            typ: str()
                type of model, [rgs, som, mlp]

            tryLoad: bool()
                Attempt to load model from disk

            ###  Complete docs in lib.ModelManager.docs  ####
        " """
        self.setTypeModel(typ)
        self.formatID(kwargs)  # Add model parameters to ID
        self.formatPathModel()  # Define the path for this model

        loaded = False
        if tryLoad:
            loaded = self.loadModel()

        if not loaded:
            self._trainModel(kwargs)
            self.__index.save()
            self._saveModel()

        return self.model

    def setTypeModel(self, typ: str):
        """ Set type model and models Class """
        self.__modelClass = Models[typ]()
        self.__index.typeModel = typ

    def updateMetrics(self, data: np.ndarray, metrics: dict = None) -> bool:
        """ Update metrics

        Parameters
        ----------
            data: np.ndarray
                Data used to collect model metrics.
            metrics: dict
                Dictionary for insertion into the database.
                If None: Uses the model's default metric collector.

        Returns
        -------
            bool:
                True if saved correctly.
                False if an error occurs.
        """
        if metrics is None:
            collector = Metrics[self.__index.typeModel](uuid=self.__index.id)

            metrics = collector.collect(
                model=self.model,
                data=data,
            )

        return self.__index.updateMetrics(metrics)

    def collectMetrics(self, data: np.ndarray) -> dict:
        """ Collect model metrics

        Parameters
        ----------
            data: np.ndarray
                Data used to collect model metrics.

        Returns
        -------
            dict with default metrics of model.
        """
        metrics = self.__index.getMetricsFromModel()

        if metrics.empty:
            collector = Metrics[self.__index.typeModel](uuid=self.__index.id)

            metrics = collector.collect(
                model=self.model,
                data=data,
            )
            self.__index.saveMetrics(metrics)

        return metrics

    def getModelParms(self, uuid: str, typeModel: str = None) -> dict:
        """ Return model parameters of any model

        Parameters
        ----------
            uuid: str
                Unique model identifier.
            typeModel: str, default None
                If None, searches the entire database.

        Returns
        -------
            dict with model parameters
        """
        return self.__index.getModelParms(uuid, typeModel)

    def getModelMetrics(self, uuid: str = None, typeModel: str = None) -> dict:
        """ Return model parameters of any model

        Parameters
        ----------
            uuid: str
                Unique model identifier.
            typeModel: str, default None
                If None, searches the entire database.

        Returns
        -------
            dict with model parameters
        """
        return self.__index.getMetricsFromModel(uuid, typeModel)

    def getCollectedMetricsFromModel(self, typeModel: str = None) -> pd.DataFrame:
        """ Returns all metrics for a model type

        Parameters
        ----------
            typeModel: str, default None
                Type of model. If None, searches
                the entire database.

        Returns
        -------
            dict with all model parameters
        """
        return self.__index.getTableMetrics(typeModel)

    def getModel(self):
        """ Return model """
        return self.model

    def getTypeModel(self) -> str:
        """ Return type model """
        return self.__index.typeModel

    def getID(self) -> str:
        """ Return ID of model """
        return self.__index.id

    def getParms(self) -> list:
        """ Get all parms from model """
        return [self.__index.dataParms, self.__index.modelParms, self.__index.typeModel]

    def formatID(self, parms: dict) -> None:
        """ Insert the model parameters in the identifier """
        self.__index.dataParms = self.getDataID()
        self.__index.modelParms = self.__modelClass.formatParms(parms)
        self.__index.formatID()
        # Quando finaliza o grid search converta para list em Data
        drops = self.__index.dataParms["drops"]
        drops = drops[4:-1].replace('(', '').replace(')', '').split(',')
        self.__index.dataParms["drops"] = '{' + \
            str(drops)[1:-1].replace("'", '"')+'}'
        #
        self.__index.updateIndexesWithUUID()

    def formatPathModel(self, uuid: str = None) -> None:
        """ Configure the path for the model """
        self.__pathModel = self.__modelClass.formatPath(
            (self.__index.id if uuid is None else uuid), self._day)

    def _trainModel(self, parms: dict) -> None:
        """Initializes and trains the model based on
        specifications"""
        self.model = self.__modelClass.train(self.df, parms)

    def loadModel(self) -> bool:
        """ Load model from file """

        def readObject(path):
            print(path)
            return pickle.load(open(path, "rb"))

        if os.path.isfile(self.__pathModel):
            if len(self.parms.keys()) > 0:
                _file = readObject(self.__pathModel)
                self.model, self.df = _file.model, _file.df
            else:
                self.model = readObject(self.__pathModel)
            return True
        else:
            return False

    def _saveModel(self) -> None:
        """ Save model """

        def saveObject(object, path):
            pickle.dump(object, open(path, "wb"))

        if len(self.parms.keys()) > 0:
            saveObject(self, self.__pathModel)
        else:
            saveObject(self.model, self.__pathModel)

        """ Temporarily removed to speed up the Cross Validation experiment """
        # if self.__index.typeModel == "som":
        #     cluster_dir = clusters_som + self._day + bar + self.__index.id + bar
        #     if not os.path.isdir(cluster_dir):
        #         os.makedirs(cluster_dir)
        #     self.model.saveClusters(self.df.T, path=cluster_dir)


ModelManager.create.__doc__ = ModelDocs
