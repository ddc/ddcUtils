from importlib.metadata import version
import logging
from typing import NamedTuple, Literal
from logging import NullHandler
from .misc_utils import Object, MiscUtils
from .file_utils import FileUtils
from .os_utils import OsUtils
from .databases.db_utils import DBUtils
from .exceptions import get_exception
from .log import Log


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


__title__ = "ddcUtils"
__author__ = "Daniel Costa"
__email__ = "danieldcsta@gmail.com>"
__license__ = "MIT"
__copyright__ = "Copyright 2023-present ddc"
__req_python_version__ = (3, 11, 0)


try:
    __version__ = tuple(int(x) for x in version(__title__).split("."))
    _release_level = "final"
except ModuleNotFoundError:
    __version__ = (0, 0, 0)
    _release_level = "test"

__version_info__: VersionInfo = VersionInfo(
    major=__version__[0],
    minor=__version__[1],
    micro=__version__[2],
    releaselevel=_release_level,
    serial=0
)

logging.getLogger(__name__).addHandler(logging.NullHandler())

del logging, NamedTuple, Literal, VersionInfo, version
