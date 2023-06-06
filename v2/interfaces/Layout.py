from PyQt6.QtWidgets import QWidget


class AbstractLayout(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args[1:], **kwargs)
        self.core = args[0].core

        self.buildComponents()
        self.buildLayout()
        self.setStyles()
        self.preLoad()
        self.connect()

    def buildComponents(self):
        raise NotImplementedError()

    def buildLayout(self):
        raise NotImplementedError()

    def setStyles(self):
        pass

    def connect(self):
        pass

    def preLoad(self):
        pass
