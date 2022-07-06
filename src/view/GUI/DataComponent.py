from PyQt5 import QtCore, QtWidgets
from lib.util import timelib


class DataComponent(object):
    def __init__(self, parent):
        """  """
        self.__transformations = [
            "None",
            "Normalize",
            "Standardize",
            "MinMax",
            "MaxAbs",
        ]

        self.data_box(parent)
        self.advanced_data_box()
        self.data_layout()
        self.swapHideAdvanced()

    def data_box(self, parent):
        """  """
        self.dataBox = QtWidgets.QGroupBox(parent)
        self.dataBox.setObjectName("dataBox")

        self.weekdayComboBox = QtWidgets.QComboBox(self.dataBox)
        self.weekdayComboBox.setObjectName("weekdayComboBox")
        self.weekdayComboBox.addItems(["", "", "", "", "", "", "", ""])

        self.weekdayLabel = QtWidgets.QLabel(self.dataBox)
        self.weekdayLabel.setObjectName("weekdayLabel")

        # Data Train
        self.trainStartComboBox = QtWidgets.QComboBox(self.dataBox)
        self.trainStartComboBox.setObjectName("trainStartComboBox")
        self.trainStartComboBox.addItems(["", "", "", ""])

        self.trainEndComboBox = QtWidgets.QComboBox(self.dataBox)
        self.trainEndComboBox.setObjectName("trainEndComboBox")
        self.trainEndComboBox.addItems(["", "", "", ""])

        self.trainStartEndLabel = QtWidgets.QLabel(self.dataBox)
        self.trainStartEndLabel.setObjectName("trainStartEndLabel")
        self.trainStartEndLabel.setBuddy(self.trainStartComboBox)

        # Data Test
        self.testStartComboBox = QtWidgets.QComboBox(self.dataBox)
        self.testStartComboBox.setObjectName("testStartComboBox")
        self.testStartComboBox.addItems(["", "", "", ""])

        self.testEndComboBox = QtWidgets.QComboBox(self.dataBox)
        self.testEndComboBox.setObjectName("testEndComboBox")
        self.testEndComboBox.addItems(["", "", "", ""])

        self.testStartEndLabel = QtWidgets.QLabel(self.dataBox)
        self.testStartEndLabel.setObjectName("testStartEndLabel")
        self.testStartEndLabel.setBuddy(self.testStartComboBox)

        # Hour
        self.hourStartTimeEdit = QtWidgets.QTimeEdit(self.dataBox)
        self.hourStartTimeEdit.setMaximumTime(QtCore.QTime(23, 59, 59))
        self.hourStartTimeEdit.setCalendarPopup(True)
        self.hourStartTimeEdit.setDisplayFormat('hh:mm')
        self.hourStartTimeEdit.setObjectName("hourStartTimeEdit")

        self.hourEndTimeEdit = QtWidgets.QTimeEdit(self.dataBox)
        self.hourEndTimeEdit.setMaximumTime(QtCore.QTime(23, 59, 59))
        self.hourEndTimeEdit.setCalendarPopup(True)
        self.hourEndTimeEdit.setDisplayFormat('hh:mm')
        self.hourEndTimeEdit.setObjectName("hourEndTimeEdit")

        self.hourLabel = QtWidgets.QLabel(self.dataBox)
        self.hourLabel.setObjectName("label")
        self.hourLabel.setBuddy(self.hourStartTimeEdit)

    def advanced_data_box(self):
        """  """
        self.advancedData = QtWidgets.QCheckBox(self.dataBox)
        self.advancedData.setCheckable(True)
        self.advancedData.setChecked(False)
        self.advancedData.setObjectName("advancedData")

        # Buttons
        self.trainingDataButton = QtWidgets.QPushButton(self.dataBox)
        self.trainingDataButton.setCheckable(True)
        self.trainingDataButton.setObjectName("trainingDataButton")

        self.fillnaButton = QtWidgets.QPushButton(self.dataBox)
        self.fillnaButton.setCheckable(True)
        self.fillnaButton.setObjectName("fillnaButton")

        self.dropIntervalButton = QtWidgets.QPushButton(self.dataBox)
        self.dropIntervalButton.setCheckable(True)
        self.dropIntervalButton.setChecked(False)
        self.dropIntervalButton.setObjectName("dropIntervalButton")

        self.mobMedianRadio = QtWidgets.QRadioButton(self.dataBox)
        self.mobMedianRadio.setObjectName("mobMedianRadio")

        self.mobMedianSpinBox = QtWidgets.QSpinBox(self.dataBox)
        self.mobMedianSpinBox.setMinimum(1)
        self.mobMedianSpinBox.setMaximum(1440)
        self.mobMedianSpinBox.setProperty("value", 5)
        self.mobMedianSpinBox.setObjectName("mobMedianSpinBox")

        self.fieldLabel = QtWidgets.QLabel(self.dataBox)
        self.fieldLabel.setObjectName("fieldLabel")

        self.fieldComboBox = QtWidgets.QComboBox(self.dataBox)
        self.fieldComboBox.setObjectName("fieldComboBox")
        self.fieldComboBox.addItems(["", "", "", "", "", "", "", "", ""])

        self.windowLabel = QtWidgets.QLabel(self.dataBox)
        self.windowLabel.setObjectName("windowLabel")

        self.defaultRadio = QtWidgets.QRadioButton(self.dataBox)
        self.defaultRadio.setChecked(True)
        self.defaultRadio.setObjectName("defaultRadio")

        self.meanRadio = QtWidgets.QRadioButton(self.dataBox)
        self.meanRadio.setObjectName("meanRadio")

        self.mobMeanRadio = QtWidgets.QRadioButton(self.dataBox)
        self.mobMeanRadio.setObjectName("mobMeanRadio")

        self.mobMeanSpinBox = QtWidgets.QSpinBox(self.dataBox)
        self.mobMeanSpinBox.setMinimum(1)
        self.mobMeanSpinBox.setMaximum(1440)
        self.mobMeanSpinBox.setProperty("value", 5)
        self.mobMeanSpinBox.setObjectName("mobMeanSpinBox")

        self.transformationsLabel = QtWidgets.QLabel(self.dataBox)
        self.transformationsLabel.setObjectName('transformationsLabel')

        self.transformationsComboBox = QtWidgets.QComboBox(self.dataBox)
        self.transformationsComboBox.addItems(self.__transformations)

        self.trainingDataButton.setVisible(False)
        self.fillnaButton.setVisible(False)
        self.dropIntervalButton.setVisible(False)
        self.mobMedianRadio.setVisible(False)
        self.mobMedianSpinBox.setVisible(False)
        self.fieldLabel.setVisible(False)
        self.fieldComboBox.setVisible(False)
        self.windowLabel.setVisible(False)
        self.defaultRadio.setVisible(False)
        self.meanRadio.setVisible(False)
        self.mobMeanRadio.setVisible(False)
        self.mobMeanSpinBox.setVisible(False)
        self.transformationsLabel.setVisible(False)
        self.transformationsComboBox.setVisible(False)

    def data_layout(self):
        """  """
        self.dataLayout = QtWidgets.QGridLayout()
        self.dataContainer = QtWidgets.QVBoxLayout(self.dataBox)
        self.dataContainer.setObjectName("dataContainer")
        self.dataContainer.addLayout(self.dataLayout)

        self.dataLayout.addWidget(self.weekdayLabel, 0, 0, 1, 1)
        self.dataLayout.addWidget(self.weekdayComboBox, 0, 1, 1, 2)

        self.dataLayout.addWidget(self.fieldLabel, 1, 0, 1, 1)
        self.dataLayout.addWidget(self.fieldComboBox, 1, 1, 1, 2)

        self.dataLayout.addWidget(self.trainStartEndLabel, 2, 0, 1, 1)
        self.dataLayout.addWidget(self.trainStartComboBox, 2, 1, 1, 1)
        self.dataLayout.addWidget(self.trainEndComboBox, 2, 2, 1, 1)

        self.dataLayout.addWidget(self.testStartEndLabel, 3, 0, 1, 1)
        self.dataLayout.addWidget(self.testStartComboBox, 3, 1, 1, 1)
        self.dataLayout.addWidget(self.testEndComboBox, 3, 2, 1, 1)

        self.dataLayout.addWidget(self.hourLabel, 5, 0, 1, 1)
        self.dataLayout.addWidget(self.hourStartTimeEdit, 5, 1, 1, 1)
        self.dataLayout.addWidget(self.hourEndTimeEdit, 5, 2, 1, 1)
        self.dataLayout.addWidget(self.transformationsLabel, 6, 0, 1, 1)
        self.dataLayout.addWidget(self.transformationsComboBox, 6, 1, 1, 2)

        spacerItemBefore = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        self.dataLayout.addItem(spacerItemBefore, 7, 0, 1, 2)
        self.dataLayout.addWidget(self.advancedData, 8, 0, 1, 2)

        self.dataLayout.addWidget(self.dropIntervalButton, 9, 0, 1, 3)
        self.dataLayout.addWidget(self.trainingDataButton, 10, 0, 1, 3)
        self.dataLayout.addWidget(self.fillnaButton, 11, 0, 1, 3)

        spacerItemAfterButtons = QtWidgets.QSpacerItem(18, 18,
                                                       QtWidgets.QSizePolicy.Minimum,
                                                       QtWidgets.QSizePolicy.Fixed)

        self.dataLayout.addItem(spacerItemAfterButtons, 12, 0, 1, 2)

        self.dataLayout.addWidget(self.windowLabel, 15, 2, 1, 1)
        self.dataLayout.addWidget(self.defaultRadio, 14, 0, 1, 3)
        self.dataLayout.addWidget(self.meanRadio, 15, 0, 1, 3)
        self.dataLayout.addWidget(self.mobMeanRadio, 16, 0, 1, 1)

        self.dataLayout.addWidget(self.mobMeanSpinBox, 16, 2, 1, 1)
        self.dataLayout.addWidget(self.mobMedianRadio, 17, 0, 1, 1)
        self.dataLayout.addWidget(self.mobMedianSpinBox, 17, 2, 1, 1)

        self.dataLayout.setObjectName("dataLayout")

    def swapHideAdvanced(self):
        """  """
        self.advancedData.toggled.connect(
            lambda x: (
                self.trainingDataButton.setVisible(x),
                self.fillnaButton.setVisible(x),
                self.dropIntervalButton.setVisible(x),
                self.mobMedianRadio.setVisible(x),
                self.mobMedianSpinBox.setVisible(x),
                self.windowLabel.setVisible(x),
                self.defaultRadio.setVisible(x),
                self.meanRadio.setVisible(x),
                self.mobMeanRadio.setVisible(x),
                self.mobMeanSpinBox.setVisible(x),
                self.transformationsLabel.setVisible(x),
                self.transformationsComboBox.setVisible(x)
            )
        )

    def connectWidgetsDataType(self, type, check):
        """  """
        if check:
            self.connectSettingsData('dataType', type)
            self.updateClustersComboBox()
            self.updateSampleShowComboBox()

    def connectReloadData(self, field, setting):
        """  """
        self.connectSettingsData(field, setting)
        self.updateSamplePIDComboBox()
        self.updateClustersComboBox()
        self.updateSampleShowComboBox()

    def __getWeekday(self, index):
        """  """
        day = timelib.weekday(index)
        if day is None:
            return "All"
        else:
            return day

    def connectWidgetsData(self):
        """  """
        # Main settings
        self.weekdayComboBox.currentTextChanged.connect(
            lambda: self.connectReloadData('weekday', self.__getWeekday(self.weekdayComboBox.currentIndex())))
        self.fieldComboBox.currentTextChanged.connect(
            lambda: self.connectReloadData('field', self.fieldComboBox.currentText()))
        self.trainStartComboBox.currentTextChanged.connect(
            lambda: self.connectReloadData('trainStart', self.trainStartComboBox.currentText()))
        self.trainEndComboBox.currentTextChanged.connect(
            lambda: self.connectReloadData('trainEnd', self.trainEndComboBox.currentText()))
        self.testStartComboBox.currentTextChanged.connect(
            lambda: self.connectReloadData('testStart', self.testStartComboBox.currentText()))
        self.testEndComboBox.currentTextChanged.connect(
            lambda: self.connectReloadData('testEnd', self.testEndComboBox.currentText()))
        self.hourStartTimeEdit.editingFinished.connect(
            lambda: self.connectReloadData('hourStart', self.hourStartTimeEdit.text()))
        self.hourEndTimeEdit.editingFinished.connect(
            lambda: self.connectReloadData('hourEnd', self.hourEndTimeEdit.text()))

        # Additional configurations
        self.dropIntervalButton.clicked.connect(
            lambda: self.connectReloadData('dropInterval', self.dropIntervalButton.isChecked()))
        self.trainingDataButton.clicked.connect(
            lambda: self.connectReloadData('splitData', self.trainingDataButton.isChecked()))
        self.fillnaButton.clicked.connect(
            lambda: self.connectSettingsData('replaceNaN', self.fillnaButton.isChecked()))

        # Special data settings
        self.defaultRadio.toggled.connect(
            lambda: self.connectWidgetsDataType('default', self.defaultRadio.isChecked()))
        self.meanRadio.toggled.connect(
            lambda: self.connectWidgetsDataType('mean', self.meanRadio.isChecked()))
        self.mobMeanRadio.toggled.connect(
            lambda: self.connectWidgetsDataType('mobileMean', self.mobMeanRadio.isChecked()))
        self.mobMedianRadio.toggled.connect(
            lambda: self.connectWidgetsDataType('mobileMedian', self.mobMedianRadio.isChecked()))
        self.mobMeanSpinBox.editingFinished.connect(
            lambda: self.connectSettingsData('mobileMeanMinutes', self.mobMeanSpinBox.value()))
        self.mobMedianSpinBox.editingFinished.connect(
            lambda: self.connectSettingsData('mobileMedianMinutes', self.mobMedianSpinBox.value()))
        self.transformationsComboBox.currentTextChanged.connect(
            lambda x: self.connectReloadData('transformation', x))

    def connectSettingsData(self, field, setting):
        """  """
        settings = self.loadSettings()
        if settings['data'][field] != setting:
            settings['data'][field] = setting
            self.saveSettings(settings)
            self.makePlot()

    def preloadEntrysData(self):
        """ Load from settings file """
        if self.R.Weekday is None:
            self.R.Weekday = "All"
        elif self.R.Weekday.lower() != "all":
            self.weekdayComboBox.setCurrentIndex(timelib.weekday(self.R.Weekday))
        else:
            self.weekdayComboBox.setCurrentIndex(7)

        self.fieldComboBox.setCurrentText(self.R.Field)
        self.trainStartComboBox.setCurrentText(self.R.DateTrainStart)
        self.trainEndComboBox.setCurrentText(self.R.DateTrainEnd)

        self.testStartComboBox.setCurrentText(self.R.DateTestStart)
        self.testEndComboBox.setCurrentText(self.R.DateTestEnd)

        self.hourStartTimeEdit.setTime(timelib.time_from_str(self.R.HourStart))
        self.hourEndTimeEdit.setTime(timelib.time_from_str(self.R.HourEnd))

        # Additional configurations
        self.dropIntervalButton.setChecked(self.R.DropInterval)
        self.trainingDataButton.setChecked(self.R.SplitData)
        self.fillnaButton.setChecked(self.R.ReplaceNaN)

        # Special data settings
        if self.R.DataType == 'default':
            self.defaultRadio.setChecked(True)
        if self.R.DataType == 'mean':
            self.meanRadio.setChecked(True)
        if self.R.DataType == 'mobileMean':
            self.mobMeanRadio.setChecked(True)
        if self.R.DataType == 'mobileMedian':
            self.mobMedianRadio.setChecked(True)

        self.mobMeanSpinBox.setValue(self.R.MobMeanMin)
        self.mobMedianSpinBox.setValue(self.R.MobMedianMin)

        transformation = 0
        for i, element in enumerate(self.__transformations):
            if element == self.R.Transformation:
                transformation = i

        self.transformationsComboBox.setCurrentIndex(transformation)
