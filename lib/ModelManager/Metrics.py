from abc import ABC, abstractmethod

import pandas as pd
from lib.util.som import SelfOrganizingMaps
import numpy as np


class Metric(ABC):
    metrics = {}

    def __init__(self):
        super().__init__()

    @abstractmethod
    def collect(model, data: np.ndarray):
        pass


class SOM(Metric):

    def __init__(self, uuid: str):
        self.metrics = {
            "uuid": uuid,
            "samples": [],
            "dotproductmean": [],
            "dotproductvar": [],
            "dotproductstd": [],
            "variancemean": [],
            "clustermean": [],
            "stdmean": [],
            "qemean": [],
            "rmsemean": [],
            "maemean": [],
            "silhouettescore": int,
            "daviesbouldinscore": int,
            "calinskiharabaszscore": int,
        }

        super().__init__()
    
    @staticmethod
    def getClusters(model: SelfOrganizingMaps, data: np.ndarray):
        """  """
        clusters = model.clusterize(data)
        for key in clusters.keys():
            clusters[key] = clusters[key].drop(
                ['weights', 'hora'], errors='ignore', axis=1).T.values
        
        return clusters

    def collect(self, model: SelfOrganizingMaps, data: np.ndarray):
        """  """
        clusters = self.getClusters(model, data)

        for cluster in model.getKeys():
            self.metrics["dotproductmean"].append(
                model.getDotProductFromCluster(clusters, cluster))
            self.metrics["dotproductvar"].append(
                model.getDotProductVarianceFromCluster(clusters, cluster))
            self.metrics["dotproductstd"].append(
                model.getDotProductStdFromCluster(clusters, cluster))
            self.metrics["variancemean"].append(
                model.getVarianceFromCluster(clusters, cluster))
            self.metrics["clustermean"].append(
                model.getMeanFromCluster(clusters, cluster))
            self.metrics["stdmean"].append(
                model.getStdFromCluster(clusters, cluster))
            self.metrics["qemean"].append(
                np.nan_to_num(x=model.getQeFromCluster(clusters, cluster), nan=-1))
            self.metrics["rmsemean"].append(
                np.nan_to_num(x=model.getMetricFromCluster("RMSE", cluster, clusters).mean(), nan=-1.0))
            self.metrics["maemean"].append(
                np.nan_to_num(x=model.getMetricFromCluster("MAE", cluster, clusters).mean(), nan=-1.0))
        
        self.metrics["silhouettescore"] = model.getSilhouetteScore(data.values)
        self.metrics["daviesbouldinscore"] = model.getDaviesBouldinScore(data.values)
        self.metrics["calinskiharabaszscore"] = model.getCalinskiHarabaszScore(data.values)

        self.metrics["samples"] = np.array([
            len(clusters[cluster]) for cluster in model.getKeys()
        ])

        for key in self.metrics.keys():
            if type(self.metrics[key]) is list:
                self.metrics[key] = np.array(
                    self.metrics[key], dtype=np.float16)

        return self.metrics


Metrics = {
    "som": SOM,
}
