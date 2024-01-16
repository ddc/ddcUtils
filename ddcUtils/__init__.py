import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

__version_info__ = ("1", "0", "0")
__version__ = ".".join(__version_info__)
__author__ = "ddc"
__email__ = "ddc@users.noreply.github.com"
__req_python_version__ = (3, 11, 0)
