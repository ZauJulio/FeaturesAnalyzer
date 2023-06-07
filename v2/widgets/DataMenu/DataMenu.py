from interfaces import AbstractLayout
from PyQt6.QtWidgets import QGroupBox, QTabWidget, QVBoxLayout

from . import PreProcessPage, SplitPage, ImportPage


class DataMenu(QGroupBox, AbstractLayout):
    def buildComponents(self):
        self.importPage = ImportPage(self)
        self.splitPage = SplitPage(self)
        self.preProcessPage = PreProcessPage(self)

    def buildLayout(self):
        tabWidget = QTabWidget(self)
        tabWidget.addTab(self.importPage, "Import")
        tabWidget.addTab(self.splitPage, "Split")
        tabWidget.addTab(self.preProcessPage, "Pre-Process")

        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(tabWidget)

    def setStyles(self):
        self.setTitle("Data")
