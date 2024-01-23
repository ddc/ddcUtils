# Few Utility Functions

[![License](https://img.shields.io/github/license/ddc/ddcUtils.svg?style=plastic)](https://github.com/ddc/ddcUtils/blob/master/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=plastic)](https://www.python.org)
[![pypi](https://img.shields.io/pypi/v/ddcUtils.svg?style=plastic)](https://pypi.python.org/pypi/ddcUtils)
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fddc%2FddcUtils%2Fbadge%3Fref%3Dmain&style=plastic&label=build&logo=none)](https://actions-badge.atrox.dev/ddc/ddcUtils/goto?ref=main)


# Install
```shell
pip install ddcUtils
pip install git+https://github.com/ddc/ddcUtils
```


# File Utils
```python
from ddcUtils import FileUtils
fu = FileUtils()
```

+ OPEN_FILE
    + Opens the given file and returns 0 for success and 1 for failed access to the file
        ```python
        open_file(file_path: str) -> int
        ```

+ LIST_FILES
    + Lists all files in the given directory and returns them in a list
        ```python
        list_files(directory: str, file_extension: str = None) -> list
        ```

+ GZIP_FILE
    + Opens the given file and returns the path for success or None if failed
        ```python
        gzip_file(file_path: str) -> Path | None
        ```

+ UNZIP_FILE
    + Opens the given file and returns the zipfile for success or None for failed
        ```python
        unzip_file(file_path: str, out_path: str = None) -> zipfile.ZipFile | None
        ```

+ COPYDIR
    + Copy files from src to dst and returns True or False
        ```python
        copydir(src, dst, symlinks=False, ignore=None) -> bool
        ```

+ DOWNLOAD_FILE
    + Download file from remote url to local and returns True or False
        ```python
        download_file(remote_file_url, local_file_path) -> bool
        ```

+ GET_EXE_BINARY_TYPE
    + Returns the binary type of the given windows EXE file
        ```python
        get_exe_binary_type(file_path: str) -> str | None
        ```

### Functions for .ini/.conf config file structure
Example of file.ini:

    [main]
    files=5
    path="/tmp/test_dir"
    port=5432
    list=1,2,3,4,5,6


+ GET_ALL_FILE_VALUES
    + Get all values from an .ini config file structure and returns them as a dictionary
        ```python
        get_all_file_values(file_path: str, mixed_values: bool = False) -> dict
        ```

+ GET_ALL_FILE_SECTION_VALUES
    + Get all section values from an .ini config file structure and returns them as a dictionary
        ```python
        get_all_file_section_values(file_path: str, section: str) -> dict
        ```

+ GET_FILE_VALUE
    + Get value from an .ini config file structure and returns it
        ```python
        get_file_value(file_path: str, section: str, config_name: str) -> str | int | None:
        ```

+ SET_FILE_VALUE
    + Set value from an .ini config file structure and returns True or False
        ```python
        set_file_value(file_path: str, section_name: str, config_name: str, new_value) -> bool:
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
        ```python
        clear_screen() -> None
        ```

+ USER_CHOICE
    + This function will ask the user to select an option
        ```python
        user_choice() -> input
        ```

+ GET_ACTIVE_BRANCH_NAME
    + This function will return the name of the active branch
        ```python
        get_active_branch_name(default_master_branch_name: str = "master") -> str
        ```

+ GET_CURRENT_DATE_TIME
    + Returns the current date and time on UTC timezone
        ```python
        get_current_date_time() -> datetime
        ```

+ CONVERT_DATETIME_TO_STR_LONG
    + Converts a datetime object to a long string
    + returns: "Mon Jan 01 2024 21:43:04"
        ```python
        convert_datetime_to_str_long(date: datetime) -> str
        ```

+ CONVERT_DATETIME_TO_STR_SHORT
    + Converts a datetime object to a short string
    + returns: "2024-01-01 00:00:00.000000"
        ```python
        convert_datetime_to_str_short(date: datetime) -> str
        ```

+ CONVERT_STR_TO_DATETIME_SHORT
    + Converts a str to a datetime
    + input: "2024-01-01 00:00:00.000000"
        ```python
        convert_str_to_datetime_short(datetime_str: str) -> datetime
        ```

+ GET_CURRENT_DATE_TIME_STR_LONG
    + Returns the current date and time as string
    + returns: "Mon Jan 01 2024 21:47:00"
        ```python
        get_current_date_time_str_long() -> str
        ```


# OS Utils
```python
from ddcUtils import OsUtils
ou = OsUtils()
```

+ GET_CURRENT_PATH
    + Returns the current working directory
        ```python
        get_current_path() -> Path
        ```

+ GET_PICTURES_PATH
    + Returns the pictures directory inside the user's home directory
        ```python
        get_pictures_path() -> Path
        ```

+ GET_DOWNLOADS_PATH
    + Returns the download directory inside the user's home directory
        ```python
        get_downloads_path() -> Path
        ```


# Logs
+ SETUP_LOGGING
    + Logs will rotate based on `when` variable to a `.tar.gz` file, defaults to `midnight`
    + Logs will be deleted based on the `days_to_keep` variable, defaults to 7
    + Current 'when' events supported:
        + S - Seconds
        + M - Minutes
        + H - Hours
        + D - Days
        + midnight - roll over at midnight
        + W{0-6} - roll over on a certain day; 0 - Monday
```python
from ddcUtils import Log
log = Log(
    dir_logs: str = "logs",
    filename: str = "app",
    days_to_keep: int = 7,
    when: str = "midnight",
    utc: bool = True,
    level: str = "info"
)
log.setup_logging()
```


# Databases
+ DBSQLITE
```python
from ddcUtils.databases import DBSqlite
dbsqlite = DBSqlite(db_file_path: str, batch_size=100, echo=False)
```

+ DBPOSTGRES
```python
from ddcUtils.databases import DBPostgres
dbpostgres = DBPostgres(**kwargs)
username = kwargs["username"]
password = kwargs["password"]
host = kwargs["host"]
port = kwargs["port"]
db = kwargs["database"]
```

+ DBUTILS
  + Uses SQLAlchemy statements
```python
from ddcUtils import DBUtils
db_utils = DBUtils(session)
db_utils.add(stmt)
db_utils.execute(stmt)
db_utils.fetchall(stmt)
db_utils.fetchone(stmt)
db_utils.fetch_value(stmt)
```



# Source Code
### Build
```shell
poetry build
```

### Run Tests
```shell
poe test
```


### Get Coverage Report
```shell
poe coverage
```


# License
Released under the [MIT License](LICENSE)
