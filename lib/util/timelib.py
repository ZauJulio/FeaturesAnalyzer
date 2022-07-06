import datetime
import time

import numpy as np
from pandas import date_range

weekdays = ['segunda', 'terca', 'quarta',
            'quinta', 'sexta', 'sabado',
            'domingo']
weekdaysEN = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday',
            'sunday']

""" list of strings: This variable is used for weekdays iteraction

From 0 to 6, it has all weekday names in portuguese and without accents
"""

months = [
    'janeiro', 'fevereiro', 'marco',
    'abril', 'maio', 'junho',
    'julho', 'agosto', 'setembro',
    'outubro', 'novembro', 'dezembro']
""" list of strings: This variable is used for months iteraction

From 0 to 11, it has all month names in portuguese and without accents
"""

#            [class_start_data, class_end_date]
semester2018_1 = ["2018-04-09", "2018-08-06"]
semester2018_2 = ["2018-08-20", "2018-12-19"]
semester2019_1 = ["2019-03-11", "2019-07-08"]
semester2019_2 = ["2019-08-06", "2019-12-07"]
""" lists of strings: This variables keep semesters information

When using any of this variables, you got the start data and end date of called
semester.
"""


def strtime_to_minute(hours):
    """ strtime_to_minute: This function receives one time string array and
    returns one array with referred minute in the day.

    for a ['20:34', '15:01'] it returns [20*60 + 34, 15*60 + 1] == [1234, 901]

    Args:
        hours (list of strings): List elements must respect the following
        pattern: "%H:%M"
        The middle character can be anything, but has to be 1 character

    Returns:
        (numpy.array): List of all processed elements from passed array.
    """
    minutes = list(map(lambda x: int(x[:2]) * 60 + int(x[3:5]), hours))
    return np.array(minutes)


def time_to_minute(hours):
    """ time_to_minute: This function receives one datetime.time array and
    returns one array with referred minute in the day.

    for a [datetime.time(20, 34), datetime.time(15, 01)]
    it returns [20*60 + 34, 15*60 + 1] == [1234, 901]

    Args:
        hours (list of datetime.time): List elements must be datetime.time

    Returns:
        (numpy.array): List of all processed elements from passed array.
    """
    minutes = list(map(lambda x: x.hour * 60 + x.minute, hours))
    return np.array(minutes)


