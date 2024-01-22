# -*- encoding: utf-8 -*-
import os
from pathlib import Path
from ddcUtils import constants


class OsUtils:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def get_current_path() -> Path:
        """
        Returns the current working directory
        :return: Path
        """

        path = os.path.abspath(os.getcwd())
        return Path(os.path.normpath(path)) if path else None

    @staticmethod
    def get_pictures_path() -> Path:
        """
        Returns the pictures directory inside the user's home directory
        :return: Path
        """

        if constants.OS_NAME == "Windows":
            import winreg
            sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
            pictures_guid = "My Pictures"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                pictures_path = winreg.QueryValueEx(key, pictures_guid)[0]
            return Path(pictures_path)
        else:
            pictures_path = os.path.join(os.getenv("HOME"), "Pictures")
            return Path(pictures_path)

    @staticmethod
    def get_downloads_path() -> Path:
        """
        Returns the download directory inside the user's home directory
        :return: Path
        """

        if constants.OS_NAME == "Windows":
            import winreg
            sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
            downloads_guid = "{374DE290-123F-4565-9164-39C4925E467B}"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                downloads_path = winreg.QueryValueEx(key, downloads_guid)[0]
            return Path(downloads_path)
        else:
            downloads_path = os.path.join(os.getenv("HOME"), "Downloads")
            return Path(downloads_path)
