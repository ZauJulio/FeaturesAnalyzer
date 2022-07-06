import numpy as np
from itertools import product


class ThresholdsGraph:

    def plotThresholds(self):
        """  """
        self.__models()
        self.__optionsModels()
        self.__allMetricsOptions()
        self.__allSourcesOptions()

        self.__metrics()
        self.__metricsFiltered()
        self.__optionsMetric()
        self.__allMetricsSourcesOptions()

        self.__allOptions()

        self.__bothEntrys()

    def __getModelTitle(self, source: str) -> str:
        """  """
        source = source.lower()

        if source == "linear":
            return "Linear"
        if source == "ransac":
            return "RANSAC"
        if source == "rlm":
            return "RLM"
        else:
            raise "Regression source incorrect"

    def __models(self):
        """ Plot simple predicted data model """

        def __getLabel(self, source: str) -> str:
            """  """
            if self.LANGUAGE == 'en_us':
                return ' '.join([self.__getModelTitle(source), "Regression"])
            elif self.LANGUAGE == 'pt_br':
                return ' '.join(["Regressão", self.__getModelTitle(source)])

        def __getColor(option: str) -> str:
            """  """
            if option == "linear":
                return "blue"
            if option == "ransac":
                return "lime"
            if option == "rlm":
                return "darkorange"
            if option == "all":
                return "crimson"

        for source in self.thrSources:
            if self.thresholds["models"][source]["show"]:
                self.ax.plot(
                    self.time,
                    self.getRegressionTarget(source),
                    '-',
                    linewidth=4,
                    color=__getColor(source),
                    label=__getLabel(self, source)
                )

    def __metrics(self):
        """ Plot single data metric for model """

        def __getLabel(self, source: str, metric: str) -> str:
            """  """
            if self.LANGUAGE == 'en_us':
                return ' '.join([self.__getModelTitle(source), "with", metric.upper()])
            elif self.LANGUAGE == 'pt_br':
                return ' '.join([self.__getModelTitle(source), "com", metric.upper()])

        def __getColor(source: str) -> str:
            """  """
            if source == "linear":
                return "blue"
            if source == "ransac":
                return "lime"
            if source == "rlm":
                return "darkorange"
            if source == "all":
                return "crimson"

        def __getLineStyle(metric: str) -> str:
            """  """
            if metric == "MAE":
                return "--"
            if metric == "RMSE":
                return "-."
            if metric == "QE":
                return ":"
            if metric == "MAPE":
                return "-"

        for source, metric in product(self.thrSources, self.thrMetrics):
            if self.thresholds["metrics"][source][metric]["show"]:
                self.ax.plot(
                    self.time,
                    self.getRegressionThreshold(source, metric),
                    linestyle=__getLineStyle(metric),
                    linewidth=2,
                    label=__getLabel(self, source, metric),
                    color=__getColor(source)
                )

    def __optionsModels(self):
        """ Plot option(Min, Mean, Max) absolute point for threshold """

        def __getLabel(self, source: str, metric: str) -> str:
            """  """
            if self.LANGUAGE == 'en_us':
                return ' '.join([
                    metric.upper(),
                    "of",
                    self.__getModelTitle(source),
                    "regression"
                ])
            elif self.LANGUAGE == 'pt_br':
                return ' '.join([
                    metric.upper(),
                    "da Regressão",
                    self.__getModelTitle(source),
                ])

        iterator = product(self.thrSources, self.thrOptions)
        for source, option in iterator:
            if self.thresholds["models"][source][option]["show"]:
                self.ax.plot(
                    self.time,
                    self.getThresholdMode(
                        option=option,
                        mode="absolute",
                        data=self.getRegressionTarget(source)
                    ),
                    linestyle='--',
                    linewidth=2,
                    label=__getLabel(self, source, option)
                )

    def __optionsMetric(self) -> None:
        """ Plot option(Min, Mean, Max) absolute point for metric """

        def __getLabel(self, source: str, metric: str, option: str) -> str:
            """  """
            return ' '.join([option.title(), "of Regs. Viewd"])

        for source, metric, option in product(self.thrSources, self.thrMetrics, self.thrOptions):
            if self.thresholds["metrics"][source][metric][option]["show"]:
                self.ax.plot(
                    self.time,
                    self.getThresholdMode(
                        option=option,
                        mode="absolute",
                        data=self.getRegressionThreshold(source, metric)
                    ),
                    linestyle=(0, (3, 10, 1, 10)),
                    linewidth=3,
                    label=__getLabel(self, source, metric, option)
                )

    def __allOptions(self):
        """ Plot option(Min, Mean, Max) for all thresholds without metric """

        def __getLabel(self, option: str) -> str:
            """  """
            if self.LANGUAGE == 'en_us':
                return ' '.join([option.title(), "of Regs. Viewd"])
            elif self.LANGUAGE == 'pt_br':
                return ' '.join([option.title(), "das Regs. Visualizadas"])

        iterator = product(self.thrOptions, self.thrEntries)
        for option, entrie in iterator:
            if self.thresholds["models"]["all"][option][entrie]["show"]:
                self.ax.plot(
                    self.time,
                    self.getModelOptionsForAll(option, entrie),
                    linestyle='--',
                    linewidth=2,
                    label=__getLabel(self, option)
                )

    def __allMetricsOptions(self) -> None:
        """ Plot option(Min, Mean, Max) for all metric """

        def __getLabel(self, option: str, entrie:str, source: str) -> str:
            """  """
            if self.LANGUAGE == 'en_us':
                return ' '.join([option.title(), entrie.title(), "of Metrics model", self.__getModelTitle(source)])
            elif self.LANGUAGE == 'pt_br':
                return ' '.join([option.title(), entrie.title(), "das Métricas do modelo", self.__getModelTitle(source)])

        def __getColor(option: str) -> str:
            """  """
            if option == "min":
                return "aqua"
            if option == "mean":
                return "yellowgreen"
            if option == "max":
                return "brown"

        iterator = product(self.thrSources, self.thrOptions, self.thrEntries)
        for source, option, entrie in iterator:
            if self.thresholds["metrics"][source]["all"][option][entrie]["show"]:
                self.ax.plot(
                    self.time,
                    self.getRegressionsMetricsFromSource(source, option, entrie),
                    linestyle='-.',
                    linewidth=5,
                    label=__getLabel(self, option, entrie, source),
                    color=__getColor(option)
                )

    def __allSourcesOptions(self) -> None:
        """ Plot option(Min, Mean, Max) for all models with metric """

        def __getLabel(self, option: str, metric: str) -> str:
            """  """
            if self.LANGUAGE == 'en_us':
                return ' '.join([option.title(), "of", metric, "of All Models Viewed"])
            elif self.LANGUAGE == 'pt_br':
                return ' '.join([option.title(), "de", metric, "de Todos os Modelos Visualizados"])
        
        def __getColor(option: str) -> str:
            """  """
            if option == "min":
                return "aqua"
            if option == "mean":
                return "yellowgreen"
            if option == "max":
                return "brown"
        
        iterator = product(self.thrMetrics, self.thrOptions, self.thrEntries)
        for metric, option, entrie in iterator:
            if self.thresholds["metrics"]['all'][metric][option][entrie]["show"]:
                self.ax.plot(
                    self.time,
                    self.getModelMetricsForAll(metric, option, entrie, onlyDisplayed=True),
                    linestyle=':',
                    linewidth=4,
                    color=__getColor(option),
                    label=__getLabel(self, option, metric)
                )

    def __allMetricsSourcesOptions(self) -> None:
        """ Plot option(Min, Mean, Max) for all models with metric """

        def __getLabel(self, option: str) -> str:
            """  """
            if self.LANGUAGE == 'en_us':
                return ' '.join([option.title(), "of All Thresholds Viewed"])
            elif self.LANGUAGE == 'pt_br':
                return ' '.join([option.title(), "de Todos Os Thresholds"])

        for option, entrie in product(self.thrOptions, self.thrEntries):
            if self.thresholds["metrics"]['all']['all'][option][entrie]["show"]:
                self.ax.plot(
                    self.time,
                    self.getAllOptionsFromRegressions(option, entrie),
                    linestyle=(0, (3, 10, 1, 10)),
                    linewidth=3,
                    label=__getLabel(self, option)
                )

    def __bothEntrys(self):
        """  """

        def __getLabel(self, option: str, entrie: str) -> str:
            """  """
            if self.LANGUAGE == 'en_us':
                return ' '.join([option.title(), entrie])
            elif self.LANGUAGE == 'pt_br':
                if entrie == "absolute":
                    return ' '.join([option.title(), "absoluto"])
                else:
                    return ' '.join([option.title(), "local"])

        def __getColor(option: str) -> str:
            """  """
            if option == "min":
                return "lime"
            if option == "mean":
                return "orange"
            if option == "max":
                return "red"

        for option, entrie in product(self.thrOptions, self.thrEntries):
            if self.thresholds["both"][option][entrie]["show"]:
                self.ax.plot(
                    self.time,
                    self.getBothThresholds(option, entrie),
                    linestyle="dashdot",
                    linewidth=2.5,
                    color=__getColor(option),
                    label=__getLabel(self, option, entrie)
                )

    def __metricsFiltered(self):
        """ Plot single data metric for model """

        def __getLabel(self, source: str, metric: str, filter: str) -> str:
            """  """
            if self.LANGUAGE == 'en_us':
                return ' '.join([self.__getModelTitle(source), "with", filter.title(), 'and', metric.upper()])
            elif self.LANGUAGE == 'pt_br':
                return ' '.join([self.__getModelTitle(source), "com", filter.title(), 'e', metric.upper()])

        def __getColor(source: str) -> str:
            """  """
            if source == "linear":
                return "blue"
            if source == "ransac":
                return "lime"
            if source == "rlm":
                return "darkorange"
            if source == "all":
                return "crimson"

        def __getLineStyle(metric: str) -> str:
            """  """
            if metric == "MAE":
                return "--"
            if metric == "RMSE":
                return "-."
            if metric == "QE":
                return ":"
            if metric == "MAPE":
                return "-"

        for source, metric, filter in product(self.thrSources, self.thrMetrics, self.thrFilters):
            if self.thresholds["metrics"][source][metric]["filters"][filter]["show"]:
                self.ax.plot(
                    self.time,
                    self.getFilterFromMetric(source, metric, filter),
                    linestyle=__getLineStyle(metric),
                    linewidth=2,
                    label=__getLabel(self, source, metric, filter),
                    color=__getColor(source)
                )
