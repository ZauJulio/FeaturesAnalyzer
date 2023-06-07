import pandas as pd
from interfaces import AbstractController


class DataController(AbstractController):
    def reload(self):
        if (self.core.get('data.source.source') != ''):
            self.data = pd.read_csv(self.core.get('data.source.source'))

            self.core.view.graphView.fig.clear()
            self.core.view.graphView.ax = self.core.view.graphView.fig.add_subplot(111)

            self.core.view.graphView.ax.plot(self.data['P1'])
            self.core.view.graphView.ax.plot(self.data['P2'])
            self.core.view.graphView.ax.plot(self.data['P3'])

            self.core.view.graphView.fig.canvas.draw_idle()
