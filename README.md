# Few Utility Functions

[<img src="https://img.shields.io/github/license/ddc/ddcUtils.svg?style=plastic">](https://github.com/ddc/ddcUtils/blob/master/LICENSE)
[<img src="https://img.shields.io/badge/Python-3.11+-blue.svg?style=plastic">](https://www.python.org)
[<img src="https://img.shields.io/pypi/v/ddcUtils.svg?style=plastic">](https://pypi.python.org/pypi/ddcUtils)
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fddc%2FddcUtils%2Fbadge%3Fref%3Dmain&style=plastic&label=build&logo=none)](https://actions-badge.atrox.dev/ddc/ddcUtils/goto?ref=main)


# Install
    pip install ddcUtils
    pip install -U git+https://github.com/ddc/ddcUtils


# File Utils
    from ddcUtils import FileUtils
+ open_file
+ list_files
+ gzip_file
+ unzip_file
+ copydir
+ download_file
+ get_exe_binary_type
+ get_all_file_values
+ get_all_file_section_values
+ get_file_value
+ set_file_value


# Misc Utils
    from ddcUtils import MiscUtils
+ Object()
+ clear_screen
+ user_choice
+ get_active_branch_name
+ get_current_date_time
+ get_current_date_time_str_long
+ convert_datetime_to_str_long
+ convert_datetime_to_str_short
+ convert_str_to_datetime_short


# OS Utils
    from ddcUtils import OsUtils
+ get_current_path
+ get_pictures_path
+ get_downloads_path


# Databases
      from ddcUtils.database import DBPostgres, DBSqlite, DBUtils
+ DBSqlite
+ DBPostgres
+ DBUtils
    + add
    + execute
    + fetchall
    + fetchone
    + fetch_value


# Logs
    from ddcUtils import Log
+ setup_logging


# Source Code
#### Build
+ poetry build


#### Run Tests
+ poe test


#### Get Coverage Report
+ poe coverage


# License
Released under the [MIT License](LICENSE)
