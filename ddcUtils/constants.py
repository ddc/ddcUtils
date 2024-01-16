# -*- encoding: utf-8 -*-
from pathlib import Path
import platform


OS_NAME = platform.system()
BASE_DIR = Path(__file__).resolve().parent.parent
DATE_TIME_FORMATTER_STR = "%a %b %m %Y %X"
DATE_FORMATTER = "%Y-%m-%d"
TIME_FORMATTER = "%H:%M:%S.%f"
