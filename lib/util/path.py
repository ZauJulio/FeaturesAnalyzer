from os import name, path, makedirs
from .timelib import weekdaysEN
import psutil

bar = '/' if name == 'posix' else '\\'

_path = bar.join(['', '..', '..', '..', 'data', ''])


def fileIsOpen(fpath):
    for proc in psutil.process_iter():
        try:
            for item in proc.open_files():
                if fpath == item.path:
                    return True
        except Exception:
            pass

    return False


def check_create_dir(dir):
    """  """
    for day in weekdaysEN:
        if not path.isdir(dir+day):
            makedirs(dir+day)


tables = path.abspath(__file__ + '..' + '..' + _path + 'tables') + bar
""" A path to the tables directory
"""
tables_days = tables + bar
""" A path to the days directory
"""
tables_classified = tables + 'classified' + bar
""" A path to the classified directory
"""
tables_synthetic = tables + 'synthetic' + bar
""" A path to the synthetic directory
"""
tables_devices = tables + 'devices' + bar
""" A path to the devices directory
"""

dump = path.abspath(__file__ + _path + 'dump') + bar
""" A path to the dump directory
"""
index_path = path.abspath(__file__ + _path + 'models') + bar
""" A path to the models_rgs directory
"""
models_rgs = path.abspath(__file__ + _path + 'models') + bar + 'rgs' + bar
""" A path to the models_rgs directory
"""
models_som = path.abspath(__file__ + _path + 'models') + bar + 'som' + bar
""" A path to the models_som directory
"""
models_mlp = path.abspath(__file__ + _path + 'models') + bar + 'mlp' + bar
""" A path to the models_mlp_rgs directory """

clusters_som = path.abspath(__file__ + _path + 'clusters') + bar + 'som' + bar
""" A path to the clusters_som directory """

check_create_dir(clusters_som)
check_create_dir(models_rgs)
check_create_dir(models_som)
check_create_dir(models_mlp)

if not path.isdir(tables_days): makedirs(tables_days)
