from abc import ABC, abstractmethod
import numpy as np
import copy

import pandas as pd
from contextlib import closing


class Table(ABC):
    __create = """  """
    __name = ""

    @abstractmethod
    def tableExist(self, tableName: str) -> bool:
        """  """
        pass

    @abstractmethod
    def showException(self, err):
        """  """
        pass

    def _setTable(self, tableName: str):
        """ Set instance of table """
        self.checkTable(tableName)
        self.__create = __tables__[tableName]
        self.__name = tableName

    def _create(self):
        """ Create table """
        if self.tableExist(self.__name):
            return

        with closing(self.conn.cursor()) as cursor:
            try:
                cursor.execute(self.__create)
                self.conn.commit()
            except self.error as err:
                self.showException(err)

    @staticmethod
    def array2string(array) -> str:
        """ Convert an array to a str like:
            np.ndarray([1,2,3]) -> '1, 2, 3'
        """
        return np.array2string(
            array,
            separator=',',
            formatter={'float_kind': lambda x: "%.6f" % x}
        )[1:-1].replace('\n', '')

    def __formatInsert(self, data: dict) -> str:
        """ Format insert instruction with data
        
        Parameters
        ----------
            data: dict
                dict with all metrics of model to
                format insert instruction.
        """
        formated = "INSERT INTO %s(%s) VALUES(%s);"
        columns = str(list(data))[1:-1].replace("'", '')
        values = []

        for key, value in zip(data.keys(), data.values()):
            typ = type(value)
            if (typ is list) or (typ is np.ndarray) or (typ is pd.Series):
                values.append(('{'+self.array2string(value)+'}'))
            else:
                values.append(value)

        formated = formated % (self.__name, columns, str(values)[1:-1])
        return formated

    def __formatUpdate(self, data: dict) -> str:
        """ Format update instruction with data
        
        Parameters
        ----------
            data: dict
                dict with all metrics of model to
                format update instruction.
        """
        data = copy.deepcopy(data)
        uuid = data.pop('uuid')
        values = []

        for key, value in zip(data.keys(), data.values()):
            typ = type(value)
            if (typ is list) or (typ is np.ndarray) or (typ is pd.Series):
                values.append(key+" = '{"+self.array2string(value)+"}'")
            else:
                values.append(f"{key} = '{value}'")

        return ("UPDATE %s SET %s WHERE UUID in ('%s');" % (
            self.__name, str(values)[1:-1], uuid
        )).replace('"', '')

    def _update(self, data: dict) -> bool:
        """ Insert new model in index database

        Parameters
        ----------
            data: dict
                dict with all metrics of model.
        
        Returns
        -------
            Bool with the status of the operation.
        """
        exitCode = False

        if self._getByIndex(data["uuid"]).empty:
            return False

        with closing(self.conn.cursor()) as cursor:
            try:
                cursor.execute(self.__formatUpdate(data))
                self.conn.commit()
                exitCode = True
            except self.error as err:
                self.showException(err)
                exitCode = False
            finally:
                return exitCode

    def _insert(self, data: dict) -> bool:
        """ Insert data into the table

        Parameters
        ----------
            data: dict()
                dict with all metrics of model

        Returns
        -------
            Bool with the status of the operation.
        """
        exitCode = False

        if not self._getByIndex(data["uuid"]).empty:
            return False

        with closing(self.conn.cursor()) as cursor:
            try:
                cursor.execute(self.__formatInsert(data))
                self.conn.commit()
                exitCode = True
            except self.error as err:
                self.showException(err)
                exitCode = False
            finally:
                return exitCode

    def _getByIndex(self, index: str) -> pd.DataFrame:
        """ Returns the index data from table

        Parameters
        ----------
            index: str()
                uuid of the model

        Returns
        -------
            DataFrame with parms of model, if DataFrame.empty,
            model not found.
        """
        df = pd.DataFrame()

        with closing(self.conn.cursor()) as cursor:
            try:
                cursor.execute(
                    f"SELECT {self.__name}.* FROM {self.__name} WHERE uuid='{index}';")

                df = pd.DataFrame(
                    cursor.fetchall(),
                    columns=self.getHeader(cursor)
                ).drop(columns=["uuid"])
            except self.error as err:
                df = pd.DataFrame()
                self.showException(err)
            finally:
                return df

    def _getTable(self) -> pd.DataFrame:
        """ Get all lines from table

        Parameters
        ----------
            tableName: str()  Default = ""
                model present in self.tables.
                If None, will search all tables.

        Returns
        -------
            pd.DataFrame()
        """
        df = pd.DataFrame()

        if not self.tableExist(self.__name):
            self.createTable(self.__name)

        with closing(self.conn.cursor()) as cursor:
            try:
                cursor.execute(f"SELECT * FROM {self.__name};")
                df = pd.DataFrame(
                    cursor.fetchall(),
                    columns=self.getHeader(cursor)
                )
            except self.error as err:
                df = pd.DataFrame()
                self.showException(err)
            finally:
                return df

    def checkTable(self, tableName: str):
        """ Check if table name is valid

        Parameters
        ----------
            tableName: str()  Default = ""
                model present in self.tables.
                If not present, raise ValueError: InvalidTableName
        """
        if not (tableName in __tables__):
            raise ValueError(
                "InvalidTableName: Table name not valid %s" % tableName)

    @staticmethod
    def getHeader(cursor):
        """ Return header from cursor """
        return [desc[0] for desc in cursor.description]


