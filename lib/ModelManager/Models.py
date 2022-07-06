from abc import ABC, abstractmethod

import pandas as pd

from lib.util.timelib import weekdaysEN, weekday

from lib.util.som import SelfOrganizingMaps
from lib.util.regression import *
# from lib.util.mlp import * # Incompatibility with Python 3.9.0

from lib.ModelManager.errors import InvalidRegressionTypeError, InvalidModelTypeError
from lib.util.path import bar, models_rgs, models_som, models_mlp


class Model(ABC):
    extension = ""
    path = ""

    def __init__(self):
        """  """
        super().__init__()

    @abstractmethod
    def train(self, data: pd.DataFrame, parms: dict) -> any:
        """  """
        pass

    @abstractmethod
    def formatParms(self, parms: dict) -> str:
        """  """
        pass

    def formatPath(self, id: str, day: str) -> str:
        """  """
        if '_' in day:
            firstDay = day[:day.index('_')]
            day = weekdaysEN[weekday(firstDay)]
        else:
            day = weekdaysEN[weekday(day)]

        return self.path + bar + day + bar + id + self.extension


class SOM(Model):
    extension = ".som"
    path = models_som

    def train(self, data: pd.DataFrame, parms: dict) -> any:
        """  """
        return SelfOrganizingMaps(data=data, **parms)

    def formatParms(self, parms: dict) -> str:
        """  """
        dic = {}
        dic["x"] = parms['x'] if 'x' in parms else -1
        dic["y"] = parms['y'] if 'y' in parms else -1
        dic["inputlen"] = parms['inputLen'] if 'inputLen' in parms else -1
        dic["iterations"] = parms['iterations'] if 'iterations' in parms else -1
        dic["sigma"] = parms['sigma'] if 'sigma' in parms else 1.0
        dic["learningrate"] = parms['learningRate'] if 'learningRate' in parms else 0.5
        dic["neighborhoodfunction"] = parms['neighborhoodFunction'] if 'neighborhoodFunction' in parms else 'gaussian'
        dic["topology"] = parms['topology'] if 'topology' in parms else 'rectangular'
        dic["activationdistance"] = parms['activationDistance'] if 'activationDistance' in parms else 'euclidean'
        dic["weightsinit"] = parms['weightsInit'] if 'weightsInit' in parms else 'random'
        dic["randomorder"] = parms['randomOrder'] if 'randomOrder' in parms else 'randomOrder'
        dic["transpose"] = parms['transpose'] if 'transpose' in parms else True
        return dic


class RGS(Model):
    extension = ".rgs"
    path = models_rgs

    def train(self, data: pd.DataFrame, parms: dict) -> any:
        """  """
        if parms["typeRgs"] == "linear":
            model = LinearModel(data, parms['degree'])
        elif parms["typeRgs"] == "ransac":
            model = RANSAC(data, parms['degree'])
        elif parms["typeRgs"] == "rlm":
            model = RLM(data, parms['degree'])
        else:
            raise InvalidRegressionTypeError

        model.train()
        return model

    def formatParms(self, parms: dict) -> str:
        """  """
        dic = {}
        dic["deg"] = parms["degree"] if 'degree' in parms else exit()
        dic["type"] = parms["typeRgs"] if 'typeRgs' in parms else exit()
        return dic


class MLP(Model):
    extension = ".mlp"
    path = models_mlp

    def train(self, data: pd.DataFrame, parms: dict) -> any:
        """  """
        return Multilayer_perceptron(
            data,
            parms["layers"],
            parms["compile"],
            parms["fit"]
        )

    def formatParms(self, parms: dict) -> str:
        """  """
        dic = {}
        for i, layer in enumerate(parms["layers"]):
            dic.update({i: layer})
        dic.update(parms["compile"])
        dic.update(parms["fit"])
        return dic


Models = {
    "som": SOM,
    "mlp": MLP,
    "rgs": RGS
}
