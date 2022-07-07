from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib

from .DataComponent import DataComponent
from .PIDComponent import PIDComponent
from .RegressionsComponent import RegressionsComponent
from .SOMComponent import SOMComponent
from .ShowComponent import ShowComponent
from .ThresholdsComponent import ThresholdsComponent

matplotlib.use('agg')
_TRANSLATE = QtCore.QCoreApplication.translate


class Interface(FigureCanvasQTAgg, DataComponent, RegressionsComponent,
                ThresholdsComponent, SOMComponent, PIDComponent,
                ShowComponent):
    def __init__(self, parent):
        """  """
        self.fig = Figure(tight_layout=True)

        FigureCanvasQTAgg.__init__(self, self.fig)
        FigureCanvasQTAgg.updateGeometry(self)

        self.setParent(parent)
        self.setObjectName("parent")
        self.setWindowTitle(QtCore.QCoreApplication.translate("Parent", "Features Analyzer"))
        self.settings_box()
        self.settings_layout()
        self.master_layout(parent)
        self.translateUI()

        self.connectViewsWidgets()
        self.preloadViewsEntrys()

    def settings_box(self):
        """  """
        self.settingsBox = QtWidgets.QWidget()
        self.settingsBox.setObjectName("settingsBox")
        self.settingsBox.setContentsMargins(10, 10, 10, 10)
        self.settingsBox.setMaximumSize(QtCore.QSize(440, 16777215))

        DataComponent.__init__(self, self.settingsBox)
        RegressionsComponent.__init__(self, self.settingsBox)
        ThresholdsComponent.__init__(self, self.settingsBox)
        PIDComponent.__init__(self, self.settingsBox)
        SOMComponent.__init__(self, self.settingsBox)
        ShowComponent.__init__(self, self.settingsBox)

    def translateUI(self):
        """  """
        self.retranslateUi()
        self.retranslateDataComponent()
        self.retranslateRegressionsComponent()
        self.retranslateThresholdsComponent()
        self.retranslateSOMComponent()
        self.retranslateShowComponent()
        self.retranslatePIDComponent()

    def connectViewsWidgets(self):
        """  """
        self.connectWidgetsData()
        self.connectWidgetsRegressions()
        self.connectWidgetsThresholds()
        self.connectWidgetsSOM()
        self.connectWidgetsPID()

    def preloadViewsEntrys(self):
        """  """
        self.preloadEntrysData()
        self.preloadEntrysRegressions()
        self.preloadEntrysSOM()
        self.preloadEntrysShow()
        self.preloadEntrysPID()
        self.makePlot()

    def setDefaultSettingsUpdate(self):
        self.setDefaultSettings()
        self.preloadViewsEntrys()
        self.makePlot()

    def settings_layout(self):
        """  """
        self.settingsLayout = QtWidgets.QGridLayout(self.settingsBox)

        self.defaultSetButton = QtWidgets.QPushButton(self.settingsBox)
        self.defaultSetButton.setObjectName("defaultSetButton")
        self.defaultSetButton.clicked.connect(self.setDefaultSettingsUpdate)

        spacerItemStart = QtWidgets.QSpacerItem(
            7, 7, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        spacerItemData = QtWidgets.QSpacerItem(
            19, 19, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        spacerItemRegressons = QtWidgets.QSpacerItem(
            19, 19, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        spacerItemThresholds = QtWidgets.QSpacerItem(
            19, 19, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        spacerItemSom = QtWidgets.QSpacerItem(
            19, 19, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        spacerItemPID = QtWidgets.QSpacerItem(
            19, 19, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        spacerItemShow = QtWidgets.QSpacerItem(
            19, 19, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        self.settingsLayout.addItem(spacerItemStart, 0, 0, 1, 1)
        self.settingsLayout.addWidget(self.dataBox, 1, 0, 1, 1)
        self.settingsLayout.addItem(spacerItemData, 2, 0, 1, 1)
        self.settingsLayout.addWidget(self.regressionsBox, 3, 0, 1, 1)
        self.settingsLayout.addItem(spacerItemRegressons, 4, 0, 1, 1)
        self.settingsLayout.addWidget(self.thresholdBox, 5, 0, 1, 1)
        self.settingsLayout.addItem(spacerItemThresholds, 6, 0, 1, 1)
        self.settingsLayout.addWidget(self.somBox, 7, 0, 1, 1)
        self.settingsLayout.addItem(spacerItemSom, 8, 0, 1, 1)
        self.settingsLayout.addWidget(self.pidBox, 9, 0, 1, 1)
        self.settingsLayout.addItem(spacerItemPID, 10, 0, 1, 1)
        self.settingsLayout.addWidget(self.showBox, 11, 0, 1, 1)
        self.settingsLayout.addItem(spacerItemShow, 12, 0, 1, 1)
        self.settingsLayout.addWidget(self.defaultSetButton, 13, 0, 1, 1)

        self.settingsLayout.setObjectName("settingsLayout")

    def master_layout(self, parent):
        """  """
        self.scrollArea = QtWidgets.QScrollArea(parent)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setWidget(self.settingsBox)
        self.scrollArea.setMaximumSize(QtCore.QSize(440, 16777215))
        self.scrollArea.setContentsMargins(9, 9, 9, 9)

        self.navigationBar = NavigationToolbar2QT(self, None)

        self.masterLayout = QtWidgets.QGridLayout(parent)
        self.masterLayout.setSpacing(0)
        self.masterLayout.setContentsMargins(0, 0, 0, 0)

        self.masterLayout.addWidget(self.scrollArea, 0, 0, 2, 1)
        self.masterLayout.addWidget(self, 0, 1)
        self.masterLayout.addWidget(self.navigationBar, 1, 1)
        self.masterLayout.setObjectName("masterLayout")

    def retranslateUi(self):

        if self.LANGUAGE == 'pt_br':
            self.dataBox.setTitle(_TRANSLATE("Parent", "Gerenciar Dados"))
            self.regressionsBox.setTitle(_TRANSLATE("Parent", "Regressões"))
            self.thresholdBox.setTitle(_TRANSLATE("Parent", "Limiares"))
            self.somBox.setTitle(_TRANSLATE(
                "Parent", "Mapa Auto-organizável(Kohonen)"))
            self.pidBox.setTitle(_TRANSLATE(
                "Parent", "Controlador Proporcional Integral Derivativo"))
            self.showBox.setTitle(_TRANSLATE("Parent", "Visualizar"))
            self.defaultSetButton.setText(
                _TRANSLATE("Parent", "Configurações Padrão"))

        if self.LANGUAGE == 'en_us':
            self.dataBox.setTitle(_TRANSLATE("Parent", "Data"))
            self.regressionsBox.setTitle(_TRANSLATE("Parent", "Regressions"))
            self.thresholdBox.setTitle(_TRANSLATE("Parent", "Thresholds"))
            self.somBox.setTitle(_TRANSLATE("Parent", "Self-Organizing Maps"))
            self.pidBox.setTitle(_TRANSLATE("Parent", "PID Controller"))
            self.showBox.setTitle(_TRANSLATE("Parent", "Show"))
            self.defaultSetButton.setText(
                _TRANSLATE("Parent", "Default Settings"))

    def retranslateDataComponent(self):

        if self.LANGUAGE == "pt_br":
            self.weekdayLabel.setText(_TRANSLATE("Parent", "Dia"))

            self.weekdayComboBox.setItemText(
                0, _TRANSLATE("Parent", "Segunda-feira"))
            self.weekdayComboBox.setItemText(
                1, _TRANSLATE("Parent", "Terça-feira"))
            self.weekdayComboBox.setItemText(
                2, _TRANSLATE("Parent", "Quarta-feira"))
            self.weekdayComboBox.setItemText(
                3, _TRANSLATE("Parent", "Quinta-feira"))
            self.weekdayComboBox.setItemText(
                4, _TRANSLATE("Parent", "Sexta-feira"))
            self.weekdayComboBox.setItemText(
                5, _TRANSLATE("Parent", "Sábado"))
            self.weekdayComboBox.setItemText(
                6, _TRANSLATE("Parent", "Domingo"))
            self.weekdayComboBox.setItemText(
                7, _TRANSLATE("Parent", "Todos"))

            self.fieldLabel.setText(_TRANSLATE("Parent", "Entrada"))

            self.fieldComboBox.setItemText(0, _TRANSLATE("Parent", "P1"))
            self.fieldComboBox.setItemText(1, _TRANSLATE("Parent", "P2"))
            self.fieldComboBox.setItemText(2, _TRANSLATE("Parent", "P3"))
            self.fieldComboBox.setItemText(3, _TRANSLATE("Parent", "Q1"))
            self.fieldComboBox.setItemText(4, _TRANSLATE("Parent", "Q2"))
            self.fieldComboBox.setItemText(5, _TRANSLATE("Parent", "Q3"))
            self.fieldComboBox.setItemText(6, _TRANSLATE("Parent", "FPA"))
            self.fieldComboBox.setItemText(7, _TRANSLATE("Parent", "FPB"))
            self.fieldComboBox.setItemText(8, _TRANSLATE("Parent", "FPC"))

            self.trainStartEndLabel.setText(
                _TRANSLATE("Parent", "Treino Início/Fim"))
            self.testStartEndLabel.setText(
                _TRANSLATE("Parent", "Teste  Início/Fim"))
            self.hourLabel.setText(
                _TRANSLATE("Parent", "Horário Início/Fim"))

            self.testStartComboBox.setItemText(
                0, _TRANSLATE("Parent", "2018.1"))
            self.testStartComboBox.setItemText(
                1, _TRANSLATE("Parent", "2018.2"))
            self.testStartComboBox.setItemText(
                2, _TRANSLATE("Parent", "2019.1"))
            self.testStartComboBox.setItemText(
                3, _TRANSLATE("Parent", "2019.2"))

            self.testEndComboBox.setItemText(
                0, _TRANSLATE("Parent", "2018.1"))
            self.testEndComboBox.setItemText(
                1, _TRANSLATE("Parent", "2018.2"))
            self.testEndComboBox.setItemText(
                2, _TRANSLATE("Parent", "2019.1"))
            self.testEndComboBox.setItemText(
                3, _TRANSLATE("Parent", "2019.2"))

            self.dropIntervalButton.setText(_TRANSLATE(
                "Parent", "Selecionar Périodo Letivo"))

            self.trainStartComboBox.setItemText(
                0, _TRANSLATE("Parent", "2018.1"))
            self.trainStartComboBox.setItemText(
                1, _TRANSLATE("Parent", "2018.2"))
            self.trainStartComboBox.setItemText(
                2, _TRANSLATE("Parent", "2019.1"))
            self.trainStartComboBox.setItemText(
                3, _TRANSLATE("Parent", "2019.2"))

            self.trainEndComboBox.setItemText(
                0, _TRANSLATE("Parent", "2018.1"))
            self.trainEndComboBox.setItemText(
                1, _TRANSLATE("Parent", "2018.2"))
            self.trainEndComboBox.setItemText(
                2, _TRANSLATE("Parent", "2019.1"))
            self.trainEndComboBox.setItemText(
                3, _TRANSLATE("Parent", "2019.2"))

            self.defaultRadio.setText(
                _TRANSLATE("Parent", "Original"))
            self.trainingDataButton.setText(
                _TRANSLATE("Parent", "Dividir Treino e Teste"))
            self.meanRadio.setText(
                _TRANSLATE("Parent", "Média"))
            self.mobMeanRadio.setText(
                _TRANSLATE("Parent", "Média Móvel"))
            self.mobMedianRadio.setText(
                _TRANSLATE("Parent", "Mediana Móvel"))
            self.fillnaButton.setText(
                _TRANSLATE("Parent", "Substituir NaN"))
            self.transformationsLabel.setText(
                _TRANSLATE("Parent", "Transformações"))

            self.advancedData.setText("Visualizar mais opções...")
            self.windowLabel.setText("Janela")
            self.transformationsComboBox.setItemText(
                0, _TRANSLATE("Parent", "Nenhuma"))

        if self.LANGUAGE == "en_us":
            self.weekdayLabel.setText(_TRANSLATE("Parent", "Weekday"))

            self.weekdayComboBox.setItemText(
                0, _TRANSLATE("Parent", "Monday"))
            self.weekdayComboBox.setItemText(
                1, _TRANSLATE("Parent", "Tuesday"))
            self.weekdayComboBox.setItemText(
                2, _TRANSLATE("Parent", "Wednesday"))
            self.weekdayComboBox.setItemText(
                3, _TRANSLATE("Parent", "Thursday"))
            self.weekdayComboBox.setItemText(
                4, _TRANSLATE("Parent", "Friday"))
            self.weekdayComboBox.setItemText(
                5, _TRANSLATE("Parent", "Saturday"))
            self.weekdayComboBox.setItemText(
                6, _TRANSLATE("Parent", "Sunday"))
            self.weekdayComboBox.setItemText(
                7, _TRANSLATE("Parent", "All"))

            self.fieldLabel.setText(_TRANSLATE("Parent", "Field"))

            self.fieldComboBox.setItemText(0, _TRANSLATE("Parent", "P1"))
            self.fieldComboBox.setItemText(1, _TRANSLATE("Parent", "P2"))
            self.fieldComboBox.setItemText(2, _TRANSLATE("Parent", "P3"))
            self.fieldComboBox.setItemText(3, _TRANSLATE("Parent", "Q1"))
            self.fieldComboBox.setItemText(4, _TRANSLATE("Parent", "Q2"))
            self.fieldComboBox.setItemText(5, _TRANSLATE("Parent", "Q3"))
            self.fieldComboBox.setItemText(6, _TRANSLATE("Parent", "FPA"))
            self.fieldComboBox.setItemText(7, _TRANSLATE("Parent", "FPB"))
            self.fieldComboBox.setItemText(8, _TRANSLATE("Parent", "FPC"))

            self.trainStartEndLabel.setText(
                _TRANSLATE("Parent", "Train Start/End"))
            self.testStartEndLabel.setText(
                _TRANSLATE("Parent", "Test  Start/End"))
            self.hourLabel.setText(
                _TRANSLATE("Parent", "Hour Start/End"))

            self.testStartComboBox.setItemText(
                0, _TRANSLATE("Parent", "2018.1"))
            self.testStartComboBox.setItemText(
                1, _TRANSLATE("Parent", "2018.2"))
            self.testStartComboBox.setItemText(
                2, _TRANSLATE("Parent", "2019.1"))
            self.testStartComboBox.setItemText(
                3, _TRANSLATE("Parent", "2019.2"))

            self.testEndComboBox.setItemText(
                0, _TRANSLATE("Parent", "2018.1"))
            self.testEndComboBox.setItemText(
                1, _TRANSLATE("Parent", "2018.2"))
            self.testEndComboBox.setItemText(
                2, _TRANSLATE("Parent", "2019.1"))
            self.testEndComboBox.setItemText(
                3, _TRANSLATE("Parent", "2019.2"))

            self.dropIntervalButton.setText(
                _TRANSLATE("Parent", "Drop Interval"))

            self.trainStartComboBox.setItemText(
                0, _TRANSLATE("Parent", "2018.1"))
            self.trainStartComboBox.setItemText(
                1, _TRANSLATE("Parent", "2018.2"))
            self.trainStartComboBox.setItemText(
                2, _TRANSLATE("Parent", "2019.1"))
            self.trainStartComboBox.setItemText(
                3, _TRANSLATE("Parent", "2019.2"))

            self.trainEndComboBox.setItemText(
                0, _TRANSLATE("Parent", "2018.1"))
            self.trainEndComboBox.setItemText(
                1, _TRANSLATE("Parent", "2018.2"))
            self.trainEndComboBox.setItemText(
                2, _TRANSLATE("Parent", "2019.1"))
            self.trainEndComboBox.setItemText(
                3, _TRANSLATE("Parent", "2019.2"))

            self.defaultRadio.setText(
                _TRANSLATE("Parent", "Default"))
            self.trainingDataButton.setText(
                _TRANSLATE("Parent", "Split Data"))
            self.meanRadio.setText(
                _TRANSLATE("Parent", "Mean"))
            self.mobMeanRadio.setText(
                _TRANSLATE("Parent", "Mobile Mean"))
            self.mobMedianRadio.setText(
                _TRANSLATE("Parent", "Mobile Median"))
            self.fillnaButton.setText(
                _TRANSLATE("Parent", "Replace NaN"))
            self.transformationsLabel.setText(
                _TRANSLATE("Parent", "Transformations"))

            self.advancedData.setText("Show More Options")
            self.windowLabel.setText("Window")
            self.transformationsComboBox.setItemText(
                0, _TRANSLATE("Parent", "None"))

    def retranslateRegressionsComponent(self):

        if self.LANGUAGE == "pt_br":
            self.linearLabel.setText(_TRANSLATE("Parent", "Linear"))
            self.rlmLabel.setText(_TRANSLATE("Parent", "RLM"))
            self.ransacLabel.setText(_TRANSLATE("Parent", "RANSAC"))
            self.degreesLabel.setText(_TRANSLATE("Parent", "Grau"))

        if self.LANGUAGE == "en_us":
            self.linearLabel.setText(_TRANSLATE("Parent", "Linear"))
            self.rlmLabel.setText(_TRANSLATE("Parent", "RLM"))
            self.ransacLabel.setText(_TRANSLATE("Parent", "RANSAC"))
            self.degreesLabel.setText(_TRANSLATE("Parent", "Degrees"))

    def retranslateThresholdsComponent(self):

        if self.LANGUAGE == "pt_br":
            self.featureLabel.setText(_TRANSLATE("Parent", "Entrada:"))
            self.metricLabel.setText(_TRANSLATE("Parent", "Métrica:"))
            self.filterLabel.setText(_TRANSLATE("Parent", "Filtro:"))
            self.optionsLabel.setText(_TRANSLATE("Parent", "Opção:"))
            self.sourceShow.setText(_TRANSLATE("Parent", "Mostrar"))
            self.metricNormal.setText(_TRANSLATE("Parent", "Normal"))
            self.sourceOutlier.setText(_TRANSLATE("Parent", "Outlier"))
            self.sourceLabel.setText(_TRANSLATE("Parent", "Modelo:"))
            self.entriesLabel.setText(_TRANSLATE("Parent", "Modo:"))
            self.entryShow.setText(_TRANSLATE("Parent", "Mostrar"))
            self.entryOutlier.setText(_TRANSLATE("Parent", "Outlier"))
            self.timeLimitLabel.setText(_TRANSLATE("Parent", "Limite"))

        if self.LANGUAGE == "en_us":
            self.featureLabel.setText(_TRANSLATE("Parent", "Feature:"))
            self.metricLabel.setText(_TRANSLATE("Parent", "Metric:"))
            self.filterLabel.setText(_TRANSLATE("Parent", "Filter:"))
            self.optionsLabel.setText(_TRANSLATE("Parent", "Entry:"))
            self.sourceShow.setText(_TRANSLATE("Parent", "Show"))
            self.featureLabel.setText(_TRANSLATE("Parent", "Feature"))
            self.metricNormal.setText(_TRANSLATE("Parent", "Normal"))
            self.sourceOutlier.setText(_TRANSLATE("Parent", "Outlier"))
            self.sourceLabel.setText(_TRANSLATE("Parent", "Source:"))
            self.optionsLabel.setText(_TRANSLATE("Parent", "Option:"))
            self.entriesLabel.setText(_TRANSLATE("Parent", "Entry:"))
            self.entryShow.setText(_TRANSLATE("Parent", "Show"))
            self.entryOutlier.setText(_TRANSLATE("Parent", "Outlier"))
            self.timeLimitLabel.setText(_TRANSLATE("Parent", "Time Limit"))

    def retranslateSOMComponent(self):
        """  """

        if self.LANGUAGE == "pt_br":
            self.clusterizeLabel.setText(_TRANSLATE("Parent", "Agrupe: "))
            self.clusterButton.setText(_TRANSLATE("Parent", "PRESSIONE"))
            self.somMeshGridLabel.setText(_TRANSLATE("Parent", "Malha:"))
            self.clusterLabel.setText(_TRANSLATE("Parent", "Cluster: "))

            self.somShowBox.setTitle(_TRANSLATE(
                "Parent", "Opções de Visualização"))
            self.showActMap.setText(_TRANSLATE("Parent", "Mapa de Ativação"))
            self.showDistMap.setText(_TRANSLATE("Parent", "Mapa de Distância"))
            self.diffClusters.setText(_TRANSLATE(
                "Parent", "Diferenciar Clusters"))

        if self.LANGUAGE == "en_us":
            self.clusterizeLabel.setText(_TRANSLATE("Parent", "Clusterize: "))
            self.clusterButton.setText(_TRANSLATE("Parent", "PUSH"))
            self.somMeshGridLabel.setText(_TRANSLATE("Parent", "Grid:"))
            self.clusterLabel.setText(_TRANSLATE("Parent", "Cluster: "))

            self.somShowBox.setTitle(_TRANSLATE("Parent", "Show Options"))
            self.showActMap.setText(_TRANSLATE("Parent", "Activation Map"))
            self.showDistMap.setText(_TRANSLATE("Parent", "Distance Map"))
            self.diffClusters.setText(_TRANSLATE(
                "Parent", "Differentiate Clusters"))

    def retranslateShowComponent(self):

        if self.LANGUAGE == "pt_br":
            self.mediumLineButton.setText(
                _TRANSLATE("Parent", "Média dos Dados"))
            self.trainButton.setText(_TRANSLATE("Parent", "Dados de Treino"))
            self.testButton.setText(_TRANSLATE("Parent", "Dados de Teste"))
            self.colorClassifcationButton.setText(
                _TRANSLATE("Parent", "Classificar Nível por Cor"))

        if self.LANGUAGE == "en_us":
            self.mediumLineButton.setText(_TRANSLATE("Parent", "Mean Data"))
            self.trainButton.setText(_TRANSLATE("Parent", "Data Train"))
            self.testButton.setText(_TRANSLATE("Parent", "Data Test"))
            self.colorClassifcationButton.setText(
                _TRANSLATE("Parent", "Classify Level by Color"))

    def retranslatePIDComponent(self):

        if self.LANGUAGE == "pt_br":
            self.derivativeButton.setText(_TRANSLATE("Parent", "Derivada"))
            self.betweenButton.setText(_TRANSLATE(
                "Parent", "Mostrar área da Integral"))
            self.showIntegralParameters.setText(_TRANSLATE(
                "Parent", "Mostrar parâmetros da integral"))

        if self.LANGUAGE == "en_us":
            self.derivativeButton.setText(_TRANSLATE("Parent", "Derivative"))
            self.betweenButton.setText(
                _TRANSLATE("Parent", "Show Integral Area"))
            self.showIntegralParameters.setText(
                _TRANSLATE("Parent", "Show integral parameters"))

        self.integralButton.setText(_TRANSLATE("Parent", "Integral"))