def minute_to_time(minutes):
    """minute_to_time: Opposite to strtime_to_minute, this function receives
    a list of minutes and returns every element in datetime.time

    Args:
        minutes (list of ints or floats): It's a list of ints from 0 to 1239
        following the size of one day

    Returns:
        (numpy.array): Array of datetime.time elements
    """
    timeList = [datetime.time(int(i) // 60, int(i) % 60) for i in minutes]
    return np.array(timeList)


def hour_series(start_hour, end_hour):
    """ hour_series: A function that gets a start point and a end point and
    returns an array of datetime.time from start to end

    calling hour_series(10, 11), it will returns:
    [datetime.time(10, 0), datetime.time(10, 1)... datetime.time(10, 59)]

    Args:
        start_hour (int): it's a int value referring to the start hour, so
        if you want to start from 22:00 just pass this parameter as 22
        end_hour (int): same as start, but refer to end point

    Returns:
        (numpy.array): This array has datetime.time elements from start_hour to
        end_hour
    """
    arr = [
        datetime.time(hour, minute)
        for hour in range(start_hour, end_hour)
        for minute in range(60)]
    return np.array(arr)


def minute_from_time(t):
    """ minute_from_time: Return a day minute from a passed datetime.time

    That means that if you call minute_from_time(datetime.time(23, 59)) it
    will return 1239

    Args:
        t (datetime.time): It has to be a datetime.time to work
    Returns:
        (int): A int value representing the minute of the day for the passed
        value
    """
    return t.hour * 60 + t.minute


def weekday_from_timestamp(timestamp):
    """ weekday_from_timestamp: This function return a weekday value (0-6)
    from a passed timestamp

    Args:
        timestamp (int or float): A UNIX timestamp
    Returns:
        (int): A value of the weekday for the passed timestamp
    """
    return datetime.datetime.fromtimestamp(timestamp).weekday()


def datetime_from_timestamp(timestamp):
    """ datetime_from_timestamp: Returns a datetime object from the passed
    timestamp

    Args:
        timestamp (int or float): A UNIX timestamp

    Returns:
        (datetime.datetime): Returns the datetime object from the timestamp
        in Brazil West UTC
    """
    # format = "%Y-%m-%d %H:%M"
    # strtime = time.strftime(format, time.gmtime(timestamp - 10800))
    return datetime.datetime.fromtimestamp(timestamp)


def date_from_timestamp(timestamp):
    """ date_from_timestamp: This function receives a timestamp and returns
    a datetime.date object

    Args:
        timestamp (int or float): A UNIX timestamp

    Returns:
        (datetime.date): The date of the passed timestamp
    """
    return datetime.datetime.fromtimestamp(timestamp).date()


def timestamp_from_datetime(date):
    """ timestamp_from_datetime: From a passed string, it will return a
    timestamp value

    Args:
        date (string): This parameter has the pattern:
            "%Y-%m-%dT%H:%M:%S"

    Returns:
        (int): is returned a int value that represents the passed datetime
        string in a UNIX timestamp
    """
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").timestamp()


def datetime_from_str(date):
    """ datetime_from_str: convert string to datetime object

    Args:
        date (string): The pattern of this parameter is:
        "%Y-%m-%dT%H:%M:%S"

    Returns:
        (datetime.datetime): It is a datetime object from the passed
        string
    """
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")


def time_from_datetimestr(date):
    """ time_from_datetimestr: It returns a datetime.time object from a passed
    string

    Args:
        date (string): This string has to respect the pattern:
            "%Y-%m-%dT%H:%M:%S"

    Returns:
        (datetime.time): A datetime.time object from a passed string
    """
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").time()


def date_from_str(date, separator='-'):
    """ date_from_str: It returns a datetime.date object from a passed string

    Args:
        date (string): This parameter must respect the pattern: "%Y-%m-%d"
        separator (string): This parameter must respect the separation standard
    Returns:
        (datetime.date): A datetime.date object from a passed string
    """
    return datetime.datetime.strptime(date, "%Y"+separator+"%m"+separator+"%d").date()


def time_from_str(time):
    """ time_from_str: It returns a datetime.time object from a passed string

    Args:
        time (string): This parameter must respect the pattern: "%H:%M"

    Returns:
        (datetime.time): A datetime.time object from a passed string
    """
    if len(time) == 5:
        return datetime.datetime.strptime(time, "%H:%M").time()
    elif len(time) == 8:
        return datetime.datetime.strptime(time, "%H:%M:%S").time()


def minute_from_str(time):
    """ time_from_str: It returns a int value from a passed string

    Args:
        time (string): This parameter must respect the pattern: "%H:%M"

    Returns:
        (int): A int value, representing the minute for the passed time
    """
    return minute_from_time(time_from_str(time))


def get_dy(timestamp):
    """ get_dy: Return a the day year from a passed timestamp

    Args:
        timestamp (int): A UNIX timestamp

    Returns:
        (int): A int value representing the day of the year
    """
    return datetime.datetime.fromtimestamp(timestamp).timetuple().tm_yday


def linspace_time(start, end, typ='time'):
    """ linspace_time: It returns a list of datetime.time from a passed
    start time and end time

    That means, if you call:

    linspace_time(datetime.time(10,0), datetime.time(10,30))

    The result will be:

    [datetime.time(10,0), datetime.time(10,1)... datetime.time(10,29),
    datetime.time(10,30)]

    Args:
        start (datetime.time): This is a start point, because of that, it
        should be minor then the end parameter
        end (datetime.time): Like the start, this parameter should be higher
        then start
        typ (str): This defines the type of return list:
        (datetime.time or str with% H:% M)
        Default is 'time'.
        Options ('str' or 'time')

    Returns:
        (list of datetime.time or str): This list is a time list from the start value
        to the end value
    """
    aux = start
    timeList = []
    while aux != end:
        timeList.append(aux)
        if aux.minute == 59:
            if aux.hour == 23:
                aux = datetime.time(0, 0, 0)
            else:
                aux = datetime.time(aux.hour + 1, 0, 0)
        else:
            aux = datetime.time(aux.hour, aux.minute + 1, 0)
    timeList.append(end)

    if typ == 'time':
        return timeList
    elif typ == 'str':
        return [str_from_time(i) for i in timeList]


def weekday(day):
    """ weekday: it returns a weekday representation

    Args:
        day (int or string): If int, it must be 0 <= day < 7. If string,
        must be a day in lib.util.timelib.weekdays
    Returns:
        (int): if the day parameter is a string.
        or
        (string): if the day parameter is a int
    """
    indx = isinstance(day, int) and day < 7 and day >= 0
    value = isinstance(day, str) and day in weekdays
    valueEN = isinstance(day, str) and day in weekdaysEN
    if indx:
        return weekdays[day]
    elif value:
        return weekdays.index(day)
    elif valueEN:
        return weekdaysEN.index(day)

    return None


def translate_weekday(day, lang='EN'):
    """
    translate_weekday: it returns the weekday name in another language (PT-EN, EN-PT)

    :param day: (str) it must be a weekday name, in portuguese or english
    :param lang: (str) must be 'EN' or 'PT', the function will return the weekday in that language
    :return: (str) is a weekday str in the passed language
    """
    if day in weekdays:
        if lang == 'EN':
            return weekdaysEN[weekdays.index(day)]
        return day
    elif day in weekdaysEN:
        if lang == 'PT':
            return weekdays[weekdaysEN.index(day)]
        return day


def linspace_date(start, end, freq='MS', typ='str', format="%Y/%m/%d"):
    """ linspace_date: It returns a list of datetime.date or str
    from a passed start time and end time with frequency

    That means, if you call:

    linspace_date(datetime.date(), datetime.date(11,30), 30)

    The result will be:

    [datetime.date(10,0), datetime.date(10,30), datetime.date(11,0),
    datetime.date(11,30)]

    Args:
        start (datetime.date or str): This is a start point, because of that, it
        should be minor then the end parameter
        end (datetime.date or str): Like the start, this parameter should be higher
        then start
        freq (str): Defines the frequency of values in the list.
        Default is MS(monthly)
        Link for others freq:
            https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases
        typ (str): This defines the type of return list:
        (datetime.date or str with %Y/%m/"d)
        Default is 'str'.
        Options ('str' or 'date')
        format (str): in case of selecting return in string it is possible to
        determine the format with the notation
        Default is '"%Y/%m/%d"'
    Returns:
        (list of datetime.date or str): This list is a date list from the start value
        to the end value
    """
    if typ == 'str':
        return date_range(start, end, freq=freq).strftime(format).tolist()
    elif typ == 'time':
        return date_range(start, end, freq=freq).tolist()


def str_from_time(time):
    """ str_from_time: It returns a str object from a passed datetime.time object

    Args:
        time (datetime.time)

    Returns:
        (str): A str object from a passed datetime.time
    """
    return datetime.datetime.strftime(time, "%H:%M")