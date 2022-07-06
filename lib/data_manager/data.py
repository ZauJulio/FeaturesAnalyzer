import os
import sys

sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../../")
sys.path.append("../lib")

import pandas as pd
import numpy as np
import sqlite3

from lib.util import timelib, numlib
from lib.data_manager.days import Days
from lib.data_manager.synthetic import synthetic
from lib.util.path import bar, tables_days, tables_synthetic
from lib.data_manager.transformations import Transform


class Data(Transform):
    def __init__(self, df=None, dir=tables_days, day='segunda',
                 dump='dump-2019-09-24-21-31-31', field='P1',
                 func=None, ffill:bool=True, bfill:bool=True,
                 transform=None, synthetic:bool=False):
        """ Data Manager

        Parameters
        ----------
            df: pandas.core.frame.DataFrame
                When passing this parameter the reading is not done,
                but it is possible to use the module's methods, such
                as filter, drop and selector.
            dir: str()
                Path for tables directory or complete path for file.
                It is possible to go directly to a complete directory
                of a file as well
            day: str() | list()
                ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo']
                ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            dump: str()
                Dump used when generating the tables.
                Parameter used to complete the directory to the table folder
            field: str()
                'P1' 'P2' 'P3' 'Q1' 'Q2' 'Q3' 'FPA' 'FPB' 'FPC'
            ffill: bool()
                Fill the spaces with NaN of the DataFrame with the last valid value.
            transform: str()
                Check the Transform documentation for more information.
                [
                    "Normalize", "Standardize", "MinMax", "MaxAbs",
                    "Robust", "Binarizer", "Quantile", "Power"
                ]
        """
        super().__init__()
        self.droped = ""
        self.shuffles = []
        self._typeDf = "syn" if synthetic else "org"
        self._dump = dump
        self._func = func
        self.ffill_ = ffill
        self.bfill_ = bfill
        self._dir = None
        self.__file = None
        self.__setField(field)
        self.__setDir(dir)

        if type(df) == pd.core.frame.DataFrame:
            self.__setDay(day)
            self.df = df

        else:
            days = []
            if type(day) is not list:
                day = [day.lower()]
            if day[0] in timelib.weekdays:
                days = sorted(day, key=timelib.weekdays.index)
            if day[0] in timelib.weekdaysEN:
                days = sorted(day, key=timelib.weekdaysEN.index)
            if len(days) == 0:
                raise ValueError("Invalid day {}".format(day))

            dfs = []
            for day in days:
                self.__setDay(day)
                self.__setTable()
                dfs.append(self.__reader())
            
            self.df = pd.concat(dfs, axis=1, sort=True)

            if len(days) > 1:
                self._day = '_'.join(days)

        self.transformData(transform)

    def transformData(self, transform: str):
        """ Applies a valid transformation to the data

        Parameters
        ----------
            transform : str()
                Options = [
                    Normalize
                    Standardize
                    MinMax
                    MaxAbs
                    Robust
                    Binarizer
                    Quantile
                    Power
                ]
        """
        if transform in self.transformations.keys():
            self.transformations[transform.title()]()

    def filter(self, startTime=None, endTime=None, startDate=None, endDate=None,
               inplace=True):
        """ Update the DataFrame with all the selections

        Parameters
        ----------
            startTime : str
                Start time of day with the following format:
                    str(%H:%M): "13:50"
                To define the start of the time selection,
                do not pass this parameter.To not consider
                the minutes, just do not send them

            endTime : str
                End time of day with the following format:
                    str(%H:%M): "22:00"
                To define the end of the time selection,
                do not pass this parameter.To not consider
                the minutes, just do not send them

            startDate : str
                Selection start date with the following format:
                    str(%y-%m-%d): "2018-04-03"
                To define the start of the data selection,
                do not send this parameter.To select only the month,
                do not send the day in the string, to select the year,
                do not send the day or month in the string.

            endDate : str
                Selection end date with the following format:
                    str(%y-%m-%d): "2019-09-10"
                To define the end of the data selection,
                do not send this parameter.To select only the month,
                do not send the day in the string, to select the year,
                do not send the day or month in the string.

            inplace: bool
                If true change atribute df
        Notes
        -----
            If you do not want to define the start or end of the selection,
            do not send the desired time or date parameter.
            If you don't want to select anything while reading, don't send
            anything.
            If you want to make only the selection,send the DataFrame and
            the selection parameters.

        Return
        ------
            pandas.core.frame.DataFrame
        """
        if endDate != None:
            if endDate == self.df.columns[-1] or endDate > self.df.columns[-1]:
                endDate = None
        if endTime != None:
            if endTime == self.df.index[-1] or endTime >= self.df.index[-1]:
                endTime = None
        
        __df = self.df.loc[startTime:endTime, startDate:endDate]
        if inplace:
            self.df = __df
        return __df

    def dropHolidays(self):
        """ Drop the unactive period of the data """
        self.drop(startDate='2018-03-16', endDate='2018-04-08', inplace=True)
        self.drop(startDate='2018-08-06', endDate='2018-08-19', inplace=True)
        self.drop(startDate='2018-12-19', endDate='2019-03-10', inplace=True)
        self.drop(startDate='2019-07-08', endDate='2019-08-05', inplace=True)

    def drop(self, startTime=None, endTime=None, startDate=None, endDate=None,
             inplace=True):
        """ Drop with all the selections for the DataFrame

        Parameters
        ----------
            startTime : str
                Start time of day with the following format:
                str(%H:%M-%S) : "22:00"
                Default is None
            endTime : str
                End time of day with the following format:
                str(%H:%M-%S) : "23:59"
                Default is None
            startDate : str
                Selection start date with the following format:
                str(%y-%m-%d) : "2018-04-03"
                Default is None
            endDate : str
                Selection end date with the following format:
                str(%y-%m-%d) : "2019-09-10"
                Default is None
            inplace : bool
                If true change atribute df
                Default is True

        Return
        ------
            pandas.core.frame.DataFrame
        """
        def genDropID(args):
            """  """
            args = [str(i) for i in args if not i is None]
            args = '_'.join(args)
            args = '('+args+')'
            if not self.droped:
                self.droped = 'drop(' + args + ')'
            else:
                self.droped = self.droped[:-1] + ',' + args + ')'

        df = self.df
        if startDate and endDate:
            df = df.drop(self.nearestDateRange(startDate, endDate), axis=1)
        if startTime and endTime:
            df = df.drop(self.nearestTimeRange(startTime, endTime), axis=0)
        if inplace:
            genDropID([startDate, endDate, startTime, endTime])
            self.df = df

        return df

    def shuffle(self, seed:int, inplace:bool=True) -> pd.DataFrame:
        """ Shuffle data columns 

        Parameters
        ----------
            seed : int()
                seed to set random shuffle state
            inplace : bool()
                If true change atribute df
                Default is True
        """
        columns = self.df.columns.tolist()
        np.random.seed(seed)
        np.random.shuffle(columns)

        if inplace:
            self.shuffles.append(seed)

        self.df = self.df[columns]

    def getDataID(self) -> None:
        """ Captures the dataframe ID"""

        def getTransformationsId(self) -> list:
            """ Return transformations and parms """
            _tranformationsId = []
            if len(self.parms.keys()) > 0:
                idParms = []
                values = []
                for key in sorted(self.parms):
                    for v in self.parms[key]:
                        values = str(v)
                    idParms.append(key+'('+'_'.join(values)+')')
                _tranformationsId.append('_'.join(idParms))

            return _tranformationsId

        # Add the start and end coordinates, type and fill of the dataframe
        _id = {
            "day": self._day,
            "start_date": self.df.columns[0],
            "end_date": self.df.columns[-1],
            "start_time": self.df.index[0],
            "end_time": self.df.index[-1],
            "field": self.field,
            "ffill": self.ffill_,
            "bfill": self.bfill_,
            "seeds": self.shuffles,
            "drops": self.droped,
        }

        # alphabetically add the transformations
        _id["transformations"] = getTransformationsId(self)

        # Adds the function that generated the synthetic data (if any)
        _id["type"] = self._typeDf

        return _id

    def getDataMode(self, mode: str, data: pd.DataFrame = None, inplace: bool = True, window: int = 5) -> pd.DataFrame:
        """ Apply mean, mobile mean and mobile median operations to data

        Parameters
        ----------
            mode: str()
                ['mean', 'mobileMean', 'mobileMedian']
            data: pd.DataFrame
                Source data for operation
            inplace : bool(), default=True
                Saves the model to the Date instance
            window : int()
                window of average
        Returns
        -------
            if(you have any operations selected):
                data: data: mean, mobile mean or mobile median of data
            else:
                None
        """
        if data is None:
            data = self.df

        dataMode = {
            'mean': self.mean,
            'mobileMean': self.mobileMean,
            'mobileMedian': self.mobileMedian
        }

        if mode not in dataMode.keys():
            return data

        if mode in dataMode.keys()[1:]:
            data = dataMode[mode](data, inplace=False, window=window)
        else:
            data = dataMode[mode](data, inplace=False)

        if inplace:
            self.df = data

        return data

    def mean(self, data: pd.DataFrame, skipna: bool = True, inplace: bool = True) -> pd.DataFrame:
        """ Return mean of dataframe

        Parameters
        ----------
            data : pd.DataFrame()
                Data to get mean
            skipna : bool()
                Use or not NaN in mean
            inplace : bool(), default=True
                Saves the model to the Date instance
        Returns
        -------
            pd.DataFrame()
        """
        if data is None:
            data = self.df

        data.dropna(1, 'all', inplace=True)
        if data.index.name != 'hora' or 'hora' in data.columns:
            data.set_index('hora', inplace=True)

        df = pd.DataFrame(index=data.index)
        df['means'] = self.dropTime(data).T.mean(skipna=skipna)

        if inplace:
            self.df = df

        return df

    def mobileMean(self, data: pd.DataFrame, inplace: bool = True, window: int = 5) -> pd.DataFrame:
        """ Mobile Mean

        Parameters
        ----------
            data : pd.DataFrame
                Data to get mobile mean
            inplace : bool(), default=True
                Saves the model to the Date instance
        Returns
        -------
            pd.DataFrame
        """
        if data is None:
            data = self.df

        for day in data.drop(columns='hora', errors='ignore'):
            data[day] = numlib.mobileMean(data[day], window)
        if inplace:
            self.df = data
        return data

    def mobileMedian(self, data: pd.DataFrame, inplace: bool = True, window: int = 5) -> pd.DataFrame:
        """ Mobile Median

        Parameters
        ----------
            data : pd.DataFrame
                Data to get mobile median
            inplace : bool(), default=True
                Saves the model to the Date instance
        Returns
        -------
            pd.DataFrame
        """
        if data is None:
            data = self.df

        for day in data.drop(columns='hora'):
            data[day] = numlib.mobileMedian(data[day], window)

        if inplace:
            self.df = data

        return data

    def dropColumn(column, data: pd.DataFrame) -> pd.DataFrame:
        """ Drop Weigths

        Parameters
        ----------
        data : pd.DataFrame
            Pandas DataFrame to drop weigths from Self-Organizing Maps Cluster

        Returns
        -------
            pd.DataFrame without weigths from Self-Organizing Maps Cluster
        """
        if column in data.columns:
            data = data.drop(columns=column, errors='ignore')

        return data

    def t(self, inplace=True):
        """ Transpose DataFrame

        Parameters
        ----------
            inplace : bool()
                Saves the model to the Date instance
                Default is True

        Return
        ------
            pandas.core.frame.DataFrame transposed
        """
        if inplace:
            self.df = self.df.T
            return self.df
        else:
            return self.df.T

    def reindex(self, x):
        """  """
        return pd.DataFrame(x, index=self.df.index, columns=self.df.columns)

    def getDf(self):
        """ Returns the DataFrame """
        return self.df

    def ffill(self, inplace=True):
        """ ffill self.df. That means that evey nan value
        in self.df will be filled with the last valid value

        Parameters
        ----------
            inplace : bool()
                Saves the model to the Date instance
                Default is True

        Return
        ------
            pandas.core.frame.DataFrame No NaN intervals in columns
        """
        if inplace:
            self.df = self.df.ffill()
            return self.df
        else:
            return self.df.ffill()

    def bfill(self, inplace=True):
        """ ffill self.df. That means that evey nan value
        in self.df will be filled with the next valid value

        Parameters
        ----------
            inplace : bool()
                Saves the model to the Date instance
                Default is True

        Return
        ------
            pandas.core.frame.DataFrame No NaN intervals in rows
        """
        if inplace:
            self.df = self.df.bfill()
            return self.df
        else:
            return self.df.bfill()

    def nearestDateRange(self, startDate=None, endDate=None):
        """ Date interval with indexes

        Parameters
        ----------
            startDate : str(%Y-%m-%d)
                Ex.: startDate='2019-03-05'
                Default is None
            endDate : str(%Y-%m-%d)
                Ex.: endDate='2019-05-02'
                Default is None
        Returns
        -------
            List with the indexes closest to the parameters.
        """
        return list(self.df.loc[:, startDate:endDate].columns.values)

    def nearestTimeRange(self, startTime=None, endTime=None):
        """ Time interval with indexes

        Parameters
        ----------
            startTime : str(%H:%M)
                Ex.: startTime='22:00'
                Default is None
            endTime : str(%H:%M)
                Ex.: endTime='23:00'
                Default is None
        Returns
        -------
            List with the indexes closest to the parameters.
        """
        return list(self.df.loc[startTime:endTime, :].index.values)

    def split(self, data: pd.DataFrame=None, trainSize: float=0.5) -> list:
        """ Training and test data separator

        Parameters
        ----------
            data: pandas.DataFrame(), default=None == self.df
                Data to split.
            trainSize: float(), default=0.5
                Percentage of data intended for training.

        Returns
        -------
            list() with:
                [x_train, x_test, y_train, y_test]
        """
        if data is None:
            data = self.df

        tainEndColumnIndex = round(len(data.columns)*trainSize)

        x_train = data.iloc[None:None, None:tainEndColumnIndex].index
        x_test = data.iloc[None:None, tainEndColumnIndex:None].index
        y_train = data.iloc[None:None, None:tainEndColumnIndex]
        y_test = data.iloc[None:None, tainEndColumnIndex:None]

        return [x_train, x_test, y_train, y_test]

    def __setDay(self, day: str):
        """ Checks whether the entry is valid, that is,
        whether the day name matches in db

        Parameters
        ----------
            day : str()
                name of column
        Raises
        ----------
            Invalid Day
        """
        if day in timelib.weekdays or day in timelib.weekdaysEN:
            self._day = timelib.translate_weekday(day)
        else:
            raise ValueError('Invalid Day')

    def __setField(self, field: str):
        """ Checks whether the entry is valid, that is,
        whether the column name matches

        Parameters
        ----------
            field : str()
                name of column
        Raises
        ----------
            Invalid field
        """
        __fields = [
            'P1', 'P2', 'P3',
            'Q1', 'Q2', 'Q3',
            'FPA', 'FPB', 'FPC'
        ]

        if field in __fields:
            self.field = field
        else:
            raise ValueError('Invalid field')

    def __setDir(self, dir):
        """ Checks whether the entry is a file or directory

        Parameters
        ----------
            dir : str()
                name of column
        Raises
        ----------
            Invalid path
        """
        if os.path.isdir(dir):
            self._dir = dir
        elif os.path.isfile(dir):
            self.__file = dir
        else:
            raise ValueError('Invalid path {}'.format(dir))

    def __setFile(self, dir):
        """Directory checker

        Parameters
        ----------
            dir : str()
                Valid path to directory

        Instantiation
        --------------
            self.__file : str(path)
                If the file exists, the full path is instantiated.

        Returns
        -------
            bool()()
        """
        try:
            self.__file = [
                dir+day for day in os.listdir(dir) if self._day in day]
            self.__file = str(self.__file)[2:-2]
            return True
        except FileNotFoundError:
            return False

    def __setTable(self):
        """ Table Capture

        Checks the existence of a file with the specifications
        already instantiated and if not, try to create the table.
        """
        if self._func:
            if not self.__setFile(tables_synthetic+self._func+bar):
                try:
                    synthetic(func=self._func)
                except ValueError:
                    raise ValueError('Cannot create the synthetic table')

        elif self._day and self._dump and self.field:
            if not self.__setFile(tables_days+self._dump+bar):
                try:
                    Days(field=[self.field], days=[self._day])
                except ValueError:
                    raise ValueError('Cannot create the days table')

    def __reader(self):
        """ Read the DataFrame

        Returns
        -------
            pd.core.frame.DataFrame indexed by hours
        """
        conn = sqlite3.connect(self.__file)
        self.df = pd.read_sql(f'SELECT * FROM {self.field}', conn)
        self.df.set_index('time', inplace=True)
        self.df.index = np.array(pd.to_datetime(
            self.df.index).time).astype(str)
        self.df.index.rename('hora', inplace=True)

        self.ffill(inplace=self.ffill_)
        self.bfill(inplace=self.bfill_)
        return self.df
