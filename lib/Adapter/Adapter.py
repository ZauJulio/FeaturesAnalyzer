from pandas import DataFrame
from abc import ABC, abstractmethod
from .Table import Table, __tables__


class Adapter(Table, ABC):
    tables = __tables__

    def __init__(self, kwargs):
        """ Adapter SQL connection

        Parameters
        ----------
            dbname: str() the database name
            database: str() the database name (only as keyword argument)
            user: str() user name used to authenticate
            password: str() password used to authenticate
            host: str() database host address (defaults to UNIX socket if not provided)
            port: str() connection port number (defaults to 5432 if not provided)

            or

            path: str() path database file
        """
        super().__init__()

        self.conn = self.connect(**kwargs)

        for table in self.tables:
            self.checkTable(table)
            if not self.tableExist(table):
                self._setTable(table)
                self._create()

    @abstractmethod
    def connect(self, args):
        """  """
        pass

    @property
    @abstractmethod
    def error(self):
        pass

    @abstractmethod
    def showException(self, err):
        """  """
        pass

    @abstractmethod
    def tableExist(self, tableName: str) -> bool:
        """  """
        pass
    
    def getTable(self, table:str, metrics:bool=False) -> DataFrame:
        """ Return table
        
        Parameters
        ----------
            tableName: str()
                [data, som, rgs, mlp]
            metrics: bool() default False
                return metrics from table

        Returns
        -------
            Complete table with all values
        """
        if (metrics and (table != "data")):        
            self._setTable(table+"_metrics")
        else:
            self._setTable(table)

        return self._getTable()

    def insertModelParms(self, DataParms: dict, ModelParms: dict, TypeModel: str) -> bool:
        """ Insert new model in index database

        Parameters
        ----------
            DataParms: dict()
                dict with all data parameters
            ModelParms: dict()
                dict with all model parameters
            TypeModel: str()
                type of model, the table must be created and listed in
                self.tables.

        Returns
        -------
            bool():
                if True  -> model is inserted
                if False -> the model already exists in DB
        """
        self._setTable("data")
        self._insert(DataParms)

        self._setTable(TypeModel)
        self._insert(ModelParms)

    def updateModelMetrics(self, Metrics: dict, TypeModel: str) -> bool:
        """ Insert new model in index database

        Parameters
        ----------
            Metrics: dict()
                dict with all metrics of model
            TypeModel: str()
                type of model, the table must be created and listed in
                self.tables.

        Returns
        -------
            bool():
                if True  -> model is updated
                if False -> model not found
        """
        self._setTable(TypeModel+"_metrics")
        self._update(Metrics)

    def insertModelsMetrics(self, Metrics: dict, TypeModel: str) -> bool:
        """ Insert new model in index database

        Parameters
        ----------
            Metrics: dict()
                dict with all metrics of model
            TypeModel: str()
                type of model, the table must be created and listed in
                self.tables.

        Returns
        -------
            bool():
                if True  -> model is inserted
                if False -> the model already exists in DB
        """
        self._setTable(TypeModel+"_metrics")
        self._insert(Metrics)

    def getDataParms(self, index: str) -> DataFrame:
        """ Get data parameters

        Parameters
        ----------
            index: str()
                uuid of the model

        Returns
        -------
            DataFrame with parms of model, if DataFrame.empty,
            model not found.
        """
        self._setTable("data")
        return self._getByIndex(index)

    def getModelParms(self, index: str, typ: str = None) -> DataFrame:
        """ Get model parms from index

        Parameters
        ----------
            index: str()
                uuid of the model
            typ: str()  Default = ""
                model present in self.tables.
                If None, will search all tables.

        Returns
        -------
            DataFrame with parms of model, if DataFrame.empty,
            model not found.
        """

        if not(typ is None):
            self._setTable(typ)
            return self._getByIndex(index)

        for typ in list(self.tables.keys())[1:]:
            self._setTable(typ)
            df = self._getByIndex(index)
            if not df.empty:
                return df

        print("No reference to the UUID found in any model table.")
        return DataFrame()

    def getMetrics(self, index: str, typ: str = "") -> DataFrame:
        """ Get model parms from index

        Parameters
        ----------
            index: str()
                uuid of the model
            typ: str()  Default = ""
                model present in self.tables.
                If "", will search all tables.

        Returns
        -------
            DataFrame with parms of model, if DataFrame.empty,
            model not found.
        """
        if typ != "":
            self._setTable(typ+"_metrics")
            return self._getByIndex(index)

        for typ in list(self.tables.keys())[3:]:
            self._setTable(typ+"_metrics")
            df = self._getByIndex(index)
            if not df.empty:
                return df

        print("No reference to the UUID found in any model table.")
        return DataFrame()

    def getParms(self, index: str) -> DataFrame:
        """ Get a DataFrame with all data and model parameters

        Parameters
        ----------
            index: str()
                uuid of the model

        Returns
        -------
            DataFrame with parms of model, if DataFrame.empty,
            model not found.
        """
        return self.getDataParms(index).join(
            self.getModelParms(index),
            how="left"
        )
