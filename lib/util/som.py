import os
from collections import defaultdict
from typing import Union

import numpy as np
import pandas as pd
from minisom import MiniSom
from lib.util.numlib import dot
from lib.util.metrics import Metrics
from sklearn import metrics as skMetrics

from .path import bar

verbose = True


def convertLabelsToInt(labels: Union[list, tuple], xdim: int, ydim: int) -> list:
    """ Convert 2D label to 1D

    Parameters
    ----------
        labels: list
            List of tuples, or like, with labels.
        xdim && ydim: int
            Model dimensions, therefore, limit values
            on label tuples.

    Returns
    -------
        list 1d with labels.
    """
    i = -1
    labels_like = {(x, y): (++i)
                   for x in range(xdim)
                   for y in range(ydim)}

    return [labels_like[coor] for coor in labels]


class SelfOrganizingMaps(MiniSom):
    def __init__(self, data, x: int = -1, y: int = -1, inputLen: int = -1,
                 iterations: int = -1, sigma: float = 1.0, learningRate: float = 0.5,
                 neighborhoodFunction: str = 'gaussian', topology: str = 'rectangular',
                 activationDistance: str = 'euclidean', weightsInit: str = "random",
                 randomOrder: bool = False, transpose: bool = True,
                 ):
        """
        Parameters
        ----------
            data: np.array() or pandas.DataFrame()

            x: int, (default=-1 : Choose an optimized size)
                Number of nodes in X axis

            y: int, (default=-1 : Choose an optimized size)
                Number of nodes in Y axis

            inputLen: int, (default=-1 : Uses the number of columns in the data)
                Number of the elements of the vectors in input

            iterations: int, (default=-1 : Uses the number of samples * the length of the samples)
                Number of iterations

            sigma: float, (default=1.0)
                Spread of the neighborhood function, needs to be adequate
                to the dimensions of the map.
                (at the iteration t we have sigma(t) = sigma / (1 + t/T)
                where T is #num_iteration/2)

            learningRate: float, (default=0.5)
                (at the iteration t we have
                learning_rate(t) = learning_rate / (1 + t/T)
                where T is #num_iteration/2)

            neighborhoodFunction: str, optional (default='gaussian')
                Function that weights the neighborhood of a position in the map.
                Possible values: 'gaussian', 'mexican_hat', 'bubble', 'triangle'

            topology: str, (default='rectangular')
                Topology of the map.
                Possible values: 'rectangular', 'hexagonal'

            activationDistance: str, (default='euclidean')
                Distance used to activate the map.
                Possible values: 'euclidean', 'cosine', 'manhattan', 'chebyshev'

            weightsInit: str, (default='random')
                random: Initializes the weights by randomly sampling data
                pca: Initializes the weightsfrom the two main data components

            randomOrder: bool, optional (default=True)
                Conducts training with random samples or sequentially

            transpose: bool, optional (default=True)
                Transposes the data
        """
        if type(data) is pd.DataFrame:
            data = data.values

        if transpose:
            data = data.T

        self.nSamples = data.shape[0]
        self.lenghtSample = data.shape[1]

        self.__setInputLen(inputLen)
        self.__setIterations(iterations)
        self.__setMapDimension(x, y)

        super().__init__(
            x=self.x,
            y=self.y,
            input_len=self.inputLen,
            sigma=sigma,
            learning_rate=learningRate,
            neighborhood_function=neighborhoodFunction,
            topology=topology,
            activation_distance=activationDistance
        )

        if weightsInit.lower() == "random":
            self.random_weights_init(data)
        elif weightsInit.lower() == "pca":
            self.pca_weights_init(data)
        else:
            raise ValueError(
                "Invalid or non-existent initialization of synaptic weights."
            )

        self.train(
            data=data,
            num_iteration=self.iterations,
            random_order=randomOrder,
            verbose=verbose
        )

    def __setInputLen(self, inputLen: int) -> None:
        """ If inputLen equals -1, the sample length will be
        defined as the size of the columns """
        if inputLen == -1:
            self.inputLen = self.lenghtSample
        else:
            self.inputLen = inputLen

    def __setIterations(self, iterations: int) -> None:
        """ If iterations equals -1, Uses the number of
        samples * the length of the samples """
        if iterations == -1:
            self.iterations = self.nSamples * self.lenghtSample
        else:
            self.iterations = iterations

    def __setMapDimension(self, x: int, y: int) -> None:
        """ If x and y are -1, use the smallest square
        of the root of 5 * to root the number of samples """
        if x == -1 and y == -1:
            self.x = int(np.ceil(np.sqrt(5 * np.sqrt(self.nSamples))))
            self.y = int(self.x)
        else:
            self.x = int(x)
            self.y = int(y)

    def getKeys(self) -> list:
        """  """
        return [(x, y) for x in range(self.x) for y in range(self.y)]

    def clusterize(self, data, onlyGrouped: bool = False) -> dict:
        """ Cluster a data (or set) from the trained model

        Parameters
        ----------

            data: np.ndarray | pd.DataFrame
                Sample or set of samples for clustering.

                It is possible to send N samples for clustering, the
                following structure will be returned: a dictionary with
                the keys corresponding to the indexes, in tuples, and a
                Dataframe pandas with the days in the columns, indexed
                by the hours. The first column of the Dataframe, weights,
                corresponds to the synaptic weights of the winning neuron.

                If a single sample is sent, a tuple will be returned with
                the index values of the winning neuron. This sample may
                have a smaller number of values than the training data set.

        Return
        ------
            dict
                {tuple(indexOfCluster) :pd.DataFrame(Days grouped with synaptic weights)}
        """

        if len(data.shape) == 1:
            # winner = self.partialWinner(data)
            # return {winner:pd.DataFrame({
            #     "weights":self._weights[winner],
            #     "data":data
            # })}
            return self.partialWinner(data)
        else:
            winMap = dict(self.win_map(data.to_numpy(), return_indices=True))
            winMap = dict(sorted(winMap.items()))
            index = data.T.index

            if onlyGrouped:
                for key in winMap.keys():
                    x = {"weights": pd.Series(self._weights[key], index=index)}
                    for day in winMap[key]:
                        x.update({data.iloc[day].name: data.iloc[day]})
                    winMap[key] = pd.concat(x, axis=1)
            else:
                for key in [(i, j) for i in range(self.x) for j in range(self.y)]:
                    x = {"weights": pd.Series(self._weights[key], index=index)}
                    if key in winMap.keys():
                        for day in winMap[key]:
                            x.update({data.iloc[day].name: data.iloc[day]})
                    winMap[key] = pd.concat(x, axis=1)

            return winMap

    def partialWinner(self, x):
        """ Computes the coordinates of the winning neuron for the sample x. """
        _map = np.linalg.norm(
            np.subtract(
                x,
                self._weights[:, :, :x.shape[0]]
            ),
            axis=-1)
        return np.unravel_index(_map.argmin(), _map.shape)

    def saveClusters(self, data, clusters: dict = {}, path='som_cluster' + bar) -> None:
        """ Save clusters to files

        Parameters
        ----------
            data: np.ndarray | pd.DataFrame
                data in non-clustered
            or
            clusters: dict
                clusters in clusterize format

            path: str, (default='som_cluster/')
                Path to save the file
        """
        if len(clusters.keys()) == 0:
            clusters = self.clusterize(data)
        if not os.path.isdir(path):
            os.makedirs(path)
        for key in clusters:
            clusters[key].to_csv(path + str(key) + '.csv')

    @staticmethod
    def getVarianceFromCluster(data: np.ndarray, cluster: list) -> float:
        """ Return mean of variance of current cluster"""
        if data[cluster].shape[0] == 0:
            return np.nan

        return np.var(data[cluster], axis=1).mean()

    @staticmethod
    def getMeanFromCluster(data: np.ndarray, cluster: list) -> float:
        """ Return absolute mean of the current cluster"""
        if data[cluster].shape[0] == 0:
            return np.nan

        return np.mean(data[cluster], axis=1).mean()

    @staticmethod
    def getStdFromCluster(data: np.ndarray, cluster: list) -> float:
        """ Return mean of standard deviation of current cluster"""
        if data[cluster].shape[0] == 0:
            return np.nan

        return np.std(data[cluster], axis=1).mean()

    def getQeFromCluster(self, data: np.ndarray, cluster: list) -> float:
        """ Return mean of quantization_error from current cluster"""
        if data[cluster].shape[0] == 0:
            return np.nan

        return self.quantization_error(data[cluster])

    def getDotProductFromCluster(self, data: np.ndarray, cluster: tuple) -> float:
        """ Return dot product mean of current cluster"""
        if data[cluster].shape[0] == 0:
            return np.nan

        return dot(data[cluster], np.ravel(self._weights[cluster])).mean()

    def getDotProductVarianceFromCluster(self, data: np.ndarray, cluster: tuple) -> float:
        """ Return dot product viance of current cluster"""
        if data[cluster].shape[0] == 0:
            return np.nan

        return dot(data[cluster], np.ravel(self._weights[cluster])).var()

    def getDotProductStdFromCluster(self, data: np.ndarray, cluster: tuple) -> float:
        """ Return dot product std of current cluster"""
        if data[cluster].shape[0] == 0:
            return np.nan

        return dot(data[cluster], np.ravel(self._weights[cluster])).std()

    def getSilhouetteScore(self, data: np.ndarray) -> float:
        """ Return silhouette score by data """
        if self._input_len != len(data[0]):
            return np.nan

        labels = convertLabelsToInt(
            [self.winner(x) for x in data],
            self.x,
            self.y
        )

        try:
            return skMetrics.silhouette_score(data, labels, metric='euclidean')
        except ValueError:
            return np.nan


    def getDaviesBouldinScore(self, data: np.ndarray) -> float:
        """ Return davies bouldin score score by data """
        if self._input_len != len(data[0]):
            return np.nan

        labels = convertLabelsToInt(
            [self.winner(x) for x in data],
            self.x,
            self.y
        )

        try:
            return skMetrics.davies_bouldin_score(data, labels)
        except ValueError:
            return np.nan

    def getCalinskiHarabaszScore(self, data: np.ndarray) -> float:
        """ Return calinski harabasz score score by data """
        if self._input_len != len(data[0]):
            return np.nan

        labels = convertLabelsToInt(
            [self.winner(x) for x in data],
            self.x,
            self.y
        )
        try:
            return skMetrics.calinski_harabasz_score(data, labels)
        except ValueError:
            return np.nan

    def getMetricFromCluster(self, metric: str, cluster: list, data: np.ndarray) -> np.ndarray:
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
        if data[cluster].shape[0] == 0:
            return np.array(np.nan)

        if np.all(np.isnan(self._weights[cluster])):
            target = np.nan_to_num(self._weights[cluster], 0.0)
        else:
            target = self._weights[cluster]

        _metric = Metrics(
            source=data[cluster].T,
            target=target
        )

        if metric == "MAE":
            return _metric.MAE() + self._weights[cluster]
        if metric == "MSE":
            return _metric.MSE() + self._weights[cluster]
        if metric == "RMSE":
            return _metric.RMSE() + self._weights[cluster]
        if metric == "QE":
            return _metric.QE() + self._weights[cluster]
        if metric == "MAPE":
            return _metric.MAPE() + self._weights[cluster]
        else:
            raise Exception("Incorrect metric")
