from ..base import ComboBox, Label, TimeEdit
from interfaces import AbstractLayout

from PyQt6.QtWidgets import QGridLayout, QGroupBox


class SplitPage(QGroupBox, AbstractLayout):
    def buildComponents(self):
        self.weekdayComboBox = ComboBox(self)
        self.weekdayLabel = Label(self, "Weekday", self.weekdayComboBox)

        # Data Train
        self.trainStartComboBox = ComboBox(self, ["", "", "", ""])
        self.trainEndComboBox = ComboBox(self, ["", "", "", ""])
        self.trainStartEndLabel = Label(
            self, "Train: Start - End", self.trainStartComboBox)

        # Data Test
        self.testStartComboBox = ComboBox(self, ["", "", "", ""])
        self.testEndComboBox = ComboBox(self, ["", "", "", ""])
        self.testStartEndLabel = Label(
            self, "Test: Start - End", self.testStartComboBox)

        # Hour
        self.hourStartTimeEdit = TimeEdit(self)
        self.hourEndTimeEdit = TimeEdit(self)
        self.hourLabel = Label(self, "Time: Start - End",
                               self.hourStartTimeEdit)

    def buildLayout(self):
        dataLayout = QGridLayout(self)

        # Widget, row=0, column=0, rowSpan=1, columnSpan=1
        dataLayout.addWidget(self.weekdayLabel,       0, 0, 1, 1)
        dataLayout.addWidget(self.weekdayComboBox,    0, 1, 1, 2)

        dataLayout.addWidget(self.trainStartEndLabel, 2, 0, 1, 1)
        dataLayout.addWidget(self.trainStartComboBox, 2, 1, 1, 1)
        dataLayout.addWidget(self.trainEndComboBox,   2, 2, 1, 1)

        dataLayout.addWidget(self.testStartEndLabel,  3, 0, 1, 1)
        dataLayout.addWidget(self.testStartComboBox,  3, 1, 1, 1)
        dataLayout.addWidget(self.testEndComboBox,    3, 2, 1, 1)

        dataLayout.addWidget(self.hourLabel,          5, 0, 1, 1)
        dataLayout.addWidget(self.hourStartTimeEdit,  5, 1, 1, 1)
        dataLayout.addWidget(self.hourEndTimeEdit,    5, 2, 1, 1)
