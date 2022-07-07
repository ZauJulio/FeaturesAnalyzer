import numpy as np


def MAE(array, yPredict, normal=False):
    """ MAE function
    font: https://en.wikipedia.org/wiki/Mean_absolute_error

    MAE is the average absolute difference between X and Y. Here, the X are
        every single value in array and Y are every single value in yPredict.

    Args:
        array (numpy.array or pandas.Series): Is the data source to calculate
        the difference. It can be a single array or an 2D matrix.

        yPredict (numpy.array): Is the model to compare the difference. The
        size must be the same as array rows size

    Returns:
        numpy.array: This contains the MAE for every value in passed array and
            yPredict.
    """
    resultMae = []

    for i, v in enumerate(array):
        if not normal:
            v = v[np.nan_to_num(v - yPredict[i]) > 0]
        t = abs(v - yPredict[i])
        if t.size > 0:
            resultMae.append(np.nanmean(t))
        else:
            resultMae.append(0)

    return np.array(resultMae)


def mobileMean(array, minutes):
    """ mobileMean

    mobileMean takes an array and a value (minutes). Then it calculates the
    mean for every minutes space and saves into a new array.
    That means, for example:

    Given an array: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    and minutes equal to 3, the behavior will be:

    mean(1), mean(1, 2), mean(1, 2, 3), mean(2, 3, 4)...

    this will repeat until all the array values pass, returning:
    numpy.array([1 , 1.5, 2 , 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5])

    Args:
        array (list, numpy.array, pandas.Series): Is a N size array, that will
            be the source for the mean calculations

        minutes (int): A step value that will determine how many values will be
            taken to calculate the means.

    Return:
        numpy.array: All values of passed array evalueated by a mean
            calculation.
    """
    if isinstance(array, list):
        array = np.array(array)

    mMean = np.array([])
    for i in range(array.size):
        if i >= minutes:
            actualPoint = i - minutes
        elif i >= 0:
            actualPoint = 0
        meanArray = np.array(array[actualPoint:i + 1])
        notNan = (~np.isnan(meanArray))
        meanArray = meanArray[notNan]
        mMean = np.append(mMean, np.mean(meanArray)
                          ) if meanArray is not None else 0

    return mMean


def mobileMedian(array, minutes):
    """ mobileMedian

    mobileMedian takes an array and a value (minutes). Then it calculates the
    median for every minutes space and saves into a new array.
    That means, for example:

    Given an array: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    and minutes equal to 3, the behavior will be:

    median(1), median(1, 2), median(1, 2, 3), median(2, 3, 4)...

    this will repeat until all the array values pass, returning:
    numpy.array([1 , 1.5, 2, 3, 4, 5, 6, 7, 8, 9])

    Args:
        array (list, numpy.array, pandas.Series): Is a N size array, that will
            be the source for the median calculations

        minutes (int): A step value that will determine how many values will be
            taken to calculate the medians.

    Return:
        numpy.array: All values of passed array evalueated by a median
            calculation.
    """
    if isinstance(array, list):
        array = np.array(array)

    mMedian = np.array([])
    for i in range(array.size):
        if i >= minutes:
            actualPoint = i - minutes
        elif i >= 0:
            actualPoint = 0
        meanArray = np.array(array[actualPoint:i + 1])
        notNan = (~np.isnan(meanArray))
        meanArray = meanArray[notNan]
        mMedian = np.append(mMedian, np.median(meanArray))

    return mMedian


def integrator(y, signal):
    """ integrator function
    font: https://en.wikipedia.org/wiki/Numerical_integration

    This function takes two arrays and calcule the area between then. It uses
        numerical integration. For every index is calculated the rectangle
        area.
        This rectangle is made by:

        base = space between values.
            **Assuming that the passed arrays are temporal, the base will be
                always equal to 1
        height = difference between y[i] and signal[i].

        with this values is calculated: base x height, or, just height if the
            base is equal to 1. The result are added to another array.

    Args:
        y (list, numpy.array, pandas.Series): Is the source data to calculate
            the difference.

        signal (list, numpy.array, pandas.Series): The data to take a
            reference.

    Returns:
        (list, numpy.array, pandas.Series): All values of this array are the
            accumulated data from integral in every single index.
    """
    x = 0
    integ = []
    for i in range(y.size):
        x += y[i] - signal[i]
        integ.append(x)
    return integ


def _dPoint(y0, y1):
    """ _dPoint

    Auxiliar function to derivative. Check this one.
    """
    if not np.isnan(y0) and not np.isnan(y1):
        return (y1 - y0)
    return np.nan


def derivative(y):
    """ derivative function
    font: https://en.wikipedia.org/wiki/Numerical_differentiation

    This function uses the Numerical differentiation theory. It takes every
        value of passed y and calculate the tangent inclination for every index
        using:
            (f(x + h) - f(x))/h
    Assuming that the passed array is a temporal serie, the h value will always
        be 1, so the x+1 will be the next value and the division is not
        necessary.

    Args:
        y (list, numpy.array, pandas.Series): This is the array to calculate
        the derivative.

    Returns:
        (list, numpy.array, pandas.Series): Array with derivative result.
    """
    d = [_dPoint(y[i], y[i + 1]) for i in range(y.size - 1)]
    d.append(d[-1])
    return d


def dot(x, y):
    """ Dot product normalized

    Args:
        x and y (list, numpy.array, pandas.Series): A two-dimensional array.

    Returns:
        (float): Returns the internal product realized with
        the normalized inputs.
    """
    # Check shape
    lx = x/np.linalg.norm(x, 2)
    ly = y/np.linalg.norm(y, 2)

    return np.array([np.dot(lx_i, ly) for lx_i in lx])
