import numpy as np
import pandas as pd

from lib.util.metrics import Metrics
from scipy.signal import savgol_filter


class ThresholdsController:

    def getRegressionTarget(self, source: str) -> np.ndarray:
        """ Return target for regression

        Parameters
        ----------
            source: str()
                regression, ['linear', 'ransac', 'rlm']

        Returns
        -------
            np.ndarray()
        """
        return self.R.Regressions[source].target

    def getRegressionThreshold(self, source: str, metric: str) -> np.ndarray:
        """ Return array with threshold of regression

        Parameters
        ----------
            source: str()
                regression, ['linear', 'ransac', 'rlm']
            metric: str()
                metric, ['MAE', 'RMSE', 'QE', 'MAPE']

        Returns
        -------
            np.ndarray()
        """
        return self.R.Regressions[source].get_features(
            metric=metric,
            normal=self.thresholds["metrics"][source][metric]["normal"]
        )["threshold"].flatten()

    def getSOMThresholdFromMetric(self, metric: str) -> np.ndarray:
        """ Return np.ndarray with threshold of SOM

        Parameters
        ----------
            metric: str()
                metric ["MAE", "RMSE", "QE", "MAPE"]

        Returns
        -------
            np.ndarray()
        """
        return self.getMetricFromCluster(
            metric=metric,
            source=self.getCurrentCluster().drop(columns="hora", errors='ignore'),
            target=self.getSOMWeights()
        ) + self.getSOMWeights()

    def getModelOptionsForAll(self, option: str, entry: str) -> np.ndarray:
        """ Return option of all sources

        Parameters
        ----------
            option: str()
                One of this arguments ['min','mean','max']
            entry: str()
                "absolute", constante value
                "relative", minimum horizontal

        Returns
        -------
            np.ndarray()
        """
        df = self.getAllRegressionTargets(onlyDisplayed=True)

        if self.R.Clusterize and self.thresholds["models"]["weights"]["show"]:
            df['weights'] = self.getSOMWeights()

        if not df.empty:
            return self.getThresholdMode(
                option=option,
                mode=entry,
                data=df.values
            )

    def getRegressionsMetricsFromSource(self, source: str, option: str, entry: str) -> np.ndarray:
        """ Return option from all metris of a source

        Parameters
        ----------
            source: str()
                regression, ['linear', 'ransac', 'rlm']
            option: str()
                One of this arguments ['min','mean','max']
            entry: str()
                "absolute", constante value
                "relative", minimum horizontal

        Returns
        -------
            np.ndarray()
        """
        df = pd.DataFrame()
        for _metric in self.thrMetrics:
            df[_metric] = self.getRegressionThreshold(source, _metric)

        if not df.empty:
            return self.getThresholdMode(
                option=option,
                mode=entry,
                data=df.values
            )

    def getModelMetricsForAll(self, metric: str, option: str, entry: str, onlyDisplayed: bool=False) -> np.ndarray:
        """ Return option from all sources of a metric

        Parameters
        ----------
            metric: str()
                Error metric in ["MAE", "RMSE", "QE", "MAPE"]
            option: str()
                One of this arguments ['min','mean','max']
            entry: str()
                "absolute", constante value
                "relative", minimum horizontal
            onlyDisplayed: bool()
                use only displayed values

        Returns
        -------
            np.ndarray()
        """
        df = pd.DataFrame()
        if onlyDisplayed:
            for source in self.thrSources:
                if self.thresholds["metrics"][source][metric]["show"]:
                    df[source] = self.getRegressionThreshold(source, metric)
        else:
            for source in self.thrSources:
                df[source] = self.getRegressionThreshold(source, metric)


        if self.R.Clusterize and self.thresholds["metrics"]["weights"][metric]["show"]:
            df["weights"] = self.getSOMThresholdFromMetric(metric)

        if not df.empty:
            return self.getThresholdMode(
                option=option,
                mode=entry,
                data=df.values
            )

    def getAllOptionsFromRegressions(self, option: str, entry: str) -> np.ndarray:
        """ Return option from all thresholds viewed

        Parameters
        ----------
            option: str()
                One of this arguments ['min','mean','max']
            entry: str()
                "absolute", constante value
                "relative", minimum horizontal
        Returns
        -------
            np.ndarray()
        """
        thresholds = pd.DataFrame()
        for source in self.thrSources:
            df = pd.DataFrame()
            
            if self.thresholds['models'][source]['show']:
                df[source] = self.getRegressionTarget(source)

            for metric in self.thrMetrics:
                if self.thresholds["metrics"][source][metric]["show"]:
                    df[metric] = self.getRegressionThreshold(source, metric)

            if not df.empty:
                thresholds[source] = self.getThresholdMode(
                    option=option,
                    mode=entry,
                    data=df.values
                )

        if not thresholds.empty:
            return self.getThresholdMode(
                option=option,
                mode=entry,
                data=thresholds.values
            )

    def getBothThresholds(self, option: str, entry: str) -> np.ndarray:
        """ Returns the minimum, average or maximum of all
        models added to the metrics

        Parameters
        ----------
            option: str()
                One of this arguments ['min','mean','max']
            entry: str()
                "absolute", constante value
                "relative", minimum horizontal
        Returns
        -------
            np.ndarray()
        """
        ls = [self.getThresholdMode(
            option=option,
            mode=entry,
            data=self.getAllRegressionTargets()
        )]

        __thresholds = []
        for source in self.thrSources:
            df = pd.DataFrame()
            for metric in self.thrMetrics:
                df[source+metric] = self.getRegressionThreshold(source, metric)
                if self.R.Clusterize:
                    df[source+metric + "_w"] = self.getSOMThresholdFromMetric(metric)

            if not df.empty:
                __thresholds.append(df)
        
        for threshold in __thresholds:
            ls.append(self.getThresholdMode(
                option=option,
                mode=entry,
                data=threshold
            ))

        return self.getThresholdMode(option=option, mode=entry, data=pd.DataFrame(ls).T)

    def getAllRegressionTargets(self, onlyDisplayed: bool = False) -> np.ndarray:
        """ Return pd.DataFrame with all regression targets

        Parameters
        ----------
            onlyDisplayed: bool(), default False
                uses only viewed thresholds sources, if not use all

        Returns
        -------
            np.ndarray()
        """
        df = pd.DataFrame()

        if onlyDisplayed:
            for source in self.thrSources:
                if self.thresholds['models'][source]['show']:
                    df[source] = self.getRegressionTarget(source)
        else:
            for source in self.thrSources:
                df[source] = self.getRegressionTarget(source)

        return df

    def getThresholdMode(self, option: str, mode: str, data):
        """ Transform data

        Parameters
        ----------
            option: str()
                One of this arguments ['min','mean','max']
            mode: str()
                One of this arguments ['absolute','relative']

            data: np.ndarray() | pd.DataFrame() | pd.Series()
                Data source

        Returns
        -------
            Data transformed into a 1D array
        """
        _OPTIONS_FUNCS = {
            "min": np.min,
            "mean": np.mean,
            "max": np.max
        }

        data = pd.DataFrame(data)
        length = data.shape[0]

        data = _OPTIONS_FUNCS[option](data.T)

        if mode == 'absolute':
            data = _OPTIONS_FUNCS[option](data) + ([0] * length)

        return data

    def getMetricFromCluster(self, metric: str, source, target) -> np.ndarray:
        """ Calculate the selected metric for the cluster data

        Parameters
        ----------
            metric: str()
                Error metric in ["MAE", "RMSE", "QE", "MAPE"]
            source: np.ndarray() | pd.series()
                Is the data source to calculate the difference.
                It can be a single array or an 2D matrix.
            target: np.ndarray() | pd.series()
                Is the model to compare the difference. The
                size must be the same as array rows size.

        Returns
        -------
            np.ndarray()
        """
        _metric = Metrics(
            source=source,
            target=target
        )

        if metric == "MAE":
            return _metric.MAE()
        if metric == "MSE":
            return _metric.MSE()
        if metric == "RMSE":
            return _metric.RMSE()
        if metric == "QE":
            return _metric.QE()
        if metric == "MAPE":
            return _metric.MAPE()
        else:
            raise Exception("Incorrect metric")
    
    def getFilterFromCluster(self, metric:str, filter: str) -> np.ndarray:
        """  """
        if filter == "savgol":
            return savgol_filter(self.getSOMThresholdFromMetric(metric), 59, 4)

    def getFilterFromMetric(self, source:str, metric:str, filter:str) -> np.ndarray:
        """  """
        if filter == "savgol":
            return savgol_filter(self.getRegressionThreshold(source, metric), 59, 4)
