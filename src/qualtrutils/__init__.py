try:
    import os
    import pkg_resources  # part of setuptools
    __version__ = pkg_resources.get_distribution(os.path.dirname(__file__)).version
except:
    pass

from .qualtrics import *