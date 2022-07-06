import sys

sys.path.append("../")

from lib.util import numlib


class PIDController:

    def updatePID(self) -> None:
        """ Update PID data

        Returns
        -------
        None
        """

        if self.R.Derivative:
            try:
                self.derivative = self.getDerivative()
            except KeyError:
                print("PID: Error when calculating derivative. Not Raise.")
                pass
        if self.R.Integral or self.R.IntegralParameters:
            try:
                self.integral = self.getIntegral()
            except KeyError:
                print("PID: Error when calculating integral. Not Raise.")
                pass

    def getDerivative(self) -> list:
        """ Derivative

        Returns
        -------
            Derivative of data of test(if self.R.ShowTest) or self.DataTrain
        """
        data = self.dataTest if self.R.ShowTest else self.dataTrain
        if self.R.PIDSample in data:
            return numlib.derivative(data[self.R.PIDSample])

    def getIntegral(self) -> list:
        """ Integral

        Returns
        -------
            Integral of data of test(if self.R.ShowTest) or self.DataTrain
        """
        data = self.dataTest if self.R.ShowTest else self.dataTrain
        if self.R.PIDSample in data:
            day = data[self.R.PIDSample]
            self.sampleSignal = numlib.mobileMean(day, len(day))
            self.sampleMobMean = numlib.mobileMean(day, self.R.MobMeanMin)
            return numlib.integrator(self.sampleMobMean, self.sampleSignal)
