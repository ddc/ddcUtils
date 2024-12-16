# File Utilities
Few File Utilities and some OS Functions

[![Donate](https://img.shields.io/badge/Donate-PayPal-brightgreen.svg?style=plastic)](https://www.paypal.com/ncp/payment/6G9Z78QHUD4RJ)
[![License](https://img.shields.io/github/license/ddc/ddcUtils.svg)](https://github.com/ddc/ddcUtils/blob/master/LICENSE)
[![PyPi](https://img.shields.io/pypi/v/ddcUtils.svg)](https://pypi.python.org/pypi/ddcUtils)
[![PyPI Downloads](https://static.pepy.tech/badge/ddcUtils)](https://pepy.tech/projects/ddcUtils)
[![codecov](https://codecov.io/gh/ddc/ddcUtils/graph/badge.svg?token=1ULU74GF57)](https://codecov.io/gh/ddc/ddcUtils)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A//actions-badge.atrox.dev/ddc/ddcUtils/badge?ref=main&label=build&logo=none)](https://actions-badge.atrox.dev/ddc/ddcUtils/goto?ref=main)
[![Python](https://img.shields.io/pypi/pyversions/ddcUtils.svg)](https://www.python.org)


# Install
```shell
pip install ddcUtils
```


# Conf File Utils

File example - file.ini:

    [main]
    files=5
    path="/tmp/test_dir"
    port=5432
    list=1,2,3,4,5,6


+ GET_ALL_VALUES
  + Get all values from an .ini config file structure and returns them as a dictionary
  + mixed_values will return all values as an object instead of dict
```python
from ddcUtils import ConfFileUtils
cfu = ConfFileUtils()
cfu.get_all_values(file_path, mixed_values=False)
```



+ GET_SECTION_VALUES
  + Get all section values from an .ini config file structure and returns them as a dictionary
```python
from ddcUtils import ConfFileUtils
cfu = ConfFileUtils()
cfu.get_section_values(file_path, section)
```



+ GET_VALUE
  + Get value from an .ini config file structure and returns it
```python
from ddcUtils import ConfFileUtils
cfu = ConfFileUtils()
cfu.get_value(file_path, section, config_name)
```



+ SET_VALUE
  + Set value from an .ini config file structure and returns True or False
```python
from ddcUtils import ConfFileUtils
cfu = ConfFileUtils()
cfu.set_value(file_path, section_name, config_name, new_value, commas=False)
```


# File Utils

+ OPEN
  + Open the given file or directory in explorer or notepad and returns True for success or False for failed access
```python
from ddcUtils import FileUtils
fu = FileUtils()
fu.open(path)
```



+ LIST_FILES
  + List all files in the given directory and returns them in a tuple sorted by creation time in ascending order
```python
from ddcUtils import FileUtils
fu = FileUtils()
fu.list_files(directory, starts_with, ends_with)
```



+ GZIP
  + Compress the given file and returns the Path for success or None if failed
```python
from ddcUtils import FileUtils
fu = FileUtils()
fu.gzip(input_file_path, output_dir=None)
```



+ UNZIP
  + Unzips the given file.zip and returns ZipFile for success or None if failed
```python
from ddcUtils import FileUtils
fu = FileUtils()
fu.unzip(file_path, out_pathNone)
```



+ REMOVE
  + Remove the given file or dir and returns True if it was successfully removed
```python
from ddcUtils import FileUtils
fu = FileUtils()
fu.remove(path)
```



+ RENAME
  + Rename the given file and returns True if the file was successfully
```python
from ddcUtils import FileUtils
fu = FileUtils()
fu.rename(from_name, to_name)
```



+ COPY_DIR
  + Copy files from src to dst and returns True or False
```python
from ddcUtils import FileUtils
fu = FileUtils()
fu.copy_dir(src, dst, symlinks=False, ignore=None)
```



+ DOWNLOAD_FILE
  + Download file from remote url to local and returns True or False
```python
from ddcUtils import FileUtils
fu = FileUtils()
fu.download_file(remote_file_url, local_file_path)
```



+ GET_EXE_BINARY_TYPE
  + Returns the binary type of the given windows EXE file
```python
from ddcUtils import FileUtils
fu = FileUtils()
fu.get_exe_binary_type(file_path)
```



+ IS_OLDER_THAN_X_DAYS
  + Check if a file or directory is older than the specified number of days
```python
from ddcUtils import FileUtils
fu = FileUtils()
fu.is_older_than_x_days(path, days)
```



+ COPY
  + Copy a file to another location
```python
from ddcUtils import FileUtils
fu = FileUtils()
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

+ CLEAR_SCREEN
  + Clears the terminal screen
```python
from ddcUtils import MiscUtils
mu = MiscUtils()
mu.clear_screen()
```



+ USER_CHOICE
  + This function will ask the user to select an option
```python
from ddcUtils import MiscUtils
mu = MiscUtils()
mu.user_choice()
```



+ GET_ACTIVE_BRANCH_NAME
  + Returns the name of the active branch if found, else returns None
```python
from ddcUtils import MiscUtils
mu = MiscUtils()
mu.get_active_branch_name(git_dir=".git")
```



+ GET_CURRENT_DATE_TIME
  + Returns the current date and time on UTC timezone
```python
from ddcUtils import MiscUtils
mu = MiscUtils()
mu.get_current_date_time()
```



+ CONVERT_DATETIME_TO_STR_LONG
  + Converts a datetime object to a long string
  + returns: "Mon Jan 01 2024 21:43:04"
```python
from ddcUtils import MiscUtils
mu = MiscUtils()
mu.convert_datetime_to_str_long(date)
```



+ CONVERT_DATETIME_TO_STR_SHORT
  + Converts a datetime object to a short string
  + returns: "2024-01-01 00:00:00.000000"
```python
from ddcUtils import MiscUtils
mu = MiscUtils()
mu.convert_datetime_to_str_short(date)
```



+ CONVERT_STR_TO_DATETIME_SHORT
  + Converts a str to a datetime
  + input: "2024-01-01 00:00:00.000000"
```python
from ddcUtils import MiscUtils
mu = MiscUtils()
mu.convert_str_to_datetime_short(datetime_str)
```



+ GET_CURRENT_DATE_TIME_STR_LONG
  + Returns the current date and time as string
  + returns: "Mon Jan 01 2024 21:47:00"
```python
from ddcUtils import MiscUtils
mu = MiscUtils()
mu.get_current_date_time_str_long()
```


# OS Utils

+ GET_OS_NAME
  + Get OS name
```python
from ddcUtils import OsUtils
ou = OsUtils()
get_os_name()
```



+ IS_WINDOWS
  + Check if OS is Windows
```python
from ddcUtils import OsUtils
ou = OsUtils()
is_windows()
```



+ GET_CURRENT_PATH
  + Returns the current working directory
```python
from ddcUtils import OsUtils
ou = OsUtils()
get_current_path()
```



+ GET_PICTURES_PATH
  + Returns the pictures directory inside the user's home directory
```python
from ddcUtils import OsUtils
ou = OsUtils()
get_pictures_path()
```



+ GET_DOWNLOADS_PATH
  + Returns the download directory inside the user's home directory
```python
from ddcUtils import OsUtils
ou = OsUtils()
get_downloads_path()
```


# Source Code
### Build
```shell
poetry build -f wheel
```



# Run Tests and Get Coverage Report using Poe
```shell
poetry update --with test
poe tests
```



# License
Released under the [MIT License](LICENSE)



# Buy me a cup of coffee
+ [GitHub Sponsor](https://github.com/sponsors/ddc)
+ [ko-fi](https://ko-fi.com/ddcsta)
+ [Paypal](https://www.paypal.com/ncp/payment/6G9Z78QHUD4RJ)
