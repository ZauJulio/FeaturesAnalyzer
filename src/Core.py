import sys
import json
from copy import deepcopy

sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../../")
sys.path.append("../lib")

import pandas as pd

from view import Views
from controller import Controllers
from lib.util.path import bar

pd.plotting.register_matplotlib_converters()

CURRENT_SETTINGS_PATH = bar.join(['model', 'settings', 'current.json'])
CURRENT_THRESHOLD_PATH = bar.join(['model', 'thresholds', 'current.json'])

DEFAULT_SETTINGS_PATH = bar.join(['model', 'settings', 'default.json'])
DEFAULT_THRESHOLD_PATH = bar.join(['model', 'thresholds', 'default.json'])


class Core(Controllers, Views):
    def __init__(self, parent=None, language='en_us'):
        """  """
        self.thrFeatures = ["models", "metrics", "both"]
        self.thrSources = ['linear', 'ransac', 'rlm']
        self.thrMetrics = ['MAE', 'RMSE', 'QE', 'MAPE']
        self.thrOptions = ['min', 'mean', 'max']
        self.thrEntries = ['absolute', 'relative']

        self.thrFilters = ['savgol']
        self.LANGUAGE = language

        self.R = R()
        self.loadSettings()
        self.updateCore()

        Views.__init__(self, parent)

    def updateCore(self):
        """  """
        print("--> Updating the data:...", end="")
        self.thresholds = deepcopy(self.thresholdSettings)
        self.updateData()
        self.updateModels()
        self.updatePID()
        print('| DONE')

    def loadSettings(self) -> None:
        """ Load settings by .json """
        with open(CURRENT_SETTINGS_PATH, 'r') as settings:
            self.settings = json.load(settings)
        with open(CURRENT_THRESHOLD_PATH, 'r') as thresholds:
            self.thresholdSettings = json.load(thresholds)

        self.R.catch(self.settings)
        return self.settings

    def saveSettings(self, settings=None) -> None:
        """  """
        if settings != None:
            with open(CURRENT_SETTINGS_PATH, 'w') as file:
                if settings is None:
                    json.dump(self.settings, file)
                else:
                    json.dump(settings, file, indent=2)

        with open(CURRENT_THRESHOLD_PATH, 'w') as file:
            json.dump(self.thresholdSettings, file, indent=2)

        if settings is None:
            self.R.catch(self.settings)
        else:
            self.R.catch(settings)

        self.updateCore()

    def setDefaultSettings(self) -> None:
        """ Load default application interface settings """
        with open(DEFAULT_SETTINGS_PATH, 'r') as file:
            settings = json.load(file)

        with open(CURRENT_SETTINGS_PATH, 'w') as file:
            json.dump(settings, file, indent=2)

        with open(DEFAULT_THRESHOLD_PATH, 'r') as file:
            settings = json.load(file)

        with open(CURRENT_THRESHOLD_PATH, 'w') as file:
            json.dump(settings, file, indent=2)

        self.loadSettings()


class R(object):
    def catch(self, struct):
        """  """
        self.Weekday = struct['data']['weekday']
        self.Field = struct['data']['field']
        self.HourStart = struct['data']['hourStart']
        self.HourEnd = struct['data']['hourEnd']
        self.DateTrainStart = struct['data']['trainStart']
        self.DateTrainEnd = struct['data']['trainEnd']
        self.DateTestStart = struct['data']['testStart']
        self.DateTestEnd = struct['data']['testEnd']
        self.Transformation = struct['data']['transformation']

        self.ReplaceNaN = struct['data']['replaceNaN']
        self.DropInterval = struct['data']['dropInterval']
        self.SplitData = struct['data']['splitData']

        self.DataType = struct['data']['dataType']
        self.MobMeanMin = struct['data']['mobileMeanMinutes']
        self.MobMedianMin = struct['data']['mobileMedianMinutes']

        self.Regressions = struct['regressions']

        self.Clusterize = struct['som']['clusterize']
        self.Cluster = tuple(struct['som']['cluster'])
        self.Grid = struct['som']['grid']
        self.showActMap = struct['som']['showActMap']
        self.showDistMap = struct['som']['showDistMap']
        self.diffClusters = struct['som']['diffClusters']

        self.Derivative = struct['pid']['derivative']
        self.Integral = struct['pid']['integral']
        self.PIDSample = struct['pid']['sample']
        self.FillBetween = struct['pid']['fillBetween']
        self.IntegralParameters = struct['pid']['showIntegralParameters']

        self.ShowSample = struct['show']['data']
        self.MediumLine = struct['show']['mediumLine']
        self.ShowTrain = struct['show']['train']
        self.ShowTest = struct['show']['test']
        self.ColorClassification = struct['show']['ColorClassification']
        self.TimeLimit = struct['show']['TimeLimit']


if __name__ == "__main__":
    Core().setDefaultSettings()
