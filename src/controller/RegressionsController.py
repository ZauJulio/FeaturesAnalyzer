from lib.util import regression

REGRESSIONS = {
    "linear": regression.LinearModel,
    "ransac": regression.RANSAC,
    "rlm": regression.RLM
}


class RegressionsController:
    def updateModels(self) -> None:
        """ loads the regression models """
        trainData = self.__getTrainData()

        for source in self.thrSources:
            if self.R.Regressions[source]:
                model = REGRESSIONS[source](
                    source=trainData,
                    deg=self.__getDegree(source),
                    metrics_data=self.metricData
                )
                
                model.train()
                self.R.Regressions[source] = model

    def __getTrainData(self):
        """ Return train data """
        if self.R.Clusterize:
            return self.trainClusters[self.R.Cluster].set_index('hora', drop=True)
        else:
            return self.dataTrain

    def __getDegree(self, source: str) -> int:
        """ Return degree from source regression """
        return int(self.settings['regressions'][source + 'Degree'])
