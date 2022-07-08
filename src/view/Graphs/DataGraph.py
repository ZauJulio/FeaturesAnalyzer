from itertools import product
from matplotlib import pyplot as plt

import pandas as pd
import numpy as np


class DataGraph:

    def __modelsOutlier(self):
        """ Update mask with simple predicted data model """
        for source in self.thrSources:
            if self.thresholds["models"][source]["outlier"]:
                self.__updateMaskData(
                    self.getRegressionTarget(source), isSource=True)

    def __modelsOutlierOptions(self):
        """ Update mask with option(Min, Mean, Max) absolute point for threshold """
        iterator = product(self.thrSources, self.thrOptions, self.thrEntries)
        for source, option, entrie in iterator:
            if self.thresholds["models"][source][option]["outlier"]:
                self.__updateMaskData(self.getThresholdMode(
                    option=option,
                    mode=entrie,
                    data=self.getRegressionTarget(source)
                ), isSource=True)

    def __modelsOutlierOptionsForAllSources(self):
        """ Update mask with option(Min, Mean, Max) for all thresholds without metric """
        for option, entrie in product(self.thrOptions, self.thrEntries):
            if self.thresholds["models"]["all"][option][entrie]["outlier"]:
                self.__updateMaskData(
                    self.getModelOptionsForAll(option, entrie), isSource=True)

    def __metricsOutlier(self):
        """ Update mask with single data metric for model """
        for source, metric in product(self.thrSources, self.thrMetrics):
            if self.thresholds["metrics"][source][metric]["outlier"]:
                self.__updateMaskData(
                    self.getRegressionThreshold(source, metric)
                )

    def __metricsOutlierFiltered(self):
        """ Update mask with single data metric for model """
        for source, metric, filter in product(self.thrSources, self.thrMetrics, self.thrFilters):
            if self.thresholds["metrics"][source][metric]["filters"][filter]["outlier"]:
                self.__updateMaskData(
                    self.getFilterFromMetric(source, metric, filter)
                )

    def __metricsWeightsOutlier(self):
        """  """
        for metric in self.thrMetrics:
            if self.thresholds["metrics"]["weights"][metric]["outlier"]:
                self.__updateMaskData(
                    self.getSOMThresholdFromMetric(metric),
                )

    def __metricsWeightsOutlierFiltered(self):
        """  """
        for metric, filter in product(self.thrMetrics, self.thrFilters):
            if self.thresholds["metrics"]["weights"][metric]["filters"][filter]["outlier"]:
                self.__updateMaskData(
                    self.getFilterFromCluster(metric, filter),
                )

    def __metricsWeightsOutlierOptions(self):
        """ Update mask with option(Min, Mean, Max) absolute point for metric of weights """
        for metric, option in product(self.thrMetrics, self.thrOptions):
            if self.thresholds["metrics"]["weights"][metric][option]["outlier"]:
                self.__updateMaskData(
                    self.getThresholdMode(
                        option=option,
                        mode="absolute",
                        data=self.getSOMThresholdFromMetric(metric)
                    )
                )

    def __metricsOutlierOptions(self):
        """ Update mask with option(Min, Mean, Max) absolute point for metric """
        iterator = product(self.thrSources, self.thrMetrics, self.thrOptions)
        for source, metric, option in iterator:
            if self.thresholds["metrics"][source][metric][option]["outlier"]:
                self.__updateMaskData(
                    self.getThresholdMode(
                        option=option,
                        mode="absolute",
                        data=self.getRegressionThreshold(source, metric)
                    )
                )

    def __metricsOptionsForAllMetrics(self):
        """ Update mask with option(Min, Mean, Max) for all metric """
        iterator = product(self.thrSources, self.thrOptions, self.thrEntries)
        for source, option, entrie in iterator:
            if self.thresholds["metrics"][source]["all"][option][entrie]["outlier"]:
                self.__updateMaskData(
                    self.getRegressionsMetricsFromSource(
                        source, option, entrie)
                )

    def __metricsOutlierOptionsForAllModels(self):
        """ Update mask with option(Min, Mean, Max) for all models with metric """
        iterator = product(self.thrMetrics, self.thrOptions, self.thrEntries)
        for metric, option, entrie in iterator:
            if self.thresholds["metrics"]["all"][metric][option][entrie]["outlier"]:
                self.__updateMaskData(
                    self.getModelMetricsForAll(metric, option, entrie)
                )

    def __bothModelsMetricsOutlier(self):
        """  """
        for option, entrie in product(self.thrOptions, self.thrEntries):
            if self.thresholds["both"][option][entrie]["outlier"]:
                self.__updateMaskData(
                    self.getBothThresholds(option, entrie)
                )

    def __plotData(self):
        """  """
        if self.R.Clusterize:
            data = self.getDataMode(self.getCurrentCluster(
                dropTime=True, dropWeights=True))
        else:
            if self.R.ShowTrain:
                data = self.dataTrain.copy()
            elif self.R.ShowTest:
                data = self.dataTest.copy()
            else:
                return

        COLORS = [
            'darkorange', 'royalblue',
            'lightcoral', 'slateblue',
            'khaki', 'teal'
        ]

        if self.R.ShowSample not in data:
            self.R.ShowSample = "All"

        if self.R.ShowSample == "All":
            if self.R.Clusterize and self.R.diffClusters:
                i = 0
                for column in data:
                    label = column.split('-')
                    label = label[-1]+'/'+label[1]+'/'+label[0]

                    self.ax.plot(
                        self.time,
                        data[column].astype(int),
                        'o',
                        color=COLORS[i if i < len(COLORS) else i % len(COLORS)],
                        label=label,
                        markersize=5,
                        markeredgewidth=0,
                        alpha=0.4,
                    )
                    i += 1
            else:
                self.ax.plot(
                    self.time,
                    data,
                    'o',
                    color="black",
                    markersize=6,
                    markeredgewidth=0,
                    alpha=0.3
                )
        else:
            self.ax.plot(
                self.time,
                data[self.R.ShowSample],
                'o',
                color='black',
                markersize=4,
                markeredgewidth=0,
            )

    def __plotMediumLine(self):
        """  """
        if self.R.MediumLine:

            if self.LANGUAGE == 'en_us':
                label = "Mean of Data"
            elif self.LANGUAGE == 'pt_br':
                label = "Média dos Dados"

            self.ax.plot(
                self.time,
                self.mediumLine,
                label=label
            )

    def __updateMaskData(self, model, isSource:bool=False) -> None:
        """  """
        dataMask = pd.DataFrame(
            False,
            columns=self.__data.columns,
            index=self.__data.index
        )

        if len(model.shape) == 1:
            model = np.ravel(model)

        if isSource:
            check = self.__data.values.T < model.T
            dataMask = np.logical_xor(check.T, dataMask)
            self.__dataMask[dataMask] = 1
        else:
            check = self.__data.values.T > model.T
            dataMask = np.logical_xor(check.T, dataMask)
            self.__dataMask[dataMask] = 2

    def __plotAlarms(self):
        """  """
        if self.__data[self.__dataMask == 2][self.timeLimit:].any().any():
            self.alarmsFound = True

        self.ax.plot(
            self.time[self.timeLimit:],
            self.__data[self.__dataMask == 2][self.timeLimit:],
            'x',
            color='C3',
            markersize=4,
        )

    def __plotAboveExpected(self):
        """  """
        if self.__data[self.__dataMask == 2][:self.timeLimit].any().any():
            self.aboveExpectedFound = True

        self.ax.plot(
            self.time[:self.timeLimit],
            self.__data[self.__dataMask == 2][:self.timeLimit],
            'x',
            color='darkgoldenrod',
            markersize=4,
        )

    def __plotExpected(self):
        """  """
        self.expectedFound = self.__data[self.__dataMask == 0].any().any()

        self.ax.plot(
            self.time,
            self.__data[self.__dataMask == 0],
            'x',
            color='C2',
            markersize=4,
        )

    def __plotBellowExpected(self):
        """  """
        if self.__data[self.__dataMask == 1].any().any():
            self.bellowExpectedFound = True

        self.ax.plot(
            self.time,
            self.__data[self.__dataMask == 1],
            'x',
            color='C0',
            markersize=4,
        )

    def __plotOutliers(self):
        """  """
        if self.__data[self.__dataMask == 2].any().any():
            self.outliersFound = True

        self.ax.plot(
            self.time,
            self.__data[self.__dataMask == 2],
            'x',
            color='C3',
            markersize=4,
        )

    def __setData(self):
        """  """
        if self.R.ShowTrain:
            if self.R.Clusterize:
                if self.R.ShowSample in self.trainClusters[self.R.Cluster]:
                    self.__data = self.trainClusters[self.R.Cluster][self.R.ShowSample].copy()
                else:
                    self.__data = self.trainClusters[self.R.Cluster].copy()

            elif self.R.ShowSample in self.dataTrain:
                self.__data = self.dataTrain[self.R.ShowSample].copy()
            else:
                self.__data = self.dataTrain.copy()

        else:
            if self.R.ShowSample in self.dataTest:
                self.__data = self.dataTest[[self.R.ShowSample]].copy()
            else:
                self.__data = self.dataTest.copy()

        self.__data.drop(columns=['hora', 'weights'],
                         errors='ignore', inplace=True)

    def __setDataMask(self):
        """  """
        self.__dataMask = pd.DataFrame(
            0,
            columns=self.__data.columns,
            index=self.__data.index
        )

    def __updateMask(self):
        """  """
        self.__modelsOutlier()
        self.__modelsOutlierOptions()
        self.__modelsOutlierOptionsForAllSources()

        self.__metricsOutlier()
        self.__metricsOutlierFiltered()
        self.__metricsOutlierOptions()
        self.__metricsOptionsForAllMetrics()

        self.__metricsWeightsOutlier()
        self.__metricsWeightsOutlierFiltered()
        self.__metricsWeightsOutlierOptions()

        self.__metricsOutlierOptionsForAllModels()

        self.__bothModelsMetricsOutlier()

    def plotData(self):
        """  """
        self.alarmsFound = False
        self.aboveExpectedFound = False
        self.bellowExpectedFound = False
        self.outliersFound = False

        self.ax = self.fig.add_subplot(*self.subplots)

        self.__setData()
        self.__setDataMask()
        self.__updateMask()

        self.__plotMediumLine()
        if self.R.ColorClassification:
            self.__plotAboveExpected()
            self.__plotExpected()
            self.__plotBellowExpected()
            self.__plotAlarms()
        else:
            self.__plotData()
            self.__plotOutliers()

        del self.__data
        del self.__dataMask
