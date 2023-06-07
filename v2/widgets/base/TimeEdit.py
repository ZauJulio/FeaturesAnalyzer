from contextlib import suppress
from datetime import time
from typing import Callable, Optional

from interfaces.Widget import AbstractWidget
from PyQt6.QtCore import QTime
from PyQt6.QtWidgets import QTimeEdit, QWidget


class TimeEdit(QTimeEdit, AbstractWidget):
    def __init__(self,
                 parent: Optional[QWidget] = None,
                 value: time = time(0, 0, 0),
                 maxTime: QTime = QTime(23, 59, 59),
                 calendarPopUp: bool = True,
                 displayFormat: str = 'hh:mm',
                 onChange: Callable[[str], None] = lambda x: None,
                 *args, **kwargs):

        super().__init__(parent, *args, **kwargs)

        self.setTime(value)
        self.setMaximumTime(maxTime)
        self.setCalendarPopup(calendarPopUp)
        self.setDisplayFormat(displayFormat)
        self.editingFinished.connect(lambda: onChange(self.text()))

    def getValue(self) -> str:
        return self.text()

    def setValue(self, value: time) -> None:
        self.setTime(value)

    def setOnChange(self, callback: Callable[[str], None]) -> None:
        with suppress(TypeError):
            self.editingFinished.disconnect()

        self.editingFinished.connect(lambda: callback(self.getValue()))
