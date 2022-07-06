from copy import deepcopy
from lib.data_manager.data import Data as DataManager
from lib.util import timelib, numlib
import pandas as pd
import numpy as np
import sys


class DataController:

    def updateData(self) -> None:
        """ Apply the data usage pattern for model formation

        Returns
        -------
        None
        """
        if self.R.Clusterize:
            self.dataTrain = self.loadClusterizer()
            self.trainClusters = self.clusterize(data=self.dataTrain)
            
            if self.R.ShowTrain:
                self.testClusters = deepcopy(self.trainClusters)
            else:
                self.testClusters = self.clusterize(self.getData())
            self.dataTest = self.getDataMode(data=self.testClusters[self.R.Cluster])
        else:
            self.dataTrain = self.getDataMode(self.getData('train'))
            self.dataTest = self.getData()

        self.setTime(self.dataTrain)
        self.setMetricData()
        self.setMediumLine(self.dataTest)

    def getData(self, dataType: str = None) -> pd.DataFrame:
        """ Loads and filters data based on the type

        Parameters
        ----------
        dataType: str
            'train' or 'test'

        Returns
        -------
        pd.DataFrame
        """
        if dataType is None:
            if self.R.ShowTrain:
                dataType = 'train'
            else:
                dataType = 'test'
                
        period = self.getPeriod(dataType)

        startDate = period[0][0]
        endDate = period[1][1]

        startDateDrop = period[0][1]
        endDateDrop = period[1][0]
        
        reader = DataManager(
            day=self.getWeekday(),
            field=self.R.Field,
            ffill=self.R.ReplaceNaN,
            bfill=self.R.ReplaceNaN,
            transform=self.R.Transformation
        )
        # Filter Data in datetime
        reader.filter(
            startTime=self.R.HourStart,
            endTime=self.R.HourEnd,
            startDate=startDate,
            endDate=endDate,
            inplace=True
        )

        # Drop custom date interval
        if self.R.DropInterval:
            reader.drop(
                startDate=startDateDrop,
                endDate=endDateDrop,
                inplace=True
            )

        # Set hour to column
        return reader.getDf()

    def setMediumLine(self, data: pd.DataFrame):
        """  """
        self.mediumLine = np.zeros(len(data.index)) + data.mean().mean()

    def setMetricData(self):
        """ Update Metric data """
        if self.R.Clusterize:
            self.metricData = self.trainClusters[self.R.Cluster]
        else:
            self.metricData = self.dataTrain

    def setTime(self, data: pd.DataFrame) -> None:
        """ Set time """
        if 'hora' in data.columns:
            self.time = data['hora'].tolist()
        elif data.index.name == 'hora':
            self.time = data.index.tolist()
        if self.R.TimeLimit != "":
            self.timeLimit = data.index.tolist().index(self.R.TimeLimit)

    def getDataMode(self, data: pd.DataFrame = None) -> pd.DataFrame:
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

        dataMode = {
            'mean': self.mean,
            'mobileMean': self.mobileMean,
            'mobileMedian': self.mobileMedian
        }

        if self.R.DataType == "default":
            return data

        return dataMode[self.R.DataType](data)

    def mean(self, data: pd.DataFrame, skipna: bool = True) -> pd.DataFrame:
        """ Return mean of dataframe

        Parameters
        ----------
            data : pd.DataFrame()
                Data to get mean
            skipna : bool()
                Use or not NaN in mean
        Returns
        -------
            pd.DataFrame()
        """
        data.dropna(1, 'all', inplace=True)
        if data.index.name != 'hora' or 'hora' in data.columns:
            data.set_index('hora', inplace=True)

        df = pd.DataFrame(index=data.index)
        df['means'] = data.drop('hora', axis=1, errors='ignore').T.mean(skipna=skipna)

        return df

    def mobileMean(self, data: pd.DataFrame) -> pd.DataFrame:
        """ Mobile Mean

        Parameters
        ----------
            data : pd.DataFrame
                Data to get mobile mean
        Returns
        -------
            pd.DataFrame
        """
        for day in data.drop(columns='hora', errors='ignore'):
            data[day] = numlib.mobileMean(data[day], self.R.MobMeanMin)
        return data

    def mobileMedian(self, data: pd.DataFrame) -> pd.DataFrame:
        """ Mobile Median

        Parameters
        ----------
            data : pd.DataFrame
                Data to get mobile median
        Returns
        -------
            pd.DataFrame
        """
        for day in data.drop(columns='hora'):
            data[day] = numlib.mobileMedian(data[day], self.R.MobMedianMin)
        return data

    def getWeekday(self):
        """  """
        if self.LANGUAGE == 'pt_br':
            key = 'todos'
        elif self.LANGUAGE == 'en_us':
            key = 'all'
        else:
            raise Exception("Unknown language")
        
        if self.R.Weekday.lower() == key:
            return timelib.weekdays
        else:
            return [self.R.Weekday]

    def getPeriod(self, field: str) -> list:
        """ Get data period

        Parameters
        ----------
        field: str
            data type [train, test]

        Returns
        -------
        period: list
            list with pre-defined data periods in semestres
        """

        semestres = {
            '2018.1': timelib.semester2018_1,
            '2018.2': timelib.semester2018_2,
            '2019.1': timelib.semester2019_1,
            '2019.2': timelib.semester2019_2
        }

        init = semestres[self.settings['data'][field + 'Start']][0]
        end = semestres[self.settings['data'][field + 'End']][1]
        if end < init:
            return semestres[self.R.DateTrainStart]

        return [
            semestres[self.settings['data'][field + 'Start']],
            semestres[self.settings['data'][field + 'End']]
        ]
