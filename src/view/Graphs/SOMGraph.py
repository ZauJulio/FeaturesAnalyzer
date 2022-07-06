from itertools import product
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable


class SOMGraph:
    def plotSOM(self):
        """  """
        if self.R.ShowTest or self.R.ShowTrain:
            self.__weigthsLine()
            self.__optionsWeights()
            self.__metricsWeights()
            self.__metricsWeightsFiltered()
            self.__entrysWeights()

        self.plotActMap()
        self.plotDistMap()

    def __weigthsLine(self):
        """  """

        def __getLabel(self) -> str:
            """  """
            if self.LANGUAGE == 'en_us':
                return ' '.join(["Weigths from Cluster", str(self.somLabels.index(self.R.Cluster)+1)])
            elif self.LANGUAGE == 'pt_br':
                return ' '.join(["Vetor Sináptico do Grupo:", str(self.somLabels.index(self.R.Cluster)+1)])

        if self.thresholds["models"]["weights"]["show"] and self.R.Clusterize:
            self.ax.plot(
                self.time,
                self.getSOMWeights(),
                linestyle='-',
                color="indigo",
                label=__getLabel(self),
                linewidth=4
            )

            self.ax.legend(loc="upper left")

    def plotActMap(self):
        """  """

        def __getLabel(self) -> str:
            """  """
            if self.R.ShowTest:
                if self.LANGUAGE == 'en_us':
                    return "Activation frequency from Data Test"
                elif self.LANGUAGE == 'pt_br':
                    return "Frequência de Ativação dos Dados de Teste"
            else:
                if self.LANGUAGE == 'en_us':
                    return "Activation frequency from Data Train"
                elif self.LANGUAGE == 'pt_br':
                    return "Frequência de Ativação dos Dados de Treino"

        if self.R.showActMap:
            if len(self.fig.axes) >= 1:
                self.subplots[2] += 1

            self.ax = self.fig.add_subplot(*self.subplots)

            self.fig.colorbar(
                self.ax.imshow(
                    X=self.getActivationMap(),
                    cmap='gist_gray'
                ),
                cax=make_axes_locatable(self.ax).append_axes(
                    "right", size="6%", pad=0.2)
            )

            self.ax.xaxis.set_ticks(np.arange(0, self.R.Grid[0], 1))
            self.ax.yaxis.set_ticks(np.arange(0, self.R.Grid[1], 1))
            self.ax.set_title(__getLabel(self))

    def plotDistMap(self):
        """  """

        def __getLabel(self) -> str:
            """  """
            if self.LANGUAGE == 'en_us':
                return "Distance Map"
            elif self.LANGUAGE == 'pt_br':
                return "Mapa de Distância"

        if self.R.showDistMap:
            if len(self.fig.axes) >= 1:
                self.subplots[2] += 1

            self.ax = self.fig.add_subplot(*self.subplots)

            self.fig.colorbar(
                self.ax.imshow(
                    X=self.getDistanceMap(),
                    cmap='gist_gray',
                ),
                cax=make_axes_locatable(self.ax).append_axes(
                    "right", size="6%", pad=0.2)
            )

            self.ax.xaxis.set_ticks(np.arange(0, self.R.Grid[0], 1))
            self.ax.yaxis.set_ticks(np.arange(0, self.R.Grid[1], 1))
            self.ax.set_title(__getLabel(self))

    def __metricsWeights(self):
        """  """

        def __getLabel(self, source: str, metric: str) -> str:
            """  """
            if self.LANGUAGE == 'en_us':
                return ' '.join([metric.upper(), 'with', source.title()])
            elif self.LANGUAGE == 'pt_br':
                return ' '.join(['Pesos Sinápticos Com', metric.upper()])

        for metric in self.thrMetrics:
            if self.thresholds["metrics"]["weights"][metric]["show"]:
                self.ax.plot(
                    self.time,
                    self.getSOMThresholdFromMetric(metric),
                    linestyle="--",
                    linewidth=2,
                    label=__getLabel(self, "weights", metric),
                    color='blueviolet'
                )

    def __optionsWeights(self):
        """ Plot option(Min, Mean, Max) absolute point for threshold """

        def __getLabel(self, option: str) -> str:
            """  """
            if self.LANGUAGE == 'en_us':
                return ' '.join([option.upper(), "of Weigths"])
            elif self.LANGUAGE == 'pt_br':
                return ' '.join([option.upper(), "dos Pesos Sinápticos"])

        for option in self.thrOptions:
            if self.thresholds["models"]["weights"][option]["show"]:
                self.ax.plot(
                    self.time,
                    self.getThresholdMode(
                        option=option,
                        mode="absolute",
                        data=self.getSOMWeights()
                    ),
                    linestyle='--',
                    linewidth=2,
                    label=__getLabel(self, option)
                )

    def __metricsWeightsFiltered(self):
        """  """

        def __getLabel(self, source: str, metric: str, filter:str) -> str:
            """  """
            if self.LANGUAGE == 'en_us':
                return ' '.join([metric.upper(), 'with', filter.title(), 'and', source.title()])
            elif self.LANGUAGE == 'pt_br':
                return ' '.join(['Pesos Sinápticos Com', metric.upper(), 'e', filter.title()])

        for metric, filter in product(self.thrMetrics, self.thrFilters):
            if self.thresholds["metrics"]["weights"][metric]["filters"][filter]["show"]:
                self.ax.plot(
                    self.time,
                    self.getFilterFromCluster(metric, filter),
                    linestyle="--",
                    linewidth=2,
                    label=__getLabel(self, "weights", metric, filter),
                    color='blueviolet'
                )

    def __entrysWeights(self):
        """  """

        def __getLabel(self, metric: str, option: str, entry: str) -> str:
            """  """
            if self.LANGUAGE == 'en_us':
                return ' '.join([option.upper(), entry, "of", metric.upper(), "with the Weigths"])
            elif self.LANGUAGE == 'pt_br':
                return ' '.join([option.upper(), entry, "do", metric.upper(), "com os Pesos Sinápticos"])

        for metric, option in product(self.thrMetrics, self.thrOptions):
            if self.thresholds["metrics"]["weights"][metric][option]["show"]:
                self.ax.plot(
                    self.time,
                    self.getThresholdMode(
                        option=option,
                        mode="absolute",
                        data=self.getSOMThresholdFromMetric(metric)
                    ),
                    linestyle='--',
                    linewidth=2,
                    label=__getLabel(self, metric, option, "absolute")
                )
