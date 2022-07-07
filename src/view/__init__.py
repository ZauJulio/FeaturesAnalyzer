from .Graphs import Graphs
from .GUI import Interface


class Views(Interface, Graphs):
    def __init__(self, parent):
        print("--> Initializing the views:...", end="")
        Graphs.__init__(self)
        print('| DONE')
        Interface.__init__(self, parent)
