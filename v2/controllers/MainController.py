from interfaces import AbstractController

from .DataController import DataController


class MainController:
    def __init__(self, core):
        self.S = {
            "data": {
                "source": {
                    "type": "url",
                    "source": ""
                },
            },
        }

        self.core = core
        self.modules: dict[str, AbstractController] = {
            "data": DataController(self.core)
        }

        super().__init__()
