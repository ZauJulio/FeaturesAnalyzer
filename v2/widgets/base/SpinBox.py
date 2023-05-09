from contextlib import suppress
from typing import Callable, Optional, Tuple

from interfaces.Widget import AbstractWidget
from PyQt6.QtWidgets import QSpinBox, QWidget


class SpinBox(QSpinBox, AbstractWidget):
    def __init__(self,
                 parent: Optional[QWidget] = None,
                 minimum: int = 0,
                 maximum: int = 100,
                 property: Tuple[str, int] = ("value", 0),
                 onChange: Callable[[int], None] = lambda x: None,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setProperty(*property)

        self.editingFinished.connect(lambda: onChange(self.getValue()))

    def getValue(self) -> int:
        return self.value()

    def setValue(self, value: int) -> None:
        self.setValue(value)

    def setOnChange(self, callback: Callable[[int], None]) -> None:
        with suppress(TypeError):
            self.editingFinished.disconnect()

        self.editingFinished.connect(lambda: callback(self.getValue()))
