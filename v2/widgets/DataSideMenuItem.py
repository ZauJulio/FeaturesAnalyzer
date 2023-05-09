from PyQt6.QtWidgets import QGridLayout, QGroupBox, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from .base.CheckBox import CheckBox
from .base.ComboBox import ComboBox
from .base.Label import Label
from .base.PushButton import PushButton
from .base.RadioButton import RadioButton
from .base.SpinBox import SpinBox
from .base.TimeEdit import TimeEdit


class DataSideMenuItem(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.buildComponents()
        self.buildLayout()

    def buildComponents(self):
        self.dataBox = QGroupBox(self)

        self.weekdayLabel = Label(parent=self.dataBox)
        self.weekdayComboBox = ComboBox(parent=self.dataBox, items=["", "", "", "", "", "", "", ""])

        # Data Train
        self.trainStartComboBox = ComboBox(parent=self.dataBox, items=["", "", "", ""])
        self.trainEndComboBox = ComboBox(parent=self.dataBox, items=["", "", "", ""])

        # Data Test
        self.trainStartEndLabel = Label(parent=self.dataBox, buddy=self.trainStartComboBox)
        self.testStartComboBox = ComboBox(self.dataBox, items=["", "", "", ""])
        self.testEndComboBox = ComboBox(self.dataBox, items=["", "", "", ""])

        # Hour
        self.testStartEndLabel = Label(parent=self.dataBox, buddy=self.testStartComboBox)
        self.hourStartTimeEdit = TimeEdit(parent=self.dataBox)
        self.hourEndTimeEdit = TimeEdit(parent=self.dataBox)

        self.hourLabel = Label(parent=self.dataBox, buddy=self.hourStartTimeEdit)

        # Advanced Options
        self.advancedData = CheckBox(parent=self.dataBox, checkable=True, checked=False)

        # Buttons
        self.trainingDataButton = PushButton(parent=self.dataBox, checkable=True)
        self.fillNaNButton = PushButton(parent=self.dataBox, checkable=True)
        self.dropIntervalButton = PushButton(parent=self.dataBox, checkable=True, checked=False)

        self.mobMedianRadio = RadioButton(parent=self.dataBox)
        self.mobMedianSpinBox = SpinBox(parent=self.dataBox, minimum=1, maximum=1440, property=("value", 5))

        self.fieldLabel = Label(parent=self.dataBox)
        self.fieldComboBox = ComboBox(parent=self.dataBox, items=["", "", "", "", "", "", "", "", ""])

        self.windowLabel = Label(parent=self.dataBox)

        self.defaultRadio = RadioButton(parent=self.dataBox, checked=True)
        self.meanRadio = RadioButton(parent=self.dataBox)
        self.mobMeanRadio = RadioButton(parent=self.dataBox)

        self.mobMeanSpinBox = SpinBox(parent=self.dataBox, minimum=1, maximum=1440, property=("value", 5))

        self.transformationsLabel = Label(parent=self.dataBox)
        self.transformationsComboBox = ComboBox(parent=self.dataBox, items=["", "", "", "", "", "", "", "", ""])

        # self.trainingDataButton.setVisible(False)
        # self.fillNaNButton.setVisible(False)
        # self.dropIntervalButton.setVisible(False)
        # self.mobMedianRadio.setVisible(False)
        # self.mobMedianSpinBox.setVisible(False)
        # self.fieldLabel.setVisible(False)
        # self.fieldComboBox.setVisible(False)
        # self.windowLabel.setVisible(False)
        # self.defaultRadio.setVisible(False)
        # self.meanRadio.setVisible(False)
        # self.mobMeanRadio.setVisible(False)
        # self.mobMeanSpinBox.setVisible(False)
        # self.transformationsLabel.setVisible(False)
        # self.transformationsComboBox.setVisible(False)

    def buildLayout(self):
        dataLayout = QGridLayout()

        dataContainer = QVBoxLayout(self.dataBox)
        dataContainer.addLayout(dataLayout)

        # Widget, row=0, column=0, rowSpan=1, columnSpan=1
        dataLayout.addWidget(self.weekdayLabel, 0, 0, 1, 1)
        dataLayout.addWidget(self.weekdayComboBox, 0, 1, 1, 2)

        dataLayout.addWidget(self.fieldLabel, 1, 0, 1, 1)
        dataLayout.addWidget(self.fieldComboBox, 1, 1, 1, 2)

        dataLayout.addWidget(self.trainStartEndLabel, 2, 0, 1, 1)
        dataLayout.addWidget(self.trainStartComboBox, 2, 1, 1, 1)
        dataLayout.addWidget(self.trainEndComboBox, 2, 2, 1, 1)

        dataLayout.addWidget(self.testStartEndLabel, 3, 0, 1, 1)
        dataLayout.addWidget(self.testStartComboBox, 3, 1, 1, 1)
        dataLayout.addWidget(self.testEndComboBox, 3, 2, 1, 1)

        dataLayout.addWidget(self.hourLabel, 5, 0, 1, 1)
        dataLayout.addWidget(self.hourStartTimeEdit, 5, 1, 1, 1)
        dataLayout.addWidget(self.hourEndTimeEdit, 5, 2, 1, 1)
        dataLayout.addWidget(self.transformationsLabel, 6, 0, 1, 1)
        dataLayout.addWidget(self.transformationsComboBox, 6, 1, 1, 2)

        spacerItemBefore = QSpacerItem(
            20, 20,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Fixed)

        dataLayout.addItem(spacerItemBefore, 7, 0, 1, 2)
        dataLayout.addWidget(self.advancedData, 8, 0, 1, 2)

        dataLayout.addWidget(self.dropIntervalButton, 9, 0, 1, 3)
        dataLayout.addWidget(self.trainingDataButton, 10, 0, 1, 3)
        dataLayout.addWidget(self.fillNaNButton, 11, 0, 1, 3)

        spacerItemAfterButtons = QSpacerItem(
            18, 18,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Fixed)

        dataLayout.addItem(spacerItemAfterButtons, 12, 0, 1, 2)

        dataLayout.addWidget(self.windowLabel, 15, 2, 1, 1)
        dataLayout.addWidget(self.defaultRadio, 14, 0, 1, 3)
        dataLayout.addWidget(self.meanRadio, 15, 0, 1, 3)
        dataLayout.addWidget(self.mobMeanRadio, 16, 0, 1, 1)

        dataLayout.addWidget(self.mobMeanSpinBox, 16, 2, 1, 1)
        dataLayout.addWidget(self.mobMedianRadio, 17, 0, 1, 1)
        dataLayout.addWidget(self.mobMedianSpinBox, 17, 2, 1, 1)
