import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure


class GraphBox(Gtk.Box):
    """A Gtk.Box that contains a matplotlib graph."""

    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.figure = Figure(figsize=(500, 400))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.pack_start(self.canvas, True, True, 0)
        self.canvas.show()

    def plot(self, x, y):
        """Plot a graph on the canvas."""
        self.ax.clear()  # Clear the previous plot
        self.ax.plot(x, y)
        self.canvas.draw()
