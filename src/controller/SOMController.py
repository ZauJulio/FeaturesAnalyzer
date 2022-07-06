import sys

import pandas as pd
import numpy as np

sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../../")
sys.path.append("../../lib/")

from lib.util.numlib import dot
from lib.ModelManager import ModelManager

class SOMController:
    def loadClusterizer(self):
        """ Start and train the cluster model

        Generates a model based on training data with the following parameters:

            input_len             = -1
            num_iteration         = 100000
            sigma                 = 1.0
            learning_rate         = 0.5
            neighborhood_function = 'gaussian'
            topology              = 'rectangular'
            activation_distance   = 'euclidean'
            weights_init          = "random"
            random_order          = False

        Returns
        -------
        None

        """
        period = self.getPeriod('train')

        startDate = period[0][0]
        endDate = period[1][1]

        startDateDrop = period[0][1]
        endDateDrop = period[1][0]

        model = ModelManager(
            day=self.getWeekday(),
            field=self.R.Field,
            ffill=self.R.ReplaceNaN,
            bfill=self.R.ReplaceNaN,
            transform=self.R.Transformation
        )

        # Filter Data in datetime
        model.filter(
            startTime=self.R.HourStart,
            endTime=self.R.HourEnd,
            startDate=startDate,
            endDate=endDate,
            inplace=True
        )

        # Drop custom date interval
        if self.R.DropInterval:
            model.drop(
                startDate=startDateDrop,
                endDate=endDateDrop,
                inplace=True
            )

        model.getDataMode(mode=self.R.DataType)

        # Create and train model of Self-Organizing Maps
        self.modelSOM = model.create(
            typ="som",
            x=-1 if self.R.Grid[0] is None else self.R.Grid[0],
            y=-1 if self.R.Grid[1] is None else self.R.Grid[1],
            inputLen=-1,
            iterations=100000,
            sigma=1.0 if self.R.Grid[0] > 1 else 0.5,
            learningRate=0.5,
            neighborhoodFunction='gaussian',
            topology='rectangular',
            activationDistance='euclidean',
            weightsInit="random",
            randomOrder=True,
        )

        self.setSOMLabels()

        # Apply custom transformations in training data
        return self.getDataMode(data=model.getDf())

    def clusterize(self, data: pd.DataFrame):
        """ Data clustering

        Exposes samples to the clusters to map neuron activations
        and activation.

        Parameters
        ----------
            data: pd.DataFrame
                Dataframe data for clustering
            inplace: bool
                Replace current data
            getClusters: bool
                return all current clusters

        Notes
        -----
            They are presented to the
            cluster, where the same training distance is used to calculate
            the BMU (Best Match Unit) for the sample. Soon after, a dictionary
            is generated with tuple keys, based on the coordinates (X, Y) of
            the neuron BMU.
        """

        # Replace NaN
        data = data.ffill().bfill()

        # Clusterize
        clusters = self.modelSOM.clusterize(data=data.T)

        # Revert hour to index
        for key in clusters.keys():
            clusters[key].reset_index(level=0, inplace=True)

        return clusters

    def setSOMLabels(self):
        """ Set SOM labels list """
        self.somLabels = []

        for i in range(self.R.Grid[0]):
            for j in range(self.R.Grid[1]):
                self.somLabels.append((i, j))

    def getActivationMap(self):
        """ Return activation map from data """
        data = self.getData()
        data = data.drop(['weights', 'hora'], errors='ignore', axis=1)
        return self.modelSOM.activation_response(data.values.T)

    def getDistanceMap(self):
        """ Return current distance map from trained model """
        return self.modelSOM.distance_map()

    def getClusters(self) -> dict:
        """ Get clusters in state

        Returns
        -------
            dict with, coordinates from cluster in map, in key
            of dict.
            Ex.:
                { (0,0): [...], (0,1): [...] }
        """
        return self.clusters

    def getCurrentCluster(self, dropWeights: bool = False, dropTime: bool = False):
        """  """
        cluster = self.testClusters[self.R.Cluster]
        
        if dropWeights:
            cluster = cluster.drop(['weights'], errors='ignore', axis=1)
        if dropTime:
            cluster = cluster.drop(['hora'], errors='ignore', axis=1)

        return cluster

    def getVarianceFromCluster(self) -> float:
        """ Return mean of variance of current cluster"""
        return np.var(
            self.getCurrentCluster(dropWeights=True, dropTime=True).to_numpy(),
            axis=1
        ).mean()

    def getMeanFromCluster(self) -> float:
        """ Return absolute mean of the current cluster"""
        return np.mean(
            self.getCurrentCluster(dropWeights=True, dropTime=True).to_numpy(),
            axis=1
        ).mean()

    def getStdFromCluster(self) -> float:
        """ Return mean of standard deviation of current cluster"""
        return np.std(
            self.getCurrentCluster(dropWeights=True, dropTime=True).to_numpy(),
            axis=1
        ).mean()

    def getQeFromCluster(self) -> float:
        """ Return mean of quantization_error from current cluster"""
        return self.modelSOM.quantization_error(
            self.getCurrentCluster(dropWeights=True, dropTime=True).T.to_numpy()
        )

    def getSOMWeights(self):
        """ Return current cluster weights """
        return self.getCurrentCluster()['weights']

    def getDotProductFromCluster(self) -> float:
        """ Return dot product of current cluster"""
        return np.mean(dot(
            self.getCurrentCluster(dropWeights=True, dropTime=True).T.values,
            np.ravel(self.getSOMWeights())
        ))
