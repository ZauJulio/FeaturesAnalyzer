import datetime as dt
import sqlite3
import os
import sys

from numpy import NaN, array
from pandas import DataFrame, read_csv

sys.path.append('../../')
from lib.util import path, timelib

USAGE = """
    USAGE: python3 tables.py <saveDir> <dumpDir> <field> <days>

    Ex.: python3 tables.py ../../data/tables/days/ ../../data/dump/dump-2019-09-24-21-31-31.csv [P1, Q1, FPA] [segunda, terca]
"""


class Days:
    def __init__(self, saveDir=path.tables+path.bar,
                dump=path.dump+'dump-2019-09-24-21-31-31.csv',
                field=['P1','P2', 'P3', 'Q1', 'Q2', 'Q3', 'FPA', 'FPB', 'FPC'],
                days=timelib.weekdaysEN):
        """ Table generator
        Args:

        dump: str()
            Path to dump file, by default with the highest dump.
            Ex.: data/dump/dump-2019-09-24-21-31-31.csv -- Default
            The path varies depending on where the main code starts.add()
        saveDir: str()
            Path to save all tables.
            Ex.: data/tables/days/ -- Default
            The path varies depending on where the main code starts.add()
            Do not pass any parameters or pass any equivalent to False that
            the table will not be saved.
        field: str()
            Fild by filter the dump. P1, P2, P3, Q1, Q2, Q3, FPA, FPB, FPC.
            Ex.: ['P1', 'Q1', 'FPA']
        days: list()
            List with day or days to generate the tables.
            Ex.: ['segunda'] or ['segunda','terça','sexta']

        Without returns.
        """
        self.dataPoints = None
        self.days = [timelib.translate_weekday(day) for day in list(days)]
        self.fields = list(field)
        self.saveDir = saveDir
        self.read(dump)
        self.dumpID(dump)
        for self.field in self.fields:
            for self.indDay, self.weekday in enumerate(self.days):
                self.table = {}
                self.initDict()
                self.dataCorrection()
                self.to_DataFrame()
                self.save()

    def read(self, dump):
        """
        """
        try:
            self.df = read_csv(dump)
        except:
            return ValueError('Cannot read file.')

    def dumpID(self, dump):
        """ Selects only the source dump name
        """
        self.dump = os.path.basename(dump)[:-4]

    def checkMinute(self, i):
        """ Checks and corrects the lack of minutes and
            add correct minute from field
        Args:
        i: int()
            Index by datetime in timestamp.
        """
        key = str(self.day.date())
        if key not in self.table:
            self.table[key] = [(self.df[self.field][i], self.timing)]
        else:
            self.table[key].append((self.df[self.field][i], self.timing))

    def updateHour(self):
        """ Updates the time based on the current DB time
        """
        self.timing = self.day.time().replace(second=0)
        if self.timing > self.maxHour:
            self.maxHour = self.timing
        if self.timing < self.minHour:
            self.minHour = self.timing

    def initHour(self):
        """ Starts the maximum and minimum time
        """
        self.minHour = dt.time(23, 59, 59)
        self.maxHour = dt.time(0, 0, 0)

    def initDict(self):
        """ Init dictionary table with fild value and timing
        """
        self.initHour()
        for i, self.day in enumerate(self.timestamps):
            if self.day.weekday() == timelib.weekday(self.weekday):
                self.updateHour()
                self.checkMinute(i)

    def schedules(self):
        """ Starts the time list corresponding to minHour and maxHour
        """
        self.hours = timelib.linspace_time(self.minHour.replace(second=0), self.maxHour.replace(second=0))

    def initMinute(self):
        """
        """
        self.tableM = timelib.minute_from_time(self.table[self.date][self.idx][1])
        self.hoursM = timelib.minute_from_time(self.hour)

    def checkSchedule(self):
        """
        """
        if self.idx < len(self.table[self.date]):
            self.initMinute()
            if self.hoursM < self.tableM:
                self.tableDate.append((NaN, self.hour))
            elif self.hoursM > self.tableM:
                self.tableDate.append((self.table[self.date][self.idx][0], self.hour))
                self.idx += 1
            else:
                self.tableDate.append(self.table[self.date][self.idx])
                self.idx += 1
        else:
            self.tableDate.append((NaN, self.hour))

    def dataCorrection(self):
        """
        """
        self.schedules()
        for self.date in self.table:
            self.idx = 0
            self.tableDate = []
            for _, self.hour in enumerate(self.hours):
                if self.idx < len(self.table[self.date]):
                    self.checkSchedule()
                else:
                    self.tableDate.append((NaN, self.hour))
            self.table[self.date] = self.tableDate[:]

    @property
    def timestamps(self):
        """ Return list of datetime from timestamps
        """
        if self.dataPoints is None:
            self.dataPoints = [timelib.datetime_from_timestamp(x) for x in self.df['time']]
            return self.dataPoints
        return self.dataPoints

    def to_DataFrame(self):
        """ Convert dic to pandas.DataFrame with line
            index in date-time
        """
        for date in self.table:
            self.table[date] = array([x[0] for x in self.table[date]])
        self.table = DataFrame.from_dict(self.table, orient='index').T
        self.table.insert(0, 'hora', self.hours)
        self.table.set_index('hora', drop=True, inplace=True)

    def save(self):
        """ Save new table in sqlite3 file """
        if self.saveDir:
            dir = self.saveDir+self.dump+path.bar
            if not os.path.isdir(dir):
                os.mkdir(dir)

            conn = sqlite3.connect(dir+self.weekday+'.db')

            self.table.to_sql(self.field, con=conn, if_exists="replace", index_label='time')


if  __name__ == "__main__":
    check_list = lambda x: '[' in x.split('=')[1] and ']' in x.split('=')[1]
    split_list = lambda x: x[1:-1].split(',')

    saveDir = sys.argv[1]
    dumpDir = sys.argv[2]
    field = split_list(sys.argv[3])
    days = split_list(sys.argv[4])

    Days(saveDir, dumpDir, field, days)
