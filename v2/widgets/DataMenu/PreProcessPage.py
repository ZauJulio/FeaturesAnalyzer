from interfaces import AbstractLayout
from PyQt6.QtWidgets import QGridLayout, QGroupBox

from ..base import ComboBox, Label, PushButton, RadioButton, SpinBox


class PreProcessPage(QGroupBox, AbstractLayout):
    def buildComponents(self):
        self.trainingDataButton = PushButton(self, checkable=True)
        self.fillNaNButton = PushButton(self, checkable=True)
        self.dropIntervalButton = PushButton(
            self, checkable=True, checked=False)

        self.mobMedianRadio = RadioButton(self)
        self.mobMedianSpinBox = SpinBox(self, 1, 1440, property=("value", 5))

        self.windowLabel = Label(self, value="Window")

        self.defaultRadio = RadioButton(self, checked=True)
        self.meanRadio = RadioButton(self)
        self.mobMeanRadio = RadioButton(self)

        self.mobMeanSpinBox = SpinBox(self, 1, 1440, property=("value", 5))

        self.transformationsLabel = Label(self, value="Transformations")
        self.transformationsComboBox = ComboBox(
            self, items=["", "", "", "", "", "", "", "", ""])

    def buildLayout(self):
        dataLayout = QGridLayout(self)

        # Widget, row=0, column=0, rowSpan=1, columnSpan=1
        dataLayout.addWidget(self.dropIntervalButton,      0, 0, 1, 3)
        dataLayout.addWidget(self.trainingDataButton,      0, 1, 1, 3)

        dataLayout.addWidget(self.fillNaNButton,           1, 0, 1, 3)
        dataLayout.addWidget(self.windowLabel,             1, 1, 1, 1)

        dataLayout.addWidget(self.defaultRadio,            2, 0, 1, 3)
        dataLayout.addWidget(self.meanRadio,               2, 1, 1, 3)
        dataLayout.addWidget(self.mobMeanRadio,            2, 2, 1, 1)

        dataLayout.addWidget(self.mobMeanSpinBox,          3, 0, 1, 1)
        dataLayout.addWidget(self.mobMedianRadio,          3, 1, 1, 1)
        dataLayout.addWidget(self.mobMedianSpinBox,        3, 2, 1, 1)

        dataLayout.addWidget(self.transformationsLabel,    4, 0, 1, 1)
        dataLayout.addWidget(self.transformationsComboBox, 4, 1, 1, 3)