"""
dict.key   = 3-character model identifier
dict.value = Generic SQL statement for creating the table
"""
__tables__ = {
    "data": """
        CREATE TABLE Data(
            uuid                    CHAR(36)  PRIMARY KEY       NOT NULL,
            day                     TEXT                        NOT NULL,
            start_date              TEXT                        NOT NULL,
            end_date                TEXT                        NOT NULL,
            start_time              TEXT                        NOT NULL,
            end_time                TEXT                        NOT NULL,
            field                   CHAR(2)                     NOT NULL,
            ffill                   BOOLEAN                     NOT NULL,
            bfill                   BOOLEAN                     NOT NULL,
            seeds                   INT[]                       NOT NULL,
            drops                   TEXT[]                      NOT NULL,
            transformations         TEXT[]                      NOT NULL,
            type                    CHAR(3)                     NOT NULL
        );""",
    "som": """
            CREATE TABLE Som(
            uuid                    CHAR(36)  PRIMARY KEY       NOT NULL,
            x                       INT                         NOT NULL,
            y                       INT                         NOT NULL,
            inputlen                INT                         NOT NULL,
            iterations              INT                         NOT NULL,
            sigma                   REAL                        NOT NULL,
            learningrate            REAL                        NOT NULL,
            neighborhoodfunction    TEXT                        NOT NULL,
            topology                TEXT                        NOT NULL,
            activationdistance      TEXT                        NOT NULL,
            weightsinit             TEXT                        NOT NULL,
            randomorder             TEXT                        NOT NULL,
            transpose               BOOLEAN                     NOT NULL,
            CONSTRAINT fk_SomData FOREIGN KEY (UUID) REFERENCES DATA (UUID)
        );""",
    "rgs": """
        CREATE TABLE Rgs(
            uuid                    CHAR(36)  PRIMARY KEY       NOT NULL,
            deg                     INT                         NOT NULL,
            type                    TEXT                        NOT NULL,
            CONSTRAINT fk_RgsData FOREIGN KEY (UUID) REFERENCES DATA (UUID)
        );""",
    "som_metrics": """
        CREATE TABLE som_metrics (
            uuid                    CHAR(36) PRIMARY KEY UNIQUE NOT NULL,
            samples                 SMALLINT[]           NOT NULL,
            dotproductmean          FLOAT(16)[]          NOT NULL,
            dotproductvar           FLOAT(16)[]          NOT NULL,
            dotproductstd           FLOAT(16)[]          NOT NULL,
            variancemean            FLOAT(16)[]          NOT NULL,
            clustermean             FLOAT(16)[]          NOT NULL,
            stdmean                 FLOAT(16)[]          NOT NULL,
            qemean                  FLOAT(16)[]          NOT NULL,
            rmsemean                FLOAT(16)[]          NOT NULL,
            maemean                 FLOAT(16)[]          NOT NULL,
            silhouettescore         FLOAT(16)            NOT NULL,
            daviesbouldinscore      FLOAT(16)            NOT NULL,
            calinskiharabaszscore   FLOAT(16)            NOT NULL,
            CONSTRAINT fk_SomMetricsData FOREIGN KEY (UUID) REFERENCES DATA (UUID)
        );"""
}
