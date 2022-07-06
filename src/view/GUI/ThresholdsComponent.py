from PyQt5 import QtCore, QtWidgets


class ThresholdsComponent(object):

    def __init__(self, parent):
        """  """
        self.__thresholdBox(parent)

        self.__feature = "models"
        self.__source = "linear"
        self.__metric = "MAE"
        self.__option = "min"
        self.__entry = "absolute"
        self.__filter = ""

        self.__reload()
        self.thresholdLayout()
        self.swapHide()

    def __thresholdBox(self, parent):
        """  """
        self.thresholdBox = QtWidgets.QGroupBox(parent)

        # Feature Selection
        self.featureLabel = QtWidgets.QLabel(self.thresholdBox)
        self.featureList = QtWidgets.QComboBox(self.thresholdBox)
        self.featureList.addItems(["Models", "Metrics", "Both"])
        ##############################################################

        # Source Selection
        self.sourceLabel = QtWidgets.QLabel("Source:", self.thresholdBox)
        self.sourceList = QtWidgets.QComboBox(self.thresholdBox)
        self.sourceList.addItems(["Linear", "RANSAC", "RLM", "Weights", "All"])
        ##############################################################

        # Metric Selection
        self.metricLabel = QtWidgets.QLabel(self.thresholdBox)
        self.metricLabel.setVisible(False)
        #
        self.metricList = QtWidgets.QComboBox(self.thresholdBox)
        self.metricList.addItems(["MAE", "RMSE", "QE", "MAPE", "All"])
        self.metricList.setVisible(False)
        ##############################################################

        # Filter Selection
        self.filterLabel = QtWidgets.QLabel(self.thresholdBox)
        self.filterLabel.setVisible(False)
        #
        self.filterList = QtWidgets.QComboBox(self.thresholdBox)
        self.filterList.addItems(["", "Savitzky–Golay"])
        self.filterList.setVisible(False)
        #
        self.filterShow = QtWidgets.QPushButton("Show", self.thresholdBox)
        self.filterShow.setCheckable(True)
        self.filterShow.setVisible(False)
        #
        self.filterOutlier = QtWidgets.QPushButton("Outlier")
        self.filterOutlier.setCheckable(True)
        self.filterOutlier.setVisible(False)
        ##############################################################

        # General buttons of Source das Metrics
        self.sourceShow = QtWidgets.QPushButton("Show", self.thresholdBox)
        self.sourceShow.setCheckable(True)
        #
        self.sourceOutlier = QtWidgets.QPushButton("Outlier")
        self.sourceOutlier.setCheckable(True)
        #
        self.metricNormal = QtWidgets.QPushButton("Normal", self.thresholdBox)
        self.metricNormal.setCheckable(True)
        self.metricNormal.setVisible(False)
        ##############################################################

        # Options Settings
        self.optionsLabel = QtWidgets.QLabel("Option:", self.thresholdBox)
        self.optionsList = QtWidgets.QComboBox(self.thresholdBox)
        self.optionsList.addItems(["Min", "Mean", "Max"])
        ##############################################################

        # Entrys settings
        self.entriesLabel = QtWidgets.QLabel("Entry:", self.thresholdBox)
        self.entriesLabel.setVisible(False)
        #
        self.entriesList = QtWidgets.QComboBox(self.thresholdBox)
        self.entriesList.addItems(["Absolute", "Relative"])
        self.entriesList.setVisible(False)
        # General buttons for combining thresholds
        self.entryShow = QtWidgets.QPushButton("Absolute", self.thresholdBox)
        self.entryShow.setCheckable(True)
        #
        self.entryOutlier = QtWidgets.QPushButton("Outlier", self.thresholdBox)
        self.entryOutlier.setCheckable(True)

    def thresholdLayout(self):
        """  """
        self.thresholdLayout = QtWidgets.QGridLayout()
        self.thresholdContainer = QtWidgets.QVBoxLayout(self.thresholdBox)
        self.thresholdContainer.addLayout(self.thresholdLayout)

        # Features list
        self.thresholdLayout.addWidget(self.featureLabel, 0, 0, 1, 1)
        self.thresholdLayout.addWidget(self.featureList, 0, 1, 1, 4)
        ##############################################################
        # Source list
        self.thresholdLayout.addWidget(self.sourceLabel, 1, 0, 1, 1)
        self.thresholdLayout.addWidget(self.sourceList, 1, 1, 1, 4)
        ##############################################################
        # Metrics list
        self.thresholdLayout.addWidget(self.metricLabel, 2, 0, 1, 1)
        self.thresholdLayout.addWidget(self.metricList, 2, 1, 1, 4)
        ##############################################################
        # General source/metric buttons
        self.thresholdLayout.addWidget(self.metricNormal, 3, 0, 1, 1)
        self.thresholdLayout.addWidget(self.sourceShow, 3, 1, 1, 2)
        self.thresholdLayout.addWidget(self.sourceOutlier, 3, 3, 1, 2)
        ##############################################################

        spacerItemBefore = QtWidgets.QSpacerItem(
            20,
            20,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Fixed
        )

        # Options list, Min, Mean, Max
        self.thresholdLayout.addItem(spacerItemBefore, 4, 0, 1, 4)
        self.thresholdLayout.addWidget(self.optionsLabel, 5, 0, 1, 1)
        self.thresholdLayout.addWidget(self.optionsList, 5, 1, 1, 4)
        ##############################################################
        # Entry, absolute, relative
        self.thresholdLayout.addWidget(self.entriesLabel, 6, 0, 1, 1)
        self.thresholdLayout.addWidget(self.entriesList, 6, 1, 1, 4)
        ##############################################################
        # Entry buttons
        self.thresholdLayout.addWidget(self.entryShow, 7, 1, 1, 2)
        self.thresholdLayout.addWidget(self.entryOutlier, 7, 3, 1, 2)

        spacerItemBeforeEntrys = QtWidgets.QSpacerItem(
            20,
            20,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Fixed
        )
        
        # Filter list
        self.thresholdLayout.addItem(spacerItemBeforeEntrys, 8, 0, 1, 4)
        self.thresholdLayout.addWidget(self.filterLabel, 9, 0, 1, 1)
        self.thresholdLayout.addWidget(self.filterList, 9, 1, 1, 4)
        # Filter buttons
        self.thresholdLayout.addWidget(self.filterShow, 10, 1, 1, 2)
        self.thresholdLayout.addWidget(self.filterOutlier, 10, 3, 1, 2)


    def swapHide(self):
        """ Hide by occurrence """

        def metricWidgetsHide(self, featureIndex):
            """ Show metric options in the corresponding feature """
            if featureIndex == 1:
                self.metricLabel.setVisible(True)
                self.metricList.setVisible(True)
            else:
                self.metricLabel.setVisible(False)
                self.metricList.setVisible(False)

        def sourceWidgetsHide(self, featureIndex):
            """ Hide source options in feature Both """
            if featureIndex != 2:
                self.sourceList.setVisible(True)
                self.sourceLabel.setVisible(True)
            else:
                self.sourceList.setVisible(False)
                self.sourceLabel.setVisible(False)

        def entryHide(self):
            """ Show combination options only when the feature is Both or
            the Source or Metric is All """
            if (self.sourceList.currentIndex() == 4 or self.metricList.currentIndex() == 4) and (self.featureList.currentIndex() != 0):
                self.entriesLabel.setVisible(True)
                self.entriesList.setVisible(True)

                self.sourceShow.setVisible(False)
                self.sourceOutlier.setVisible(False)
            else:
                self.entriesLabel.setVisible(False)
                self.entriesList.setVisible(False)

                self.sourceShow.setVisible(True)
                self.sourceOutlier.setVisible(True)

        def filterHide(self):
            """ Show filter options """
            if (self.sourceList.currentIndex() != 4 and self.metricList.currentIndex() != 4) and (self.featureList.currentIndex() != 0):
                self.filterLabel.setVisible(True)
                self.filterList.setVisible(True)

                self.filterShow.setVisible(True)
                self.filterOutlier.setVisible(True)
            else:
                self.filterLabel.setVisible(False)
                self.filterList.setVisible(False)

                self.filterShow.setVisible(False)
                self.filterOutlier.setVisible(False)

        def hideNormalButton(self):
            """ Hide threshold combination options """
            if (self.featureList.currentIndex() == 0) or \
                (self.featureList.currentIndex() == 2) or \
                    (self.sourceList.currentIndex() == 4) or \
                    (self.metricList.currentIndex() == 4):
                self.metricNormal.setVisible(False)
            else:
                self.metricNormal.setVisible(True)

        # Show/Hide metric options
        self.featureList.currentIndexChanged.connect(
            lambda index: (
                sourceWidgetsHide(self, index),
                metricWidgetsHide(self, index),
                entryHide(self),
                filterHide(self)
            ))

        # Hide Hide threshold combination options
        self.sourceList.currentIndexChanged.connect(lambda x: (entryHide(self), filterHide(self)))
        self.metricList.currentIndexChanged.connect(lambda x: (entryHide(self), filterHide(self)))

        # Hide normal button from metrics
        self.featureList.currentIndexChanged.connect(
            lambda x: hideNormalButton(self))
        self.sourceList.currentIndexChanged.connect(
            lambda x: hideNormalButton(self))
        self.metricList.currentIndexChanged.connect(
            lambda x: hideNormalButton(self))

    def connectWidgetsThresholds(self):
        """ Connect list's and widgets buttons """

        def __setFeature(self, index: int) -> None:
            """ Change current feature """
            self.__feature = __features[index].lower()

        def __setSource(self, index: int) -> None:
            """ Change current source """
            self.__source = __sources[index].lower()

        def __setMetric(self, index: int) -> None:
            """ Change current metric """
            self.__metric = __metrics[index]

        def __setFilter(self, index: int) -> None:
            """ Change current metric """
            self.__filter = __filters[index]

        def __setOption(self, index: int) -> None:
            """ Change current option"""
            self.__option = __options[index].lower()

        def __setEntry(self, index: int) -> None:
            """ Change current entry """
            self.__entry = __entries[index].lower()

        __features = ["Models", "Metrics", "Both"]
        __sources = ["Linear", "RANSAC", "RLM", "weights", "all"]
        __metrics = ["MAE", "RMSE", "QE", "MAPE", "all"]
        __filters = [""]+self.thrFilters
        __options = ["Min", "Mean", "Max"]
        __entries = ["Absolute", "Relative"]

        # Feature Selection
        self.featureList.currentIndexChanged.connect(
            lambda index: (__setFeature(self, index), self.__reload()))
        self.sourceList.currentIndexChanged.connect(
            lambda index: (__setSource(self, index), self.__reload()))
        self.metricList.currentIndexChanged.connect(
            lambda index: (__setMetric(self, index), self.__reload()))
        self.filterList.currentIndexChanged.connect(
            lambda index: (__setFilter(self, index), self.__reload()))
        self.optionsList.currentIndexChanged.connect(
            lambda index: (__setOption(self, index), self.__reload()))
        self.entriesList.currentIndexChanged.connect(
            lambda index: (__setEntry(self, index), self.__reload()))

        # Connect source/metric buttons
        self.sourceShow.clicked.connect(
            lambda: self.__setThresholdsUse("show", self.sourceShow.isChecked()))
        self.sourceOutlier.clicked.connect(
            lambda: self.__setThresholdsUse("outlier", self.sourceOutlier.isChecked()))
        self.filterShow.clicked.connect(
            lambda: self.__setThresholdsUse("show", self.filterShow.isChecked(), inFilter=True))
        self.filterOutlier.clicked.connect(
            lambda: self.__setThresholdsUse("outlier", self.filterOutlier.isChecked(), inFilter=True))

        self.metricNormal.clicked.connect(
            lambda: self.__setThresholdsUse("normal", self.sourceOutlier.isChecked()))

        # Connect combining buttons
        self.entryShow.clicked.connect(
            lambda: self.__setThresholdsUse("show", self.entryShow.isChecked(), inOption=True))
        self.entryOutlier.clicked.connect(
            lambda: self.__setThresholdsUse("outlier", self.entryOutlier.isChecked(), inOption=True))

    def __setThresholdsUse(self, use: str, check: bool, inOption: bool = False, inFilter:bool = False, updateGraph: bool = True) -> None:
        """ Connect Show Outlier button for sources and metrics options

        Parameters
        ----------
            use: str()
                ['show', 'outlier']
            check: bool()
                input validation
            inOption: str(), default=False
                If true, change the Show and Outlier options to absolute and
                relative, change the Show and Outlier options for the model
                and metric.
            updateGraph: bool(), default=True
        """
        if self.__feature == "models":
            if inOption:
                if self.__source == "all" or self.__metric == "all":
                    self.thresholdSettings[self.__feature][self.__source][self.__option][self.__entry][use] = check
                else:
                    self.thresholdSettings[self.__feature][self.__source][self.__option][use] = check
            else:
                self.thresholdSettings[self.__feature][self.__source][use] = check

        elif self.__feature == "metrics":
            if inOption:
                if self.__source == "all" or self.__metric == "all":
                    self.thresholdSettings[self.__feature][self.__source][self.__metric][self.__option][self.__entry][use] = check
                else:
                    self.thresholdSettings[self.__feature][self.__source][self.__metric][self.__option][use] = check
            elif inFilter and self.__filter != "":
                self.thresholdSettings[self.__feature][self.__source][self.__metric]["filters"][self.__filter][use] = check
            else:
                self.thresholdSettings[self.__feature][self.__source][self.__metric][use] = check

        elif self.__feature == "both":
            self.thresholdSettings[self.__feature][self.__option][self.__entry][use] = check

        if updateGraph:
            self.saveSettings()
            self.makePlot()

    def __getSourceUse(self, use: str) -> bool:
        """ Returns the validity of the use as Show or Outlier """
        if self.__feature == "models":
            return self.thresholdSettings[self.__feature][self.__source][use]
        elif self.__feature == "metrics":
            return self.thresholdSettings[self.__feature][self.__source][self.__metric][use]

    def __getMetricNormalParm(self) -> bool:
        """ Returns the validity of the normal parameter of the current model/metric """
        return self.thresholdSettings[self.__feature][self.__source][self.__metric]["normal"]

    def __getThresholdsEntry(self, use: str, inFilter:bool=False) -> bool:
        """ Returns the selected usage options """
        if inFilter and (self.__feature == "metrics") and (self.__filter != '') and (self.__source != "all") and (self.__metric != "all"):
            return self.thresholdSettings[self.__feature][self.__source][self.__metric]["filters"][self.__filter][use]

        # Return option from all used models
        if self.__feature == "models" and self.__source == "all":
            return self.thresholdSettings[self.__feature][self.__source][self.__option][self.__entry][use]

        # Return option from single models
        if self.__feature == "models" and self.__source != "all":
            return self.thresholdSettings[self.__feature][self.__source][self.__option][use]

        # Return option from single threshold
        if self.__feature == "metrics" and self.__source != "all" and self.__metric != "all":
            return self.thresholdSettings[self.__feature][self.__source][self.__metric][self.__option][use]

        # Return both threshold option
        if self.__feature == "both":
            return self.thresholdSettings[self.__feature][self.__option][self.__entry][use]

        # Return threshold option for all models and/or metrics
        if self.__source == "all" or self.__metric == "all":
            return self.thresholdSettings[self.__feature][self.__source][self.__metric][self.__option][self.__entry][use]

    def __reload(self) -> None:
        """ Update buttons settings """
        if self.__source != "all" and self.__metric != "all" and self.__feature != "both":
            self.sourceShow.setChecked(self.__getSourceUse("show"))
            self.sourceOutlier.setChecked(self.__getSourceUse("outlier"))

        if self.__feature == "metrics" and not(self.__source == "all" or self.__metric == "all"):
            self.metricNormal.setChecked(self.__getMetricNormalParm())

        self.entryShow.setChecked(self.__getThresholdsEntry("show"))
        self.entryOutlier.setChecked(self.__getThresholdsEntry("outlier"))
        
        self.filterShow.setChecked(self.__getThresholdsEntry("show", inFilter=True))
        self.filterOutlier.setChecked(self.__getThresholdsEntry("outlier", inFilter=True))
