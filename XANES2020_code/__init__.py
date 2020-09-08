try:
    from . import paths
except ImportError:
    print('You have not specified the path to the data.')
    print('Create a paths.py file by copying paths-template.py and editing it.')
    raise

import os

_ROOT = os.path.abspath(os.path.dirname(__file__))
PKG_DATA = os.path.join(_ROOT,'pkg_data')
def get_data(path):
    return os.path.join(PKG_DATA, path)
