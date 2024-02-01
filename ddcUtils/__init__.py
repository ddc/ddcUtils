import logging
import os
from .crypto import Cryptography
from .exceptions import get_exception
from .file_utils import FileUtils
from .log import Log
from .misc_utils import Object, MiscUtils
from .os_utils import OsUtils
from importlib.metadata import version
from pathlib import Path
from typing import Literal, NamedTuple


__title__ = "ddcUtils"
__author__ = "Daniel Costa"
__email__ = "danieldcsta@gmail.com>"
__license__ = "MIT"
__copyright__ = "Copyright 2023-present ddc"
_req_python_version = (3, 11, 0)


try:
    _version = tuple(int(x) for x in version(__title__).split("."))
except ModuleNotFoundError:
    # this will be called on local tests, since theres no package installed
    import toml
    pyproject = toml.load(os.path.join(Path(__file__).parent.parent, "pyproject.toml"))
    _version = pyproject["tool"]["poetry"]["version"]
    del pyproject


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


__version__ = _version
__version_info__: VersionInfo = VersionInfo(
    major=__version__[0],
    minor=__version__[1],
    micro=__version__[2],
    releaselevel="final",
    serial=0
)
__req_python_version__: VersionInfo = VersionInfo(
    major=_req_python_version[0],
    minor=_req_python_version[1],
    micro=_req_python_version[2],
    releaselevel="final",
    serial=0
)

logging.getLogger(__name__).addHandler(logging.NullHandler())

del logging, NamedTuple, Literal, VersionInfo, version, _version, _req_python_version
