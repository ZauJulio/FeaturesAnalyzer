from typing import Any

from controllers import MainController
from PyQt6.QtWidgets import QMainWindow
from views import MainView


class Core:
    def __init__(self, window: QMainWindow, language: str = 'en_us'):
        self.window = window
        self.language = language

        self.controller = MainController(self)
        self.view = MainView(self)

    def get(self, key: str) -> Any:
        paths = key.split(".")
        mirror: Any = self.controller.S

        if len(paths) == 1:
            return self.controller.S[key]
        else:
            return [mirror := mirror[path] for path in paths][-1]

    def update(self, key: str, value: Any, apply: bool = True) -> None:
        paths = key.split(".")
        mirror: Any = self.controller.S

        if len(paths) == 1:
            self.controller.S.update({key: value})
        else:
            [mirror := mirror[path] for path in paths[:-1]]

            mirror[paths[-1]] = value

        if apply:
            self.apply(paths[0])

    def updateBatch(self, arr: list[tuple[str, Any]], applyOnEnd: bool = True) -> None:
        [self.update(item[0], item[1], False) for item in arr]

        if applyOnEnd:
            self.apply(arr[0][0].split(".")[0])

    def apply(self, module: str) -> None:
        self.controller.modules[module].reload()
