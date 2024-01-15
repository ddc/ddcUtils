# -*- encoding: utf-8 -*-
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from ddcUtils import constants


class Object:
    def __init__(self):
        self._created = datetime.now().isoformat()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_dict(self):
        json_string = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_dict = json.loads(json_string)
        return json_dict


def clear_screen() -> None:
    if constants.OS_NAME == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def user_choice() -> input:
    try:
        return input(">>> ").lower().strip()
    except SyntaxError:
        pass


def get_active_branch_name(default_master_branch_name: str = "master") -> str:
    head_dir = Path(os.path.join(constants.BASE_DIR, ".git", "HEAD"))
    try:
        with head_dir.open("r") as f:
            content = f.read().splitlines()
        for line in content:
            if line[0:4] == "ref:":
                return line.partition("refs/heads/")[2]
    except FileNotFoundError:
        return default_master_branch_name


def get_current_date_time() -> datetime:
    return datetime.now(timezone.utc)


def get_current_date_time_str_long() -> str:
    return convert_datetime_to_str_long(get_current_date_time())


def convert_datetime_to_str_long(date: datetime) -> str:
    return date.strftime(constants.DATE_TIME_FORMATTER_STR)


def convert_datetime_to_str_short(date: datetime) -> str:
    return date.strftime(f"{constants.DATE_FORMATTER} {constants.TIME_FORMATTER}")


def convert_str_to_datetime_short(date_str: str) -> datetime:
    return datetime.strptime(date_str, f"{constants.DATE_FORMATTER} {constants.TIME_FORMATTER}")
