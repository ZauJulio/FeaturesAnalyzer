from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib

matplotlib.use('QtAgg', force=True)


class MPLCanvas(FigureCanvasQTAgg):
    def __init__(self, fig: Figure):
        super(MPLCanvas, self).__init__(fig)
