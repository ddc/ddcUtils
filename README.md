# Few Utility Functions

[![License](https://img.shields.io/github/license/ddc/ddcUtils.svg?style=plastic)](https://github.com/ddc/ddcUtils/blob/master/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?style=plastic)](https://www.python.org)
[![PyPi](https://img.shields.io/pypi/v/ddcUtils.svg?style=plastic)](https://pypi.python.org/pypi/ddcUtils)
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A//actions-badge.atrox.dev/ddc/ddcUtils/badge?ref=main&style=plastic&label=build&logo=none)](https://actions-badge.atrox.dev/ddc/ddcUtils/goto?ref=main)


# Install
```shell
pip install ddcUtils
```

# Cryptography
```python
from ddcUtils import Cryptography
cp = Cryptography()
```

+ GENERATE_PRIVATE_KEY
    + Generates a private key to be used instead of default one
    + But keep in mind that this private key will be needed to decode further strings
        ```
        @staticmethod
        generate_private_key() -> str
        ```

+ ENCODE
    + Encodes a given string
        ```
        encode(str_to_encode: str) -> str
         ```     

+ DECODE
    + Decodes a given string
        ```
        decode(str_to_decode: str) -> str
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
    + Returns the name of the active branch if found, else returns the "master" branch
        ```
        @staticmethod
        get_active_branch_name(git_dir: str, master_branch_name: str = "master") -> str | None
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
    dir_logs = "./logs",
    level = "info",
    filename = "app.log",
    encoding = "UTF-8",
    days_to_keep = 7,
    when = "midnight",
    utc = True
)
log.setup_logging()
```


# Databases
+ DBSQLITE
```
class DBSqlite(db_file_path: str, batch_size=100, echo=False)
```

```python
import sqlalchemy as sa
from ddcUtils.databases import DBSqlite, DBUtils
dbsqlite = DBSqlite(database_file_path)
with dbsqlite.session() as session:
    stmt = sa.select(Table).where(Table.id == 1)
    db_utils = DBUtils(session)
    results = db_utils.fetchall(stmt)
```

+ DBPOSTGRES
  + Using driver "psycopg2"
```python
import sqlalchemy as sa
from ddcUtils.databases import DBPostgres, DBUtils
db_configs = {
    "username": username,
    "password": password,
    "host": host,
    "port": port,
    "database": database
}
dbpostgres = DBPostgres(**db_configs)
with dbpostgres.session() as session:
    stmt = sa.select(Table).where(Table.id == 1)
    db_utils = DBUtils(session)
    results = db_utils.fetchall(stmt)
```

+ DBPOSTGRES ASYNC
  + Using driver "psycopg2"
```python
import sqlalchemy as sa
from ddcUtils.databases import DBPostgresAsync, DBUtilsAsync
db_configs = {
    "username": username,
    "password": password,
    "host": host,
    "port": port,
    "database": database
}
dbpostgres = DBPostgresAsync(**db_configs)
async with dbpostgres.session() as session:
    stmt = sa.select(Table).where(Table.id == 1)
    db_utils = DBUtilsAsync(session)
    results = await db_utils.fetchall(stmt)
```

+ DBUTILS
  + Uses SQLAlchemy statements
```python
from ddcUtils.databases import DBUtils
db_utils = DBUtils(session)
db_utils.add(stmt)
db_utils.execute(stmt)
db_utils.fetchall(stmt)
db_utils.fetchone(stmt)
db_utils.fetch_value(stmt)
```

+ DBUTILS ASYNC
  + Uses SQLAlchemy statements
```python
from ddcUtils.databases import DBUtilsAsync
db_utils = DBUtilsAsync(session)
await db_utils.add(stmt)
await db_utils.execute(stmt)
await db_utils.fetchall(stmt)
await db_utils.fetchone(stmt)
await db_utils.fetch_value(stmt)
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
