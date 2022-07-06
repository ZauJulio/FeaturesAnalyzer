from lib.util import timelib
from PyQt5 import QtCore, QtWidgets


class ShowComponent(object):
    def __init__(self, parent):
        """  """
        self.__box(parent)
        self.__layout()
        self.connectWidgetsShow()

    def __box(self, parent):
        """  """
        self.showBox = QtWidgets.QGroupBox(parent)
        self.showBox.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.showBox.setObjectName("showBox")

        self.showComboBox = QtWidgets.QComboBox(self.showBox)
        self.showComboBox.setObjectName("showSamples")

        self.mediumLineButton = QtWidgets.QPushButton(self.showBox)
        self.mediumLineButton.setCheckable(True)
        self.mediumLineButton.setObjectName("mediumLineButton")

        self.trainButton = QtWidgets.QPushButton(self.showBox)
        self.trainButton.setCheckable(True)
        self.trainButton.setObjectName("trainButton")

        self.testButton = QtWidgets.QPushButton(self.showBox)
        self.testButton.setCheckable(True)
        self.testButton.setChecked(True)
        self.testButton.setObjectName("testButton")

        self.colorClassifcationButton = QtWidgets.QPushButton(self.showBox)
        self.colorClassifcationButton.setCheckable(True)
        self.colorClassifcationButton.setChecked(True)
        self.colorClassifcationButton.setObjectName("colorClassifcationButton")

        # Time limit
        self.timeLimitLabel = QtWidgets.QLabel("Time Limit:", parent)
        self.timeLimitLabel.setVisible(True)
        #
        self.timeLimitEdit = QtWidgets.QTimeEdit(parent)
        self.timeLimitEdit.setMaximumTime(QtCore.QTime(23, 59, 59))
        self.timeLimitEdit.setDisplayFormat('hh:mm')
        self.timeLimitEdit.setCalendarPopup(True)
        self.timeLimitEdit.setObjectName("timeLimitEdit")

    def __layout(self):
        """  """
        self.showLayout = QtWidgets.QGridLayout()
        self.showContainer = QtWidgets.QVBoxLayout(self.showBox)
        self.showContainer.setObjectName("showContainer")
        self.showContainer.addLayout(self.showLayout)

        self.showLayout.addWidget(self.showComboBox, 0, 0, 1, 3)
        self.showLayout.addWidget(self.trainButton, 1, 0, 1, 1)
        self.showLayout.addWidget(self.mediumLineButton, 1, 1, 1, 1)
        self.showLayout.addWidget(self.testButton, 1, 2, 1, 1)
        self.showLayout.addWidget(self.colorClassifcationButton, 2, 0, 1, 3)

        spacerItemBefore = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        
        self.showLayout.addItem(spacerItemBefore, 3, 0, 1, 3)
        self.showLayout.addWidget(self.timeLimitLabel, 4, 0, 1, 1)
        self.showLayout.addWidget(self.timeLimitEdit, 4, 1, 1, 2)

        self.showLayout.setObjectName("showLayout")

    def updateSampleShowComboBox(self):
        """  """
        self.showComboBox.clear()

        if self.testButton.isChecked():
            data = self.dataTest
        else:
            if self.R.Clusterize:
                data = self.trainClusters[self.R.Cluster]
            else:
                data = self.dataTrain

        items = list(data.columns)
        items.remove('hora') if 'hora' in items else None
        items.insert(0, 'All')

        self.showComboBox.addItems(items)

    def connectWidgetTrainTest(self, field, check):
        """  """
        if field == 'train' and self.trainButton.isChecked() and self.testButton.isChecked():
            self.testButton.setChecked(False)
            self.connectSettingsShow('test', False)
        if field == 'test' and self.testButton.isChecked() and self.trainButton.isChecked():
            self.trainButton.setChecked(False)
            self.connectSettingsShow('train', False)

        self.connectSettingsShow(field, check)
        self.updateClustersComboBox()
        self.updateSampleShowComboBox()
        self.updateSamplePIDComboBox()

    def connectWidgetsShow(self):
        """  """
        self.showComboBox.textActivated.connect(
            lambda x: self.connectSettingsShow('data', str(x)))
        self.mediumLineButton.clicked.connect(
            lambda x: self.connectSettingsShow('mediumLine', x))
        self.colorClassifcationButton.clicked.connect(lambda: self.connectSettingsShow(
            'ColorClassification', self.colorClassifcationButton.isChecked()))

        self.trainButton.clicked.connect(
            lambda: self.connectWidgetTrainTest('train', self.trainButton.isChecked()))
        self.testButton.clicked.connect(
            lambda: self.connectWidgetTrainTest('test', self.testButton.isChecked()))

        self.timeLimitEdit.editingFinished.connect(
            lambda: self.connectSettingsShow('TimeLimit', self.timeLimitEdit.text()))

    def connectSettingsShow(self, field, sample):
        """  """
        settings = self.loadSettings()
        if settings['show'][field] != sample:
            settings['show'][field] = sample
            self.saveSettings(settings)
            self.makePlot()

    def __resetDataSettings(self):
        """  """
        settings = self.loadSettings()
        settings['show']['train'] = False
        settings['show']['test'] = True
        self.saveSettings(settings)

    def preloadEntrysShow(self):
        """  """
        self.updateSampleShowComboBox()
        self.__resetDataSettings()
        self.showComboBox.setCurrentText(self.R.ShowSample)
        self.mediumLineButton.setChecked(self.R.MediumLine)
        self.colorClassifcationButton.setChecked(self.R.ColorClassification)
        self.timeLimitEdit.setTime(timelib.time_from_str(self.R.TimeLimit))
