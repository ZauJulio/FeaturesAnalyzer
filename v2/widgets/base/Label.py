from typing import Any, Callable, Optional

from interfaces.Widget import AbstractWidget
from PyQt6.QtWidgets import QLabel, QWidget


class Label(QLabel, AbstractWidget):
    def __init__(self,
                 parent: Optional[QWidget] = None,
                 buddy: Optional[QWidget] = None,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        if buddy:
            self.setBuddy(buddy)

    def setOnChange(self, callback: Callable[[Any], None]) -> None:
        return None
