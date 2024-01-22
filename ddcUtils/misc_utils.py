# -*- encoding: utf-8 -*-
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from ddcUtils import constants


class Object:
    """
    This class is used for creating a simple class object
    """
    def __init__(self):
        self._created = datetime.now().isoformat()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_dict(self):
        return json.loads(self.to_json())


class MiscUtils:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def clear_screen() -> None:
        """
        Clears the terminal screen
        :return:
        """

        if constants.OS_NAME == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    @staticmethod
    def user_choice() -> input:
        """
        This function will ask the user to select an option
        :return: input
        """

        try:
            return input(">>> ").lower().strip()
        except SyntaxError:
            pass

    @staticmethod
    def get_active_branch_name(default_master_branch_name: str = "master") -> str:
        """
        Returns the name of the active branch
        :param default_master_branch_name:
        :return: str
        """

        head_dir = Path(os.path.join(constants.BASE_DIR, ".git", "HEAD"))
        try:
            with head_dir.open("r") as f:
                content = f.read().splitlines()
            for line in content:
                if line[0:4] == "ref:":
                    return line.partition("refs/heads/")[2]
        except FileNotFoundError:
            return default_master_branch_name

    @staticmethod
    def get_current_date_time() -> datetime:
        """
        Returns the current date and time on UTC timezone
        :return: UTC datetime
        """

        return datetime.now(timezone.utc)

    @staticmethod
    def convert_datetime_to_str_long(date: datetime) -> str:
        """
        Converts a datetime object to a long string
        :param date:
        :return: str
        """

        return date.strftime(constants.DATE_TIME_FORMATTER_STR)

    @staticmethod
    def convert_datetime_to_str_short(date: datetime) -> str:
        """
        Converts a datetime object to a short string
        :param date:
        :return: str
        """

        return date.strftime(f"{constants.DATE_FORMATTER} {constants.TIME_FORMATTER}")

    @staticmethod
    def convert_str_to_datetime_short(datetime_str: str) -> datetime:
        """
        Converts a str to a datetime
        :param datetime_str:
        :return: datetime
        """

        return datetime.strptime(datetime_str, f"{constants.DATE_FORMATTER} {constants.TIME_FORMATTER}")

    def get_current_date_time_str_long(self) -> str:
        """
        Returns the current date and time as string
        :return: str
        """

        return self.convert_datetime_to_str_long(self.get_current_date_time())
