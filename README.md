# Few Utility Functions
Few personal utilities functions written in python3 and hosted on PyPI such as open and read conf/ini files and some OS functions.

[![License](https://img.shields.io/github/license/ddc/ddcUtils.svg?style=plastic)](https://github.com/ddc/ddcUtils/blob/master/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?style=plastic)](https://www.python.org)
[![PyPi](https://img.shields.io/pypi/v/ddcUtils.svg?style=plastic)](https://pypi.python.org/pypi/ddcUtils)
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A//actions-badge.atrox.dev/ddc/ddcUtils/badge?ref=main&style=plastic&label=build&logo=none)](https://actions-badge.atrox.dev/ddc/ddcUtils/goto?ref=main)


# Install
```shell
pip install ddcUtils
```


# Conf File Utils
```python
from ddcUtils import ConfFileUtils
cfu = ConfFileUtils()
```

File example - file.ini:

    [main]
    files=5
    path="/tmp/test_dir"
    port=5432
    list=1,2,3,4,5,6


+ GET_ALL_VALUES
    + Get all values from an .ini config file structure and returns them as a dictionary
    + mixed_values will return all values as an object instead of dict
        ```
        get_all_values(file_path: str, mixed_values: bool = False) -> dict
        ```

+ GET_SECTION_VALUES
    + Get all section values from an .ini config file structure and returns them as a dictionary
        ```
        get_section_values(file_path: str, section: str) -> dict
        ```

+ GET_VALUE
    + Get value from an .ini config file structure and returns it
        ```
        get_value(file_path: str, section: str, config_name: str) -> str | int | None
        ```

+ SET_VALUE
    + Set value from an .ini config file structure and returns True or False
        ```
        set_value(file_path: str, section_name: str, config_name: str, new_value, commas: bool = False) -> bool
        ```


# File Utils
```python
from ddcUtils import FileUtils
fu = FileUtils()
```

+ SHOW
    + Open the given file or directory in explorer or notepad and returns True for success or False for failed access
        ```
        @staticmethod
        show(path: str) -> bool
        ```

+ LIST_FILES
    + List all files in the given directory and returns them in a tuple sorted by creation time in ascending order
        ```
        @staticmethod
        list_files(directory: str, starts_with: str | tuple[str, ...] | list[str] = None, ends_with: str | tuple[str, ...] | list[str] = None) -> tuple
        ```

+ GZIP
    + Compress the given file and returns the Path for success or None if failed
        ```
        @staticmethod
        gzip(input_file_path: str, output_dir: str = None) -> Path | None
        ```

+ UNZIP
    + Unzips the given file.zip and returns ZipFile for success or None if failed
        ```
        @staticmethod
        unzip(file_path: str, out_path: str = None) -> ZipFile | None
        ```

+ REMOVE
    + Remove the given file or dir and returns True if it was successfully removed
        ```
        @staticmethod
        remove(path: str) -> bool
        ```

+ RENAME
    + Rename the given file and returns True if the file was successfully
        ```
        @staticmethod
        rename(from_name: str, to_name: str) -> bool
        ```

+ COPY_DIR
    + Copy files from src to dst and returns True or False
        ```
        @staticmethod
        copy_dir(src, dst, symlinks=False, ignore=None) -> bool
        ```

+ DOWNLOAD_FILE
    + Download file from remote url to local and returns True or False
        ```
        @staticmethod
        download_file(remote_file_url, local_file_path) -> bool
        ```

+ GET_EXE_BINARY_TYPE
    + Returns the binary type of the given windows EXE file
        ```
        @staticmethod
        get_exe_binary_type(file_path: str) -> str | None
        ```

+ IS_OLDER_THAN_X_DAYS
    + Check if a file or directory is older than the specified number of days
        ```
        @staticmethod
        is_older_than_x_days(path: str, days: int) -> bool
        ```

+ COPY
    + Copy a file to another location
        ```
        @staticmethod
        copy(src_path, dst_path)
        ```


# Object
+ This class is used for creating a simple class object
 ```python
from ddcUtils import Object
obj = Object()
obj.test = "test"
```   


# Misc Utils
```python
from ddcUtils import MiscUtils
mu = MiscUtils()
```

+ CLEAR_SCREEN
    + Clears the terminal screen
        ```
        @staticmethod
        clear_screen() -> None
        ```

+ USER_CHOICE
    + This function will ask the user to select an option
        ```
        @staticmethod
        user_choice() -> input
        ```

+ GET_ACTIVE_BRANCH_NAME
    + Returns the name of the active branch if found, else returns None
        ```
        @staticmethod
        get_active_branch_name(git_dir: str = ".git") -> str | None:
        ```

+ GET_CURRENT_DATE_TIME
    + Returns the current date and time on UTC timezone
        ```
        @staticmethod
        get_current_date_time() -> datetime
        ```

+ CONVERT_DATETIME_TO_STR_LONG
    + Converts a datetime object to a long string
    + returns: "Mon Jan 01 2024 21:43:04"
        ```
        @staticmethod
        convert_datetime_to_str_long(date: datetime) -> str
        ```

+ CONVERT_DATETIME_TO_STR_SHORT
    + Converts a datetime object to a short string
    + returns: "2024-01-01 00:00:00.000000"
        ```
        @staticmethod
        convert_datetime_to_str_short(date: datetime) -> str
        ```

+ CONVERT_STR_TO_DATETIME_SHORT
    + Converts a str to a datetime
    + input: "2024-01-01 00:00:00.000000"
        ```
        @staticmethod
        convert_str_to_datetime_short(datetime_str: str) -> datetime
        ```

+ GET_CURRENT_DATE_TIME_STR_LONG
    + Returns the current date and time as string
    + returns: "Mon Jan 01 2024 21:47:00"
        ```
        get_current_date_time_str_long() -> str
        ```


# OS Utils
```python
from ddcUtils import OsUtils
ou = OsUtils()
```

+ GET_OS_NAME
    + Get OS name
        ```
        @staticmethod
        get_os_name() -> str
        ```

+ IS_WINDOWS
    + Check if OS is Windows
        ```
        @staticmethod
        is_windows() -> bool
        ```

+ GET_CURRENT_PATH
    + Returns the current working directory
        ```
        @staticmethod
        get_current_path() -> Path
        ```

+ GET_PICTURES_PATH
    + Returns the pictures directory inside the user's home directory
        ```
        get_pictures_path() -> Path
        ```

+ GET_DOWNLOADS_PATH
    + Returns the download directory inside the user's home directory
        ```
        get_downloads_path() -> Path
        ```


# Source Code
### Build
```shell
poetry build
```


### Run Tests
```shell
poetry run coverage run -m pytest -v
```


### Get Coverage Report
```shell
poetry run coverage report
```


# License
Released under the [MIT License](LICENSE)
