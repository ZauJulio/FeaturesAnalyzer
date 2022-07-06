from .DataController import DataController
from .ThresholdsController import ThresholdsController
from .PIDController import PIDController
from .SOMController import SOMController
from .RegressionsController import RegressionsController

class Controllers(DataController, RegressionsController, ThresholdsController, PIDController, SOMController):
    def __init__(self):
        """  """
        pass