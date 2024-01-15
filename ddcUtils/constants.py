# -*- encoding: utf-8 -*-
from pathlib import Path
import platform
import sys


__version_info__ = ("1", "0", "0")
__version__ = ".".join(__version_info__)
__author__ = "ddc"
__email__ = "ddc@ddc"
__req_python_version__ = (3, 10, 0)


VERSION = __version__
PYTHON_OK = sys.version_info >= __req_python_version__
MIN_PYTHON_VERSION = ".".join(str(x) for x in __req_python_version__)
OS_NAME = platform.system()
DATE_TIME_FORMATTER_STR = "%a %b %m %Y %X"
DATE_FORMATTER = "%Y-%m-%d"
TIME_FORMATTER = "%H:%M:%S.%f"
BASE_DIR = Path(__file__).resolve().parent.parent
DAYS_TO_KEEP_LOGS = 7
