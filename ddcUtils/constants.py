# -*- encoding: utf-8 -*-
from pathlib import Path
import platform
import sys
from . import (
    __version__,
    __req_python_version__,
)


VERSION = __version__
PYTHON_OK = sys.version_info >= __req_python_version__
MIN_PYTHON_VERSION = ".".join(str(x) for x in __req_python_version__)
OS_NAME = platform.system()
DATE_TIME_FORMATTER_STR = "%a %b %m %Y %X"
DATE_FORMATTER = "%Y-%m-%d"
TIME_FORMATTER = "%H:%M:%S.%f"
BASE_DIR = Path(__file__).resolve().parent.parent
