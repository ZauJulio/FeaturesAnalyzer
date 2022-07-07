from PyQt5 import QtCore, QtWidgets
import pandas as pd
import numpy as np

class SOMComponent(object):
    def __init__(self, parent):
        """  """
        self.somMesh = []
        self.__somBox(parent)
        self.__setSOMShowLayout()
        self.__setSOMLayout()

    def __somBox(self, parent):
        """  """
        self.somBox = QtWidgets.QGroupBox(parent)
        self.somBox.setObjectName("somBox")

        self.clusterizeLabel = QtWidgets.QLabel(self.somBox)
        self.clusterizeLabel.setObjectName('clusterizeLabel')

        self.clusterButton = QtWidgets.QPushButton(self.somBox)
        self.clusterButton.setCheckable(True)
        self.clusterButton.setChecked(False)
        self.clusterButton.setObjectName("clusterButton")

        self.clusterLabel = QtWidgets.QLabel(self.somBox)
        self.clusterLabel.setObjectName("clusterLabel")

        self.clusterComBox = QtWidgets.QComboBox(self.somBox)
        self.clusterComBox.setObjectName("clusterComBox")

        self.somMeshGridLine = QtWidgets.QLineEdit(self.somBox)
        self.somMeshGridLine.setAlignment(QtCore.Qt.AlignCenter)

        self.somMeshGridLabel = QtWidgets.QLabel(self.somBox)
        self.somMeshGridLabel.setAlignment(QtCore.Qt.AlignLeft)

        self.somShowBox = QtWidgets.QGroupBox(parent)
        self.somShowBox.setObjectName("somShowBox")
        self.showActMap = QtWidgets.QPushButton(self.somShowBox)
        self.showActMap.setCheckable(True)
        self.showActMap.setObjectName("showActMap")

        self.showDistMap = QtWidgets.QPushButton(self.somShowBox)
        self.showDistMap.setCheckable(True)
        self.showDistMap.setObjectName("showDistMap")

        self.diffClusters = QtWidgets.QPushButton(self.somShowBox)
        self.diffClusters.setCheckable(True)
        self.diffClusters.setObjectName("diffClusters")

        self.clusterSamplesLabel = QtWidgets.QLabel(self.somBox)
        self.clusterSamplesLabel.setObjectName("clusterSamplesLabel")
        self.clusterSamplesLabel.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse)

    def __setSOMLayout(self):
        """  """
        self.somLayout = QtWidgets.QGridLayout()
        self.somContainer = QtWidgets.QVBoxLayout(self.somBox)
        self.somContainer.setObjectName("somContainer")
        self.somContainer.addLayout(self.somLayout)

        spacerItemLabelStart = QtWidgets.QSpacerItem(
            7, 7, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        spacerItemLabelEnd = QtWidgets.QSpacerItem(
            7, 7, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        self.somLayout.addWidget(self.clusterizeLabel, 0, 0, 1, 1)
        self.somLayout.addWidget(self.clusterButton, 0, 1, 1, 1)

        self.somLayout.addWidget(
            self.somMeshGridLabel, 1, 0, 1, 1, QtCore.Qt.AlignVCenter)
        self.somLayout.addWidget(self.somMeshGridLine, 1, 1, 1, 1)

        self.somLayout.addWidget(self.clusterLabel, 2, 0, 1, 1)
        self.somLayout.addWidget(self.clusterComBox, 2, 1, 1, 1)

        self.somLayout.addItem(spacerItemLabelStart, 3, 0, 1, 2)
        self.somLayout.addWidget(self.clusterSamplesLabel, 4, 0, 1, 2)
        self.somLayout.addItem(spacerItemLabelEnd, 5, 0, 1, 2)

        self.somLayout.addWidget(self.somShowBox, 6, 0, 1, 2)
        self.somLayout.setObjectName("somLayout")

    def __setSOMShowLayout(self):
        """  """
        self.somShowLayout = QtWidgets.QGridLayout()
        self.somShowContainer = QtWidgets.QVBoxLayout(self.somShowBox)
        self.somShowContainer.setObjectName("somShowContainer")
        self.somShowContainer.addLayout(self.somShowLayout)

        self.somShowLayout.addWidget(self.showActMap, 0, 0, 1, 1)
        self.somShowLayout.addWidget(self.showDistMap, 1, 0, 1, 1)
        self.somShowLayout.addWidget(self.diffClusters, 2, 0, 1, 1)

        self.somShowLayout.setObjectName("somShowLayout")

    def updateClustersComboBox(self):
        """  """
        self.clusterComBox.clear()
        if self.R.Clusterize:
            clusterLabels = []
            totalSamples = 0

            for i in self.testClusters.keys():
                totalSamples += self.testClusters[i].shape[1] - 2

            for key in self.testClusters.keys():
                nSamples = self.testClusters[key].shape[1] - 2
                # percent = 100*(nSamples / totalSamples)
                percent = 100*(nSamples / totalSamples)

                if self.LANGUAGE == 'pt_br':
                    label = " Amostras"
                if self.LANGUAGE == 'en_us':
                    label = " Samples"
                else:
                    raise ValueError("Unknown language")

                clusterLabels.append("%s | %s %s | %.2f %%"%(key, nSamples, label, percent))

            self.clusterComBox.addItems(clusterLabels)
            self.updateClusterInfo()

    def updateClusterInfo(self):
        """  """
        nSamples = (self.getCurrentCluster().shape[1] - 2) < 1

        if self.LANGUAGE == 'pt_br':
            text = str(
                """
                <html>
                    <head/>
                        <body>
                            <b> Informações </b>
                            <br></br>
                            <p> Total de Amostras Clusterizadas   = %d </p>
                            <p> Média da Variância do Cluster     = %f </p>
                            <p> Média do Cluster                  = %f </p>
                            <p> Média do Desvio Padrão do Cluster = %f </p>
                            <p> Erro de Quantização do Cluster    = %f </p>
                            <p> Produto Interno Normalizado       = %f </p>
                        </body>
                </html>
                """%(
                    self.getCurrentCluster().shape[1] - 2,
                    round(self.getVarianceFromCluster(), 2),
                    round(self.getMeanFromCluster(), 2),
                    -1 if nSamples else round(self.getStdFromCluster(), 2),
                    -1 if nSamples else round(self.getQeFromCluster(), 2),
                    -1 if nSamples else round(self.getDotProductFromCluster(), 8)*100,
                )
            )

        elif self.LANGUAGE == 'en_us':
            text = str(
                """
                <html>
                    <head/>
                        <body>
                            <b> Informations </b>
                            <br></br>
                            <p> Total Clustered Samples               = %d </p>
                            <p> Mean of Variance of Cluster           = %f </p>
                            <p> Mean of Cluster                       = %f </p>
                            <p> Mean of Standard-Deviation of Cluster = %f </p>
                            <p> Quantization Error of Cluster         = %f </p>
                            <p> Dot Product Normalized                = %f </p>
                        </body>
                </html>
                """%(
                    self.getCurrentCluster().shape[1] - 2,
                    round(self.getVarianceFromCluster(), 2),
                    round(self.getMeanFromCluster(), 2),
                    -1 if nSamples else round(self.getStdFromCluster(), 2),
                    -1 if nSamples else round(self.getQeFromCluster(), 2),
                    -1 if nSamples else round(self.getDotProductFromCluster(), 8)*100,
                )
            )

            self.clusterSamplesLabel.setText(text)


    def connectWidgetGrid(self):
        """  """

        def splitGridString(grid):
            """  """
            if 'x' in grid:
                return grid.replace(' ', '').split('x')
            elif ',' in grid:
                return grid.replace(' ', '').split(',')
            elif ' ' in grid:
                return grid.split(' ')
            else:
                return [None, None]

        grid = splitGridString(str(self.somMeshGridLine.text()))
        self.somMesh[0] = int(grid[0]) if grid[0] is not None else None
        self.somMesh[1] = int(grid[1]) if grid[1] is not None else None

        self.connectSettingsSOM('grid', self.somMesh)

    def connectWidgetCluster(self):
        """  """
        try:
            cluster = eval(self.clusterComBox.currentText()[:7])
        except:
            cluster = (0, 0)

        self.connectSettingsSOM('cluster', cluster)
        self.updateClusterInfo()
        self.updateSampleShowComboBox()
        self.updateSamplePIDComboBox()

    def connectWidgetClusterize(self):
        """  """
        self.connectSettingsSOM('clusterize', self.clusterButton.isChecked())

        if self.clusterButton.isChecked():
            self.somShowBox.setVisible(True)
            self.clusterSamplesLabel.setVisible(True)
        else:
            self.somShowBox.setVisible(False)
            self.clusterSamplesLabel.setVisible(False)

        self.updateClustersComboBox()
        self.updateSampleShowComboBox()
        self.updateSamplePIDComboBox()

    def connectWidgetsSOM(self):
        """  """
        self.clusterButton.clicked.connect(
            lambda: self.connectWidgetClusterize())
        self.clusterComBox.activated.connect(
            lambda: self.connectWidgetCluster())
        self.somMeshGridLine.editingFinished.connect(
            lambda: self.connectWidgetGrid())
        self.showActMap.clicked.connect(
            lambda x: self.connectSettingsSOM("showActMap", x))
        self.showDistMap.clicked.connect(
            lambda x: self.connectSettingsSOM("showDistMap", x))
        self.diffClusters.clicked.connect(
            lambda x: self.connectSettingsSOM("diffClusters", x))

    def connectSettingsSOM(self, field, setting):
        """  """
        settings = self.loadSettings()
        if settings['som'][field] != setting:
            settings['som'][field] = setting
            self.saveSettings(settings)
            self.makePlot()

    def preloadEntrysSOM(self):
        """  """
        self.updateClustersComboBox()

        self.clusterButton.setChecked(self.R.Clusterize)
        self.showActMap.setChecked(self.R.showActMap)
        self.showDistMap.setChecked(self.R.showDistMap)
        self.diffClusters.setChecked(self.R.diffClusters)

        self.somShowBox.setVisible(self.R.Clusterize)
        self.clusterSamplesLabel.setVisible(self.R.Clusterize)

        self.somMeshGridLine.setText(str(self.R.Grid)[1:-1])
        if self.R.Clusterize:
            self.connectSettingsSOM('cluster', (0, 0))
            self.updateClustersComboBox()
            self.updateSampleShowComboBox()
            self.updateSamplePIDComboBox()
