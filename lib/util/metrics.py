import numpy as np


class Metrics:
    def __init__(self, source=None, target=None):
        """ Error metrics model
        
        Parameters
        ----------
            source (numpy.array or pandas.Series):
                Is the data source to calculate
                the difference. It can be a single array or an 2D matrix.

            target: numpy.array
                Is the model to compare the difference. The
                size must be the same as array rows size.
        """
        if target is not None:
            self.target = target
        if source is not None:
            self.source = source
    
    def set_target(self, target):
        """ Set target data """
        self.target = target

    def set_source(self, source):
        """ Set source data """
        self.source = source

    def MAE(self, source=None, normal=True):
        """ Measure - Mean Absolute Error

        font: https://link.springer.com/referenceworkentry/10.1007%2F978-0-387-30164-8_525
        
        This metric calculates the mean absolute difference
        between the destination point and its corresponding dimension
        in the source matrix.

        Return
        ------
            numpy:array
            Returns a matrix with the error of each point in
            relation to its corresponding ones in the source matrix.
        """
        if source is None and self.source is not None:
            source = self.source
                
        source = np.array(source)
        r = []
        for i, v in enumerate(source):
            if not normal:
                v = v[np.nan_to_num(v - self.target[i]) > 0]
            t = np.subtract(v, self.target[i])
            if t.size > 0:
                r.append(np.nanmean(np.abs(t)))
            else:
                r.append(0)
        return np.array(r)

    def MSE(self, source=None, normal=True):
        """ Measure - Mean Squared Error

        font: https://link.springer.com/referenceworkentry/10.1007%2F978-0-387-30164-8_528
        
        This metric calculates the mean squared difference
        between the destination point and its corresponding dimension
        in the source matrix.

        Return
        ------
            numpy:array
            Returns a matrix with the error of each point in
            relation to its corresponding ones in the source matrix.
        """
        if source is None and self.source is not None:
            source = self.source
        
        source = np.array(source)
        r = []
        for i, v in enumerate(source):
            if not normal:
                v = v[np.nan_to_num(v - self.target[i]) > 0]
            t = np.square(np.subtract(v, self.target[i]))
            if t.size > 0:
                r.append(np.nanmean(t))
            else:
                r.append(0)
        return np.array(r)

    def RMSE(self, source=None, normal=True):
        """ Measure - Root Mean Squared Error

        font: http://statweb.stanford.edu/~susan/courses/s60/split/node60.html
        
        This metric calculates the root mean squared difference
        between the destination point and its corresponding dimension
        in the source matrix.

        Return
        ------
            numpy:array
            Returns a matrix with the error of each point in
            relation to its corresponding ones in the source matrix.
        """
        return np.sqrt(self.MSE(source, normal))

    def QE(self, source=None, normal=True):
        """ Measure - Quantization Error or Root Sum Squared Error

        ** font: https://accendoreliability.com/root-sum-squared-tolerance-analysis-method/#:~:text=The%20root%20sum%20squared%20(RSS,dimensions%20near%20the%20tolerance%20limits.
        
        This metric calculates the root sum squared of the difference(RSS)
        between the destination point and its corresponding dimension in the
        source matrix. This metric is commonly used as array tolerance metric in
        various clustering methods.

        ** RSS assumes the normal distribution describes the variation of
        dimensions. The bell shaped curve is symmetrical and full described
        with two parameters, the mean, μ, and the standard deviation, σ.[¹]

        Return
        ------
            numpy:array
            Returns a matrix with the error of each point in
            relation to its corresponding ones in the source matrix.
        """
        if source is None and self.source is not None:
            source = self.source
        
        source = np.array(source)
        r = []
        for i, v in enumerate(source):
            if not normal:
                v = v[np.nan_to_num(v - self.target[i]) > 0]
            t = np.subtract(v, self.target[i])
            if t.size > 0:
                r.append(np.sqrt(np.sum(np.square(t))))
            else:
                r.append(0)
        return np.array(r)

    def MAPE(self, source=None, normal=True):
        """ Measure - Mean Absolute Percentage Error

        font: https://en.wikipedia.org/wiki/Mean_absolute_percentage_error
        
        This metric calculates the mean absolute percentage difference
        between the destination point and its corresponding dimension
        in the source matrix.

        Return
        ------
            numpy:array
            Returns a matrix with the error of each point in
            relation to its corresponding ones in the source matrix.
        """
        if source is None and self.source is not None:
            source = self.source
        
        source = np.array(source)
        r = []
        for i, v in enumerate(source):
            if not normal:
                v = v[np.nan_to_num(v - self.target[i]) > 0]
            t = abs(np.divide(np.subtract(v, self.target[i]),v))*100
            if t.size > 0:
                r.append(np.nanmean(t))
            else:
                r.append(0)
        return np.array(r)
