from PyQt5 import QtCore, QtWidgets


class PIDComponent(object):
    def __init__(self, parent):
        """  """
        self.pid_box(parent)
        self.pid_layout()

    def pid_box(self, parent):
        """  """
        self.pidBox = QtWidgets.QGroupBox(parent)
        self.pidBox.setObjectName("pidBox")

        self.dateComBox = QtWidgets.QComboBox(self.pidBox)
        self.dateComBox.setObjectName("dateComBox")

        self.derivativeButton = QtWidgets.QPushButton(self.pidBox)
        self.derivativeButton.setObjectName("derivativeButton")
        self.derivativeButton.setCheckable(True)

        self.integralButton = QtWidgets.QPushButton(self.pidBox)
        self.integralButton.setObjectName("integralButton")
        self.integralButton.setCheckable(True)

        self.betweenButton = QtWidgets.QPushButton(self.pidBox)
        self.betweenButton.setCheckable(True)
        self.betweenButton.setObjectName("betweenButton")

        self.showIntegralParameters = QtWidgets.QPushButton(self.pidBox)
        self.showIntegralParameters.setCheckable(True)
        self.showIntegralParameters.setObjectName("showIntegralParameters")

    def pid_layout(self):
        """  """
        self.pidLayout = QtWidgets.QGridLayout()
        self.pidContainer = QtWidgets.QVBoxLayout(self.pidBox)
        self.pidContainer.setObjectName("pidContainer")
        self.pidContainer.addLayout(self.pidLayout)

        self.pidLayout.addWidget(self.dateComBox, 1, 0, 1, 2)
        self.pidLayout.addWidget(self.derivativeButton, 2, 0, 1, 1)
        self.pidLayout.addWidget(self.integralButton, 2, 1, 1, 1)
        self.pidLayout.addWidget(self.betweenButton, 3, 0, 1, 1)
        self.pidLayout.addWidget(self.showIntegralParameters, 3, 1, 1, 1)
        self.pidLayout.setObjectName("pidLayout")

    def updateSamplePIDComboBox(self):
        """  """
        self.dateComBox.clear()

        if self.testButton.isChecked():
            data = self.dataTest
        else:
            if self.R.Clusterize:
                data = self.trainClusters[self.R.Cluster]
            else:
                data = self.dataTrain

        items = list(data.columns)
        items.remove('hora') if 'hora' in items else None
        if self.LANGUAGE == 'pt_br':
            items.insert(0, 'Amostra...')
        if self.LANGUAGE == 'en_us':
            items.insert(0, 'Sample...')

        self.dateComBox.addItems(items)

    def connectWidgetsPID(self):
        """  """
        self.dateComBox.textActivated.connect(
            lambda x: self.connectSettingsPID('sample', str(x)))
        self.derivativeButton.clicked.connect(
            lambda: self.connectSettingsPID('derivative', self.derivativeButton.isChecked()))
        self.integralButton.clicked.connect(
            lambda: self.connectSettingsPID('integral', self.integralButton.isChecked()))
        self.betweenButton.clicked.connect(
            lambda checked: self.connectSettingsPID('fillBetween', checked))
        self.showIntegralParameters.clicked.connect(
            lambda checked: self.connectSettingsPID('showIntegralParameters', checked))

    def connectSettingsPID(self, field, setting):
        """  """
        settings = self.loadSettings()
        if settings['pid'][field] != setting:
            settings['pid'][field] = setting
            self.saveSettings(settings)
            self.makePlot()

    def preloadEntrysPID(self):
        """  """
        self.updateSamplePIDComboBox()

        self.dateComBox.setCurrentText(self.R.PIDSample)
        self.derivativeButton.setChecked(self.R.Derivative)
        self.integralButton.setChecked(self.R.Integral)
        self.betweenButton.setChecked(self.R.FillBetween)
        self.showIntegralParameters.setChecked(self.R.IntegralParameters)
