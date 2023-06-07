from typing import Callable, List, Optional

from interfaces.Widget import AbstractWidget
from PyQt6.QtWidgets import QComboBox, QWidget
from contextlib import suppress


class ComboBox(QComboBox, AbstractWidget):
    def __init__(self,
                 parent: Optional[QWidget] = None,
                 items: List[str] = [],
                 onChange: Callable[[str], None] = lambda x: None,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.addItems(items)
        self.currentTextChanged.connect(lambda: onChange(self.getValue()))

    def getValue(self) -> str:
        return self.currentText()

    def setValue(self, items: List[str]) -> None:
        self.clear()
        self.addItems(items)

    def setOnChange(self, callback: Callable[[str], None]) -> None:
        with suppress(TypeError):
            self.currentTextChanged.disconnect()

        self.currentTextChanged.connect(lambda: callback(self.getValue()))
