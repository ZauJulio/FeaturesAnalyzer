from PyQt5 import QtCore, QtWidgets


class RegressionsComponent(object):
    def __init__(self, parent):
        """  """
        self.regression_box(parent)
        self.regressions_layout()

    def regression_box(self, parent):
        """  """
        self.regressionsBox = QtWidgets.QGroupBox(parent)
        self.regressionsBox.setObjectName("regressionsBox")

        # Spin's
        # LINEAR
        self.linearSpinBox = QtWidgets.QSpinBox(self.regressionsBox)
        self.linearSpinBox.setMaximum(10)
        self.linearSpinBox.setMinimum(1)
        self.linearSpinBox.setProperty("value", 5)
        self.linearSpinBox.setObjectName("linearSpinBox")

        # RLM
        self.rlmSpinBox = QtWidgets.QSpinBox(self.regressionsBox)
        self.rlmSpinBox.setMaximum(10)
        self.rlmSpinBox.setMinimum(1)
        self.rlmSpinBox.setProperty("value", 5)
        self.rlmSpinBox.setObjectName("rlmSpinBox")

        self.ransacSpinBox = QtWidgets.QSpinBox(self.regressionsBox)
        self.ransacSpinBox.setMaximum(10)
        self.ransacSpinBox.setMinimum(1)
        self.ransacSpinBox.setProperty("value", 5)
        self.ransacSpinBox.setObjectName("ransacSpinBox")

        # Label's
        self.degreesLabel = QtWidgets.QLabel(self.regressionsBox)
        self.degreesLabel.setObjectName("degreesLabel")

        # LINEAR
        self.linearLabel = QtWidgets.QLabel(self.regressionsBox)
        self.linearLabel.setObjectName("linearLabel")

        # RLM
        self.rlmLabel = QtWidgets.QLabel(self.regressionsBox)
        self.rlmLabel.setObjectName("rlmLabel")

        # RANSAC
        self.ransacLabel = QtWidgets.QLabel(self.regressionsBox)
        self.ransacLabel.setObjectName("ransacLabel")

    def regressions_layout(self):
        """  """
        self.regressionsLayout = QtWidgets.QGridLayout()
        self.regressionsContainer = QtWidgets.QVBoxLayout(self.regressionsBox)
        self.regressionsContainer.setObjectName("regressionsContainer")
        self.regressionsContainer.addLayout(self.regressionsLayout)

        self.regressionsLayout.addWidget(self.degreesLabel, 0, 1, 1, 1)
        self.regressionsLayout.addWidget(self.linearLabel, 1, 0, 1, 1)
        self.regressionsLayout.addWidget(self.ransacLabel, 2, 0, 1, 1)
        self.regressionsLayout.addWidget(self.rlmLabel, 3, 0, 1, 1)

        self.regressionsLayout.addWidget(self.linearSpinBox, 1, 1, 1, 2)
        self.regressionsLayout.addWidget(self.ransacSpinBox, 2, 1, 1, 2)
        self.regressionsLayout.addWidget(self.rlmSpinBox, 3, 1, 1, 2)
        self.regressionsLayout.setObjectName("regressionsLayout")

    def connectWidgetsRegressions(self):
        """  """
        self.linearSpinBox.editingFinished.connect(
            lambda: self.connectSettingsRegressions('linearDegree', self.linearSpinBox.value()))
        self.rlmSpinBox.editingFinished.connect(
            lambda: self.connectSettingsRegressions('RLMDegree', self.rlmSpinBox.value()))
        self.ransacSpinBox.editingFinished.connect(
            lambda: self.connectSettingsRegressions('ransacDegree', self.ransacSpinBox.value()))

    def connectSettingsRegressions(self, field, setting):
        """  """
        settings = self.loadSettings()
        if settings['regressions'][field] != setting:
            settings['regressions'][field] = setting
            self.saveSettings(settings)
            self.makePlot()

    def preloadEntrysRegressions(self):
        """  """
        self.linearSpinBox.setValue(self.R.Regressions['linearDegree'])
        self.rlmSpinBox.setValue(self.R.Regressions['rlmDegree'])
        self.ransacSpinBox.setValue(self.R.Regressions['ransacDegree'])
