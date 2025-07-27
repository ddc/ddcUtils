# File Utilities
Few File Utilities and some OS Functions

[![Donate](https://img.shields.io/badge/Donate-PayPal-brightgreen.svg?style=plastic)](https://www.paypal.com/ncp/payment/6G9Z78QHUD4RJ)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPi](https://img.shields.io/pypi/v/ddcUtils.svg)](https://pypi.python.org/pypi/ddcUtils)
[![PyPI Downloads](https://static.pepy.tech/badge/ddcUtils)](https://pepy.tech/projects/ddcUtils)
[![codecov](https://codecov.io/gh/ddc/ddcUtils/graph/badge.svg?token=QsjwsmYzgD)](https://codecov.io/gh/ddc/ddcUtils)
[![CI/CD Pipeline](https://github.com/ddc/ddcUtils/actions/workflows/workflow.yml/badge.svg)](https://github.com/ddc/ddcUtils/actions/workflows/workflow.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ddc_ddcUtils&metric=alert_status)](https://sonarcloud.io/dashboard?id=ddc_ddcUtils)  
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A//actions-badge.atrox.dev/ddc/ddcUtils/badge?ref=main&label=build&logo=none)](https://actions-badge.atrox.dev/ddc/ddcUtils/goto?ref=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python](https://img.shields.io/pypi/pyversions/ddcUtils.svg)](https://www.python.org/downloads)

[![Support me on GitHub](https://img.shields.io/badge/Support_me_on_GitHub-154c79?style=for-the-badge&logo=github)](https://github.com/sponsors/ddc)


## Table of Contents
- [Install](#install)
- [Conf File Utils](#conf-file-utils)
- [File Utils](#file-utils)
- [Object](#object)
- [Misc Utils](#misc-utils)
- [OS Utils](#os-utils)
- [Development](#development)
- [License](#license)
- [Support](#support)


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


### GET_ALL_VALUES
Get all values from an .ini config file structure and return them as a dictionary.\
The `mixed_values` parameter will return all values as an object instead of dict.
```python
from ddcUtils import ConfFileUtils

cfu = ConfFileUtils()
# Get all values as dictionary
all_values = cfu.get_all_values("/path/to/config.ini", mixed_values=False)
print(all_values)  # {'main': {'files': '5', 'path': '/tmp/test_dir', 'port': '5432', 'list': '1,2,3,4,5,6'}}

# Get all values as object
all_values_obj = cfu.get_all_values("/path/to/config.ini", mixed_values=True)
print(all_values_obj.main.files)  # 5
```



### GET_SECTION_VALUES
Get all section values from an .ini config file structure and return them as a dictionary.
```python
from ddcUtils import ConfFileUtils

cfu = ConfFileUtils()
# Get all values from 'main' section
section_values = cfu.get_section_values("/path/to/config.ini", "main")
print(section_values)  # {'files': '5', 'path': '/tmp/test_dir', 'port': '5432', 'list': '1,2,3,4,5,6'}
```



### GET_VALUE
Get a specific value from an .ini config file structure and return it.
```python
from ddcUtils import ConfFileUtils

cfu = ConfFileUtils()
# Get specific value from config
port = cfu.get_value("/path/to/config.ini", "main", "port")
print(port)  # "5432"

path = cfu.get_value("/path/to/config.ini", "main", "path")
print(path)  # "/tmp/test_dir"
```



### SET_VALUE
Set a value in an .ini config file structure and return True for success or False for failure.
```python
from ddcUtils import ConfFileUtils

cfu = ConfFileUtils()
# Set a new value in config file
success = cfu.set_value("/path/to/config.ini", "main", "port", "8080")
print(success)  # True

# Set a list value with comma separation
success = cfu.set_value("/path/to/config.ini", "main", "servers", "server1,server2,server3", commas=True)
print(success)  # True
```


# File Utils

### OPEN
Open the given file or directory in the system's default application (explorer/file manager or text editor) and returns True for success or False for failed access.
```python
from ddcUtils import FileUtils

fu = FileUtils()
# Open file in default application
success = fu.open("/path/to/document.txt")
print(success)  # True

# Open directory in file explorer
success = fu.open("/path/to/directory")
print(success)  # True
```



### LIST_FILES
List all files in the given directory and return them in a tuple sorted by creation time in ascending order.\
Supports filtering by file prefix and suffix.
```python
from ddcUtils import FileUtils

fu = FileUtils()
# List all files in directory
all_files = fu.list_files("/home/user/documents")
print(all_files)  # ('file1.txt', 'file2.pdf', 'image.jpg')

# List files starting with 'test'
test_files = fu.list_files("/home/user/documents", starts_with="test")
print(test_files)  # ('test_data.csv', 'test_results.txt')

# List Python files
py_files = fu.list_files("/home/user/projects", ends_with=".py")
print(py_files)  # ('main.py', 'utils.py', 'config.py')
```



### GZIP
Compress the given file using gzip compression and returns the Path object for success or None if the operation failed.
```python
from ddcUtils import FileUtils

fu = FileUtils()
# Compress file to the same directory
compressed_path = fu.gzip("/path/to/large_file.txt")
print(compressed_path)  # /path/to/large_file.txt.gz

# Compress file to specific directory
compressed_path = fu.gzip("/path/to/large_file.txt", output_dir="/path/to/compressed")
print(compressed_path)  # /path/to/compressed/large_file.txt.gz
```



### UNZIP
Extracts the contents of a ZIP file to the specified output directory and returns ZipFile object for success or None if the operation failed.
```python
from ddcUtils import FileUtils

fu = FileUtils()
# Extract to the same directory as ZIP file
zip_file = fu.unzip("/path/to/archive.zip")
print(zip_file)  # <zipfile.ZipFile object>

# Extract to specific directory
zip_file = fu.unzip("/path/to/archive.zip", out_path="/path/to/extract")
print(zip_file)  # <zipfile.ZipFile object>
```



### REMOVE
Remove the given file or directory and return True if it was successfully removed, False otherwise.
```python
from ddcUtils import FileUtils

fu = FileUtils()
# Remove a file
success = fu.remove("/path/to/unwanted_file.txt")
print(success)  # True

# Remove a directory and all its contents
success = fu.remove("/path/to/unwanted_directory")
print(success)  # True
```



### RENAME
Rename the given file or directory and returns True if the operation was successful, False otherwise.
```python
from ddcUtils import FileUtils

fu = FileUtils()
# Rename a file
success = fu.rename("/path/to/old_name.txt", "/path/to/new_name.txt")
print(success)  # True

# Rename a directory
success = fu.rename("/path/to/old_folder", "/path/to/new_folder")
print(success)  # True
```



### COPY_DIR
Copy all files and subdirectories from source to destination directory and return True for success or False for failure.
```python
from ddcUtils import FileUtils

fu = FileUtils()
# Copy directory with all contents
success = fu.copy_dir("/path/to/source_dir", "/path/to/destination_dir")
print(success)  # True

# Copy directory including symbolic links
success = fu.copy_dir("/path/to/source_dir", "/path/to/destination_dir", symlinks=True)
print(success)  # True

# Copy directory ignoring certain patterns
import shutil
success = fu.copy_dir("/path/to/source_dir", "/path/to/destination_dir", 
                     ignore=shutil.ignore_patterns('*.tmp', '*.log'))
print(success)  # True
```



### DOWNLOAD_FILE
Download a file from a remote URL to a local file path and return True for success or False for failure.
```python
from ddcUtils import FileUtils

fu = FileUtils()
# Download file from URL
success = fu.download_file(
    "https://example.com/data/file.csv", 
    "/local/path/downloaded_file.csv"
)
print(success)  # True

# Download image
success = fu.download_file(
    "https://example.com/images/photo.jpg", 
    "/local/images/photo.jpg"
)
print(success)  # True
```



### GET_EXE_BINARY_TYPE
Analyzes a Windows executable file and returns its binary type (32-bit or 64-bit architecture).
```python
from ddcUtils import FileUtils

fu = FileUtils()
# Check Windows executable architecture
binary_type = fu.get_exe_binary_type("C:\\Program Files\\app.exe")
print(binary_type)  # "64-bit" or "32-bit"

# Check another executable
binary_type = fu.get_exe_binary_type("C:\\Windows\\System32\\notepad.exe")
print(binary_type)  # "64-bit"
```



### IS_OLDER_THAN_X_DAYS
Check if a file or directory is older than the specified number of days and returns True or False.
```python
from ddcUtils import FileUtils

fu = FileUtils()
# Check if the file is older than 30 days
is_old = fu.is_older_than_x_days("/path/to/log_file.txt", 30)
print(is_old)  # True or False

# Check if the directory is older than 7 days
is_old = fu.is_older_than_x_days("/path/to/temp_folder", 7)
print(is_old)  # True or False

# Useful for cleanup scripts
if fu.is_older_than_x_days("/path/to/backup.zip", 90):
    fu.remove("/path/to/backup.zip")
    print("Old backup removed")
```



### COPY
Copy a single file from source path to destination path.
```python
from ddcUtils import FileUtils

fu = FileUtils()
# Copy single file
success = fu.copy("/path/to/source_file.txt", "/path/to/destination_file.txt")
print(success)  # True

# Copy file to different directory
success = fu.copy("/home/user/document.pdf", "/backup/document.pdf")
print(success)  # True
```



# Object
This class is used for creating a simple dynamic object that allows you to add attributes on the fly.

```python
from ddcUtils import Object

# Create dynamic object
obj = Object()
obj.name = "John Doe"
obj.age = 30
obj.email = "john@example.com"

print(obj.name)  # "John Doe"
print(obj.age)   # 30

# Use as configuration object
config = Object()
config.database_url = "postgresql://localhost:5432/mydb"
config.debug_mode = True
config.max_connections = 100

print(config.database_url)  # "postgresql://localhost:5432/mydb"
```   


# Misc Utils

### CLEAR_SCREEN
Clears the terminal/console screen, works cross-platform (Windows, Linux, macOS).
```python
from ddcUtils import MiscUtils

mu = MiscUtils()
# Clear terminal screen (works on Windows, Linux, macOS)
mu.clear_screen()
print("Screen cleared!")

# Useful in interactive scripts
while True:
    user_input = input("Enter command (or 'clear' to clear screen): ")
    if user_input == 'clear':
        mu.clear_screen()
    elif user_input == 'quit':
        break
```



### USER_CHOICE
Presents options to the user and prompts them to select one, returning the user's choice.
```python
from ddcUtils import MiscUtils

mu = MiscUtils()
# Present menu options to user
options = ["Create new file", "Edit existing file", "Delete file", "Exit"]
choice = mu.user_choice(options)
print(f"You selected: {choice}")  # User's selection

# Simple yes/no choice
yes_no = mu.user_choice(["Yes", "No"])
if yes_no == "Yes":
    print("Proceeding...")
else:
    print("Cancelled.")
```



### GET_ACTIVE_BRANCH_NAME
Returns the name of the currently active Git branch if found, otherwise returns None.
```python
from ddcUtils import MiscUtils

mu = MiscUtils()
# Get current Git branch in current directory
branch = mu.get_active_branch_name()
print(branch)  # "main" or "develop" or None

# Get branch from a specific Git repository
branch = mu.get_active_branch_name(git_dir="/path/to/project/.git")
print(branch)  # "feature/new-feature" or None

# Use in deployment scripts
current_branch = mu.get_active_branch_name()
if current_branch == "main":
    print("Deploying to production...")
elif current_branch == "develop":
    print("Deploying to staging...")
else:
    print(f"Branch '{current_branch}' not configured for deployment")
```



### GET_CURRENT_DATE_TIME
Returns the current date and time as a datetime object in UTC timezone.
```python
from ddcUtils import MiscUtils
from datetime import datetime

mu = MiscUtils()
# Get current UTC datetime
current_time = mu.get_current_date_time()
print(current_time)  # 2024-01-15 14:30:25.123456+00:00
print(type(current_time))  # <class 'datetime.datetime'>

# Use for timestamps
timestamp = mu.get_current_date_time()
print(f"Operation completed at: {timestamp}")
```



### CONVERT_DATETIME_TO_STR_LONG
Converts a datetime object to a long string format.

Returns: `"Mon Jan 01 2024 21:43:04"`
```python
from ddcUtils import MiscUtils
from datetime import datetime

mu = MiscUtils()
# Convert datetime to long string format
dt = datetime(2024, 1, 15, 21, 43, 4)
long_str = mu.convert_datetime_to_str_long(dt)
print(long_str)  # "Mon Jan 15 2024 21:43:04"

# Use with current time
current_time = mu.get_current_date_time()
formatted = mu.convert_datetime_to_str_long(current_time)
print(f"Current time: {formatted}")
```



### CONVERT_DATETIME_TO_STR_SHORT
Converts a datetime object to a short string format.

Returns: `"2024-01-01 00:00:00.000000"`
```python
from ddcUtils import MiscUtils
from datetime import datetime

mu = MiscUtils()
# Convert datetime to short string format
dt = datetime(2024, 1, 15, 12, 30, 45, 123456)
short_str = mu.convert_datetime_to_str_short(dt)
print(short_str)  # "2024-01-15 12:30:45.123456"

# Use for logging
current_time = mu.get_current_date_time()
log_timestamp = mu.convert_datetime_to_str_short(current_time)
print(f"[{log_timestamp}] Application started")
```



### CONVERT_STR_TO_DATETIME_SHORT
Converts a string to a datetime object.

Input format: `"2024-01-01 00:00:00.000000"`
```python
from ddcUtils import MiscUtils

mu = MiscUtils()
# Convert string to datetime object
date_str = "2024-01-15 12:30:45.123456"
dt = mu.convert_str_to_datetime_short(date_str)
print(dt)  # 2024-01-15 12:30:45.123456
print(type(dt))  # <class 'datetime.datetime'>

# Parse timestamps from logs
log_entry = "2024-01-15 09:15:30.000000"
parsed_time = mu.convert_str_to_datetime_short(log_entry)
print(f"Log entry time: {parsed_time}")
```



### GET_CURRENT_DATE_TIME_STR_LONG
Returns the current date and time as a long formatted string.

Returns: `"Mon Jan 01 2024 21:47:00"`
```python
from ddcUtils import MiscUtils

mu = MiscUtils()
# Get current time as long formatted string
current_str = mu.get_current_date_time_str_long()
print(current_str)  # "Mon Jan 15 2024 21:47:00"

# Use for user-friendly timestamps
print(f"Report generated on: {mu.get_current_date_time_str_long()}")

# Use in file names
filename = f"backup_{mu.get_current_date_time_str_long().replace(' ', '_').replace(':', '-')}.zip"
print(filename)  # "backup_Mon_Jan_15_2024_21-47-00.zip"
```


# OS Utils

### GET_OS_NAME
Get the operating system name (Windows, Linux, Darwin/macOS, etc.).
```python
from ddcUtils import OsUtils

ou = OsUtils()
# Get operating system name
os_name = ou.get_os_name()
print(os_name)  # "Windows", "Linux", "Darwin" (macOS), etc.

# Use for platform-specific logic
if ou.get_os_name() == "Windows":
    print("Running on Windows")
    # Windows-specific code
elif ou.get_os_name() == "Linux":
    print("Running on Linux")
    # Linux-specific code
elif ou.get_os_name() == "Darwin":
    print("Running on macOS")
    # macOS-specific code
```



### IS_WINDOWS
Check if the current operating system is Windows and returns True or False.
```python
from ddcUtils import OsUtils

ou = OsUtils()
# Check if running on Windows
is_win = ou.is_windows()
print(is_win)  # True or False

# Use for Windows-specific operations
if ou.is_windows():
    print("Configuring Windows-specific settings...")
    # Use backslashes for paths, configure Windows services, etc.
else:
    print("Configuring Unix-like system settings...")
    # Use forward slashes, configure Unix services, etc.
```



### GET_CURRENT_PATH
Returns the current working directory as a string path.
```python
from ddcUtils import OsUtils

ou = OsUtils()
# Get the current working directory
current_dir = ou.get_current_path()
print(current_dir)  # "/home/user/projects/myapp" or "C:\\Users\\User\\Projects\\MyApp"

# Use for relative path operations
config_file = f"{ou.get_current_path()}/config.ini"
print(f"Config file location: {config_file}")

# Create paths relative to the current directory
log_dir = f"{ou.get_current_path()}/logs"
data_dir = f"{ou.get_current_path()}/data"
```



### GET_PICTURES_PATH
Returns the path to the Pictures directory inside the user's home directory.
```python
from ddcUtils import OsUtils

ou = OsUtils()
# Get user's Pictures directory
pictures_dir = ou.get_pictures_path()
print(pictures_dir)  # "/home/user/Pictures" or "C:\\Users\\User\\Pictures"

# Use for saving images
from ddcUtils import FileUtils
fu = FileUtils()

# Download image to Pictures folder
image_path = f"{ou.get_pictures_path()}/downloaded_image.jpg"
success = fu.download_file("https://example.com/image.jpg", image_path)
if success:
    print(f"Image saved to: {image_path}")
```



### GET_DOWNLOADS_PATH
Returns the path to the Downloads directory inside the user's home directory.
```python
from ddcUtils import OsUtils

ou = OsUtils()
# Get user's Downloads directory
downloads_dir = ou.get_downloads_path()
print(downloads_dir)  # "/home/user/Downloads" or "C:\\Users\\User\\Downloads"

# Use for file downloads
from ddcUtils import FileUtils
fu = FileUtils()

# Download file to Downloads folder
file_path = f"{ou.get_downloads_path()}/document.pdf"
success = fu.download_file("https://example.com/document.pdf", file_path)
if success:
    print(f"File downloaded to: {file_path}")

# Check for old downloads
if fu.is_older_than_x_days(downloads_dir, 30):
    print("Downloads folder has old files")
```


# Development

### Building from Source
```shell
poetry build -f wheel
```

### Running Tests
```shell
poetry update --with test
poe tests
```



# License
Released under the [MIT License](LICENSE)



# Support
If you find this project helpful, consider supporting development:

- [GitHub Sponsor](https://github.com/sponsors/ddc)
- [ko-fi](https://ko-fi.com/ddcsta)
- [PayPal](https://www.paypal.com/ncp/payment/6G9Z78QHUD4RJ)
