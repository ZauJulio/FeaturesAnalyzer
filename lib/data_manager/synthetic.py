import calendar
import os
import sys
from datetime import time
from math import *

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from lib.util.path import bar, tables_synthetic
from lib.util.timelib import linspace_time, time_from_str

USAGE = """
    USAGE: python3 synthetic.py <begin> <end> <save> <dir> <show>

    Ex.: python3 synthetic.py 22:10 24:59 True ../../tables/synthetic/ False
"""


def synthetic(func, begin='00:00', end='23:59', save=True, dir=tables_synthetic, show=False):
    """ Synthetic data generator by function
    Args:

    func: str()
    begin: str()
        Start time for synthesis.
    end: str()
        Final time for synthesis.
    save: bool()
    dir: str()
        Path to save tabels.
    show: bool()
    """
    dir = dir+func+bar
    begin = time_from_str(begin)
    end = time_from_str(end)

    space = time2min(end) - time2min(begin) + 1

    horas = linspace_time(begin, end)

    dataFrames = [{}, {}, {}, {}, {}]

    for mes in range(3, 7):
        for day in calendar.Calendar().itermonthdates(2019, mes):
            if day.month == mes:
                if day.weekday() != 5 and day.weekday() != 6:
                    dataFrames[int(day.weekday())][str(day)] = syntheticData(space, func)
    if save:
        days = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
        for i, day in enumerate(days):
            df = pd.DataFrame(dataFrames[i])
            df.insert(0, 'hora', horas)
            try:
                os.mkdir(dir)
            except FileExistsError:
                pass
            if not os.path.isfile(dir+'tabela_'+day+'.csv'):
                try:
                    df.to_csv(dir+'tabela_'+day+'.csv', index=False)
                except ValueError:
                    return ValueError('Could not create synthetic data DataFrame.')

    if show:
        for day in dataFrames:
            df = pd.DataFrame(day)
            plt.plot(horas, df, 'o')
            plt.show()

def time2min(hm):
    """ Returns hour in minute """
    return int(hm.hour) * 60 + int(hm.minute)

def putRandomNan(data):
    """  """
    nans = np.random.randint(0, len(data), 20)
    for i in nans:
        data[i] = np.nan

    return np.array(data)

def translate(data):
    """  """
    while data[data < 0].size != 0:
        data = data + 1
    return data

def syntheticData(space, func):
    """  """
    a = np.linspace(-5, 5, space)
    a = [eval(func) for x in a]
    a = a+np.random.randint(1, 50, space)
    a = translate(a)
    a = putRandomNan(a)
    return a


if  __name__ == "__main__":
    begin = sys.argv[1]
    end = sys.argv[2]
    save = eval(sys.argv[3])
    Dir = sys.argv[4]
    show = eval(sys.argv[5])

    synthetic(begin, end, save, Dir, show)
