import gi

gi.require_version("Gtk", "3.0")


from gi.repository import Gtk
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

plt.style.use("ggplot")


class GraphBox(Gtk.VBox):
    """A box to display a graph."""

    def __init__(self):
        super().__init__()

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar2GTK3(self.canvas)

        self.pack_start(self.canvas, True, True, 0)
        self.pack_start(self.toolbar, False, False, 0)

        self.set_size_request(400, 300)

    def plot(self, *args, **kwargs):
        """Plot data on the graph."""
        self.ax.clear()
        self.ax.plot(*args, **kwargs)

        self.canvas.draw()
