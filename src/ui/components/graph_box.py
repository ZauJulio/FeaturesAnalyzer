from gi.repository import Gtk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure

plt.style.use("ggplot")
plt.ion()


class GraphBox(Gtk.VBox):
    """A box to display a graph."""

    def __init__(self) -> None:
        super().__init__()

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas)

        self.pack_start(child=self.canvas, expand=True, fill=True, padding=0)
        self.pack_start(child=self.toolbar, expand=False, fill=False, padding=0)

        self.set_size_request(400, 300)

    def plot(self, *args, **kwargs) -> None:  # noqa: ANN003, ANN002
        """Plot data on the graph."""
        self.ax.clear()
        self.ax.plot(*args, **kwargs)

        self.canvas.draw()
