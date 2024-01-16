import logging
import sys
from logging import NullHandler
from .misc_utils import Object, MiscUtils
from .file_utils import FileUtils
from .os_utils import OsUtils
from .exceptions import get_exception


__version_info__ = ("1", "0", "4")
__version__ = ".".join(__version_info__)
__author__ = "Daniel Costa"
__email__ = "danieldcsta@gmail.com>"
__req_python_version__ = (3, 11, 0)
VERSION = __version__
REQ_PYTHON_VERSION = sys.version_info >= __req_python_version__

_formatt = "[%(asctime)s.%(msecs)03d]:[%(levelname)s]:%(message)s"
formatter = logging.Formatter(_formatt, datefmt="%Y-%m-%dT%H:%M:%S")
stream_hdlr = logging.StreamHandler()
stream_hdlr.setFormatter(formatter)
stream_hdlr.setLevel("INFO")
logging.getLogger(__name__).addHandler(stream_hdlr)
