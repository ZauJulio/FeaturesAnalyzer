from os import path

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

    def preLoad(self):
        if self.core.get("data.source.type") == "url":
            self.urlSourceRadio.setValue(True)
        elif self.core.get("data.source.type") == "file":
            self.fileSourceRadio.setValue(True)

        self.fileSource.setText(self.core.get("data.source.source"))

    def connect(self):
        def fileSourceChanged(text: str):
            if text == "":
                self.fileSource.onError()

            elif self.urlSourceRadio.getValue():
                # TODO: Add a regex to check if the url is valid
                if text.startswith("http"):
                    self.core.updateBatch([
                        ("data.source.type", "url"),
                        ("data.source.source", text)
                    ])
                else:
                    self.fileSource.onError()
            elif self.fileSourceRadio.getValue():
                if path.isfile(text):
                    self.core.updateBatch([
                        ("data.source.type", "file"),
                        ("data.source.source", text)
                    ])
                else:
                    self.fileSource.onError()
            else:
                self.fileSource.onError()
                self.fileSource.setText("Select a source type")

        def sourceTypeChanged(value: bool, type: str):
            if type != self.core.get("data.source.type"):
                if type == "url":
                    self.core.updateBatch([
                        ("data.source.type", type if value else "file"),
                        ("data.source.source", "")
                    ])
                else:
                    self.core.updateBatch([
                        ("data.source.type", type if value else "url"),
                        ("data.source.source", "")
                    ])

                self.fileSource.setText("")
                self.fileSource.onError()

        self.fileSource.setOnChange(fileSourceChanged)
        self.urlSourceRadio.setOnChange(
            lambda value: sourceTypeChanged(value, "url"))
        self.fileSourceRadio.setOnChange(
            lambda value: sourceTypeChanged(value, "file"))
