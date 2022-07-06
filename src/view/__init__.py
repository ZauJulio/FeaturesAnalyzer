from .Graphs import Graphs
from .GUI import Interface


class Views(Interface, Graphs):
    def __init__(self, parent):
        Graphs.__init__(self)
        Interface.__init__(self, parent)
