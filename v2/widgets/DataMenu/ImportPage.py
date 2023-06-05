from interfaces import AbstractLayout
from PyQt6.QtWidgets import QGridLayout, QGroupBox, QHBoxLayout

from ..base import Label, LineEdit, RadioButton


class ImportPage(QGroupBox, AbstractLayout):
    def buildComponents(self):
        self.sourceSelectionGroup = QGroupBox("Source Selection", self)

        self.urlSourceRadio = RadioButton(self, "URL")
        self.fileSourceRadio = RadioButton(self, "File")

        self.fileSource = LineEdit(self, "")
        self.fileSourceLabel = Label(self, "File Source", self.fileSource)

    def buildLayout(self):
        self.widgetLayout = QGridLayout(self)

        self.sourceSelectionLayout = QHBoxLayout(self.sourceSelectionGroup)
        self.sourceSelectionLayout.addWidget(self.urlSourceRadio)
        self.sourceSelectionLayout.addWidget(self.fileSourceRadio)

        # Widget, row=0, column=0, rowSpan=1, columnSpan=1
        self.widgetLayout.addWidget(self.sourceSelectionGroup, 0, 0, 1, 3)
        self.widgetLayout.addWidget(self.fileSourceLabel,      1, 0, 1, 3)
        self.widgetLayout.addWidget(self.fileSource,           2, 0, 1, 3)

    def connect(self):
        def fileSourceChanged(text: str):
            self.core.controller.S.update({"fileSource": text})
            print(text, self.core.controller.S)

        self.fileSource.setOnChange(fileSourceChanged)
