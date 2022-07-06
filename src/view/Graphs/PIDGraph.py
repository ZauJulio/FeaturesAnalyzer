

class PIDGraph:
    def plotPID(self):
        """  """
        self.samplePIDFound = False
        
        if self.availablePID:
            self.__plotDerivative()
            self.__plotIntegral()
            self.__plotPIDSample(self.getData())
            self.__plotIntegralParameters()
            self.__plotIntegralParametersFill()

    def __plotDerivative(self):
        """  """
        if self.R.Derivative:
            self.subplots[2] += 1
            self.ax = self.fig.add_subplot(*self.subplots)

            if self.LANGUAGE == 'en_us':
                label = "Derivative"
            elif self.LANGUAGE == 'pt_br':
                label = "Derivada"


            self.ax.plot(
                self.time,
                self.derivative,
                label=label
            )
            self.ax.set_xlabel('Time' if self.LANGUAGE == 'en_us' else 'Hora')
            self.ax.legend()

    def __plotIntegral(self):
        """  """
        if self.R.Integral:
            self.subplots[2] += 1
            self.ax = self.fig.add_subplot(*self.subplots)
            self.ax.plot(
                self.time,
                self.integral,
                label='Integral'
            )
            self.ax.set_xlabel('Time' if self.LANGUAGE == 'en_us' else 'Hora')
            self.ax.legend()

    def __plotPIDSample(self, data):
        """  """
        if self.R.PIDSample in data:
            self.samplePIDFound = True

            self.ax.plot(
                self.time,
                data[self.R.PIDSample], 'o',
                color='midnightblue',
                markersize=4.5,
                markeredgewidth=0,
            )

    def __plotIntegralParameters(self):
        """  """
        if self.R.IntegralParameters:

            if self.LANGUAGE == 'en_us':
                label = "Accumulated Mean"
            elif self.LANGUAGE == 'pt_br':
                label = "Média Acumulada"


            # Mobile Mean
            self.ax.plot(
                self.time,
                self.sampleMobMean,
                color='lime',
                markersize=5,
                alpha=0.5,
                label=label
            )

            if self.LANGUAGE == 'en_us':
                label = "Mobile Mean"
            elif self.LANGUAGE == 'pt_br':
                label = "Média Móvel"

            # Acc Mean
            self.ax.plot(
                self.time,
                self.sampleSignal,
                color='cyan',
                markersize=5,
                alpha=0.5,
                label=label
            )

    def __plotIntegralParametersFill(self):
        """  """
        if self.R.FillBetween:
            self.ax.fill_between(
                self.time,
                self.sampleMobMean,
                self.sampleSignal,
                where=self.sampleMobMean > self.sampleSignal, facecolor='red',
                alpha=0.2
            )

            self.ax.fill_between(
                self.time,
                self.sampleMobMean,
                self.sampleSignal,
                where=self.sampleMobMean < self.sampleSignal, facecolor='green',
                alpha=0.2
            )
