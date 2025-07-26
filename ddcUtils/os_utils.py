import os
import sys
from pathlib import Path


class OsUtils:

    @staticmethod
    def get_os_name() -> str:
        """
        Get OS name
        :return:
        """

        return sys.platform

    @staticmethod
    def is_windows() -> bool:
        """
        Check if OS is Windows
        :return:
        """

        return sys.platform.startswith("win") or (sys.platform == "cli" and os.name == "nt")

    @staticmethod
    def get_current_path() -> Path | None:
        """
        Returns the current working directory
        :return: Path
        """

        return Path.cwd().resolve()

    def get_pictures_path(self) -> Path:
        """
        Returns the pictures directory inside the user's home directory
        :return: Path
        """

        if self.is_windows():
            import winreg

            sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
            pictures_guid = "My Pictures"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                pictures_path = winreg.QueryValueEx(key, pictures_guid)[0]
            return Path(pictures_path)
        else:
            pictures_path = os.path.join(os.getenv("HOME"), "Pictures")
            return Path(pictures_path)

    def get_downloads_path(self) -> Path:
        """
        Returns the download directory inside the user's home directory
        :return: Path
        """

        if self.is_windows():
            import winreg

            sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
            downloads_guid = "{374DE290-123F-4565-9164-39C4925E467B}"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                downloads_path = winreg.QueryValueEx(key, downloads_guid)[0]
            return Path(downloads_path)
        else:
            downloads_path = os.path.join(os.getenv("HOME"), "Downloads")
            return Path(downloads_path)
