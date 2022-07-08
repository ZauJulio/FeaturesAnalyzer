from lib.util import timelib
from matplotlib.lines import Line2D

from .DataGraph import DataGraph
from .ThresholdsGraph import ThresholdsGraph
from .PIDGraph import PIDGraph
from .SOMGraph import SOMGraph


class Graphs(DataGraph, ThresholdsGraph, PIDGraph, SOMGraph):

    def makePlot(self) -> None:
        """  """
        self.fig.clear()
        self.__updateNPlots()

        print("--> Plotting:...              ", end="")
        if self.R.ShowTest or self.R.ShowTrain:
            self.plotData()
            self.plotThresholds()
            self.plotTimeLimit()
            self.__updateGraphProperties()

        self.plotSOM()
        self.plotPID()
        self.__updateLegend()

        self.draw()
        self.repaint()
        print('| DONE')

    def plotTimeLimit(self):
        """  """
        ls = [axis.get_ylim() for axis in self.fig.axes]

        self.ax.plot(
            [self.time[self.timeLimit], self.time[self.timeLimit]],
            [min(min(ls)), max(max(ls))],
            '-',
            color='darkslategray'
        )

    def __updateGraphProperties(self):
        """  """
        self.__setXTicksRange()
        self.__setXYLabels()
        self.__setLegendLocation()
        self.__setTitle()

    def __updateNPlots(self) -> list:
        """  """
        self.subplots = [1, 1, 1]

        self.availablePID = self.R.PIDSample in (
            self.dataTest if self.R.ShowTest else self.dataTrain)

        if self.availablePID:
            if self.R.Derivative:
                self.subplots[0] += 1
            if self.R.Integral:
                self.subplots[0] += 1

        if self.R.showActMap:
            self.subplots[1] += 1
        if self.R.showDistMap:
            if self.subplots[1] == 2:
                self.subplots[0] += 1
            else:
                self.subplots[1] += 1

        return self.subplots

    def __setXYLabels(self):
        """  """
        if self.LANGUAGE == 'en_us':
            self.fig.axes[0].set_xlabel("Time (H:M)")
            self.fig.axes[0].set_ylabel("Potency (W)")
        elif self.LANGUAGE == 'pt_br':
            self.fig.axes[0].set_xlabel("Tempo (H:M)")
            self.fig.axes[0].set_ylabel("Potência (W)")
        else:
            raise ValueError("Unknown language")

    def __setXTicksRange(self):
        """ Set x_tick_range """
        ticks = []
        for i in range(0, len(self.time)):
            if i % 30 == 0:
                ticks.append(self.time[i])
            else:
                ticks.append('')

        ticks.append(self.time[-1])

        for i in range(len(self.fig.axes)):
            self.fig.axes[i].set_xticks(ticks)

    def __setLegendLocation(self):
        """ Set legend position """
        for i in range(len(self.fig.axes)):
            self.fig.axes[i].legend(loc="upper left")

    def __setTitle(self):
        """  """

        def dayFormatter(self):
            """  """
            if self.R.ShowSample != "All":
                label = self.R.ShowSample.split('-')
                if self.LANGUAGE == 'en_us':
                    label = " of day " + label[-1]+'/'+label[1]+'/'+label[0]
                if self.LANGUAGE == 'pt_br':
                    label = " do dia " + label[-1]+'/'+label[1]+'/'+label[0]
            else:
                if self.LANGUAGE == 'en_us':
                    label = "on " + timelib.weekdaysEN[timelib.weekday(self.R.Weekday)]
                elif self.LANGUAGE == 'pt_br':
                    label = "das " + timelib.weekdays[timelib.weekday(self.R.Weekday)]

            return label

        if self.R.Clusterize:
            if self.LANGUAGE == 'en_us':
                self.ax.set_title(
                    "Visualization of the classification %s, from group %s (%s) examples, using regression" % (
                        dayFormatter(self),
                        str(self.somLabels.index(self.R.Cluster)+1),
                        str(self.getCurrentCluster().shape[1])
                    ))
            elif self.LANGUAGE == 'pt_br':
                self.ax.set_title(
                    "Visualização da classificação %s, do grupo %s (%s) exemplos, usando regressão" % (
                        dayFormatter(self),
                        str(self.somLabels.index(self.R.Cluster)+1),
                        str(self.getCurrentCluster().shape[1])
                    ))

    def __updateLegend(self):
        """  """
        if len(self.fig.axes) == 0:
            return

        # Get current handles
        handles, _ = self.fig.axes[0].get_legend_handles_labels()

        # Handles update
        newHandles = []

        if self.R.ColorClassification:
            if self.alarmsFound:
                newHandles.append(self.__getAlarmsPath())
            if self.aboveExpectedFound:
                newHandles.append(self.__getAboveExpectedPatch())
            if self.expectedFound:
                newHandles.append(self.__getExpectedPath())
            if self.bellowExpectedFound:
                newHandles.append(self.__getBellowExpectedPath())
            if self.outliersFound:
                newHandles.append(self.__getOutliersPatch())
        else:
            if not self.R.Clusterize:
                newHandles.append(self.__getDataPatch())
        if self.samplePIDFound:
            newHandles.append(self.__getPIDPatch())

        # Update handles
        handles += newHandles

        self.fig.axes[0].legend(handles=handles, loc='upper right')

    def __getAlarmsPath(self):
        """  """
        if self.LANGUAGE == 'en_us':
            label = "Alarms"
        elif self.LANGUAGE == 'pt_br':
            label = "Alarmes"

        return Line2D(
            [0], [0],
            marker='X',
            color='w',
            label=label,
            markerfacecolor='C3',
            markersize=10
        )

    def __getAboveExpectedPatch(self):
        """  """
        if self.LANGUAGE == 'en_us':
            label = "Above expected"
        elif self.LANGUAGE == 'pt_br':
            label = "Acima do esperado"

        return Line2D(
            [0], [0],
            marker='X',
            color='w',
            label=label,
            markerfacecolor='darkgoldenrod',
            markersize=10
        )

    def __getExpectedPath(self):
        """  """
        if self.LANGUAGE == 'en_us':
            label = "Expected"
        elif self.LANGUAGE == 'pt_br':
            label = "Esperado"

        return Line2D(
            [0], [0],
            marker='X',
            color='w',
            label=label,
            markerfacecolor='C2',
            markersize=10
        )

    def __getBellowExpectedPath(self):
        """  """
        if self.LANGUAGE == 'en_us':
            label = "Below expected"
        elif self.LANGUAGE == 'pt_br':
            label = "Abaixo do esperado"

        return Line2D(
            [0], [0],
            marker='X',
            color='w',
            label=label,
            markerfacecolor='C0',
            markersize=10
        )

    def __getOutliersPatch(self):
        """  """
        return Line2D(
            [0], [0],
            marker='X',
            color='w',
            label="Outliers",
            markerfacecolor='C3',
            markersize=10
        )

    def __getPIDPatch(self):
        """  """
        def dataFormatter(sample):
            """  """
            return label[-1]+'/'+label[1]+'/'+label[0]

        if self.LANGUAGE == 'en_us':
            label = "PID Sample - "
        elif self.LANGUAGE == 'pt_br':
            label = " Amostra do PID - "

        return Line2D(
            [0], [0],
            marker='o',
            color='w',
            label=label+dataFormatter(self.R.ShowSample),
            markerfacecolor='blue',
            markersize=10
        )

    def __getDataPatch(self):
        """  """
        if self.R.ShowTest:
            if self.LANGUAGE == 'en_us':
                label = "Data Test"
            elif self.LANGUAGE == 'pt_br':
                label = "Dados de Teste"
        if self.R.ShowTrain:
            if self.LANGUAGE == 'en_us':
                label = "Data Train"
            elif self.LANGUAGE == 'pt_br':
                label = "Dados de Treino"

        return Line2D(
            [0], [0],
            marker='o',
            color='w',
            label=label,
            markerfacecolor='black',
            markersize=10
        )
