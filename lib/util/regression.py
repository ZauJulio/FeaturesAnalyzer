from copy import deepcopy

import numpy as np
import pandas as pd
import sklearn.linear_model as lm
import sklearn.preprocessing as pp
import statsmodels.api as sm

from lib.data_manager import data
from lib.util import timelib, path
from lib.util.metrics import Metrics

__all__ = ['LinearModel', 'RLM', 'RANSAC']


class _Regression(Metrics):
    def __init__(self, source=None, deg=5, metrics_data=None):
        """ _Regression

        This class is a private father class to implements hierarchy, that
        means that _Regression will be not imported, but used for LinearModel,
        RLM and RANSAC

        Args:
            source (pandas.code.frame.DataFrame): This parameter is the
            train data for the regression

            deg (int): This is a degree for the polynimial features
        """
        self.model = None
        self.deg = deg
        self.target = np.array([])
        self.trained = False
        self.source = source
        self.metrics_data = metrics_data
        self.features = None
        if self.source is None:
            reader = data.Data(path.tables, "segunda", _ffill=True)
            self.source = reader.filter("20:00", "24:00", *timelib.semester2018_1)
        self._process_data()

    def _process_data(self):
        """ _process_data

        This method will process the data. Remove all nan values that it can
        have and populate self.xTrain with day minutes for all columns in
        self.source. Also populate self.y will a single array for all values in
        self.source
        """
        if self.source.isna().any().any():
            self.source = self.source.ffill().bfill()

        if 'hora' in self.source.columns:
            self.source.set_index('hora')

        self.xTest = self.source.index.to_numpy()
        if type(self.xTest[0]) == str:
            self.xTest = timelib.strtime_to_minute(self.xTest)
        else:
            self.xTest = timelib.time_to_minute(self.xTest)

        self.xTrain = np.array([self.xTest for i in self.source])
        self.xTrain = self.xTrain.reshape(-1, 1)
        self.xTest = self.xTest.reshape(-1, 1)
        self.y = np.array([self.source[i] for i in self.source]).reshape(1, -1)[0]

        # Remove NaN
        nan_mask = ~np.isnan(self.y)
        self.y = self.y[nan_mask]
        self.xTrain = self.xTrain[nan_mask]

        if self.metrics_data is None:
            self.metrics_data = self.source

    def _polynomialFeatures(self, arr):
        """ _polynomialFeatures

        This method turn the passed array into a polynimial series

        Args:
            arr (list of ints): A sequential array of ints
        Returns:
            (list): A list with Polynomial Features
        """
        poly_features = pp.PolynomialFeatures(
            degree=self.deg, include_bias=False)
        return poly_features.fit_transform(arr)

    def predict(self):
        """ predict

        This method return a predict model based in the regression for the
        self.source.

        Returns:
            (numpy.array): It returns a predict model
        """
        self.trained = True
        self.target = self.model.predict(self.x_test)
        return self.target

    def get_features(self, metric, normal: bool = True) -> dict:
        """ get_object

        This method returns a object with all regression features

        Args:
            normal (bool): If False, the MAE will ignore every point bellow
            the predict data

        Returns:
            (dict): It returns a dict like:
                {
                    "xAxis":
                        This is a temporal data used to plot when loading
                        this object
                    "values":
                        The predicted data, the model
                    "accuracy":
                        In multilabel classification, this function
                        computes subset accuracy: the set of labels predicted for
                        a sample must exactly match the corresponding set of labels
                        in y_true.
                    "r2":
                        Best possible score is 1.0 and it can be negative (because
                        the model can be arbitrarily worse). A constant model that
                        always predicts the expected value of y, disregarding the
                        input features, would get a R^2 score of 0.0.
                }
        """
        if not self.trained:
            self.train()

        xAxis = timelib.minute_to_time(self.xTest)

        if metric == "MAE":
            metric = self.MAE
        if metric == "MSE":
            metric = self.MSE
        if metric == "RMSE":
            metric = self.RMSE
        if metric == "QE":
            metric = self.QE
        if metric == "MAPE":
            metric = self.MAPE

        self.features = {
            "xAxis": xAxis,
            "values": self.target,
            "threshold": metric(normal=normal) + self.target
        }
        return self.features

    def get_source_data(self):
        return {
            'x': self.xTrain,
            'y': self.y
        }

    def save_features(self, filename):
        """ save_object
        This method save the object model

        Args:
            filename (string): This is the name of the file to save

        Returns:
            nothing, but save a object with pickle library:
            (dict)
                {
                    "xAxis":
                        This is a temporal data used to plot when loading
                        this object
                    "values":
                        The predicted data, the model
                    "accuracy":
                        In multilabel classification, this function
                        computes subset accuracy: the set of labels predicted for
                        a sample must exactly match the corresponding set of labels
                        in y_true.
                    "r2":
                        Best possible score is 1.0 and it can be negative (because
                        the model can be arbitrarily worse). A constant model that
                        always predicts the expected value of y, disregarding the
                        input features, would get a R^2 score of 0.0.
                }

        """
        if self.features is None:
            self.get_object()

        _features = deepcopy(self.features)
        index = _features.pop('xAxis')
        pd.DataFrame(_features, index=index).to_csv(filename)


class LinearModel(_Regression):
    def train(self):
        """ train
        This method train the model with all loaded data. First it calls the
        _polynomialFeatures for xTrain and xTest, and after that it fits its
        values.

        Returns:
            (list): return the model predict, see _Regression.predict()
        """
        x_train = self._polynomialFeatures(self.xTrain)
        self.x_test = self._polynomialFeatures(self.xTest)

        self.model = lm.LinearRegression().fit(x_train, self.y)
        return self.predict()


class RANSAC(_Regression):
    def train(self):
        """ train
        This method train the model with all loaded data. First it calls the
        _polynomialFeatures for xTrain and xTest, and after that it fits its
        values.

        Returns:
            (list): return the model predict, see _Regression.predict()
        """
        x_train = self._polynomialFeatures(self.xTrain)
        self.x_test = self._polynomialFeatures(self.xTest)

        self.model = lm.RANSACRegressor(random_state=0).fit(x_train, self.y)
        return self.predict()


class RLM(_Regression):
    def train(self):
        """ train
        This method train the model with all loaded data. First it calls the
        _polynomialFeatures for xTrain and xTest, and after that it fits its
        values.

        Returns:
            (list): return the model predict, see _Regression.predict()
        """
        x_train = self._polynomialFeatures(self.xTrain)
        self.x_test = self._polynomialFeatures(self.xTest)

        self.model = sm.RLM(self.y, x_train).fit()
        return self.predict()
