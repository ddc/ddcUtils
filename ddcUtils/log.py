# -*- encoding: utf-8 -*-
import gzip
import logging.handlers
import os
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from .exceptions import get_exception
from .file_utils import FileUtils


class TimedRotatingLog:
    """
    TimedRotatingLog class

    Current 'when' events supported:
    S - Seconds
    M - Minutes
    H - Hours
    D - Days
    midnight - roll over at midnight
    W{0-6} - roll over on a certain day; 0 - Monday
    """

    def __init__(
        self,
        level: str = "info",
        directory: str = "logs",
        filename: str = "app.log",
        encoding: str = "UTF-8",
        days_to_keep: int = 7,
        when: str = "midnight",
        utc: bool = True,
    ):
        self.level = _get_level(level)
        self.directory = directory
        self.filename = filename
        self.encoding = encoding
        self.days_to_keep = days_to_keep
        self.when = when
        self.utc = utc

    def init(self):
        log_file_path = _get_log_path(self.directory, self.filename)
        file_hdlr = TimedRotatingFileHandler(filename=log_file_path,
                                             encoding=self.encoding,
                                             when=self.when,
                                             utc=self.utc,
                                             backupCount=self.days_to_keep)
        file_hdlr.suffix = "%Y%m%d"
        file_hdlr.rotator = GZipRotatorTimed(self.directory, self.days_to_keep)
        return _set_log_format(file_hdlr, self.level)


class SizeRotatingLog:
    """
    SizeRotatingLog class
    """

    def __init__(
        self,
        level: str = "info",
        directory: str = "logs",
        filename: str = "app.log",
        encoding: str = "UTF-8",
        days_to_keep: int = 7,
        max_mbytes: int = 5
    ):
        self.level = _get_level(level)
        self.directory = directory
        self.filename = filename
        self.encoding = encoding
        self.days_to_keep = days_to_keep
        self.max_mbytes = max_mbytes

    def init(self):
        log_file_path = _get_log_path(self.directory, self.filename)
        file_hdlr = RotatingFileHandler(filename=log_file_path,
                                        mode="a",
                                        maxBytes=self.max_mbytes * 1024 * 1024,
                                        backupCount=self.days_to_keep,
                                        encoding=self.encoding,
                                        delay=False,
                                        errors=None)
        file_hdlr.rotator = GZipRotatorSize(self.directory, self.days_to_keep)
        return _set_log_format(file_hdlr, self.level)


class GZipRotatorSize:
    def __init__(self, dir_logs: str, days_to_keep: int):
        self.dir = dir_logs
        self.days_to_keep = days_to_keep

    def __call__(self, source: str, dest: str) -> None:
        RemoveOldLogs(self.dir, self.days_to_keep)
        if os.path.isfile(source) and os.stat(source).st_size > 0:
            new_file_number = 1
            old_gz_files_list = FileUtils.list_files(self.dir, ends_with=".gz")
            if old_gz_files_list:
                try:
                    oldest_file_name = old_gz_files_list[-1].name.split(".")[0].split("_")
                    if len(oldest_file_name) > 1:
                        new_file_number = int(oldest_file_name.split("_")[1]) + 1
                except ValueError as e:
                    _write_stderr(f"[Unable to get old zip log file number]:{get_exception(e)}: {old_gz_files_list[-1].name}")
            _gzip_file(source, new_file_number)


class GZipRotatorTimed:
    def __init__(self, dir_logs: str, days_to_keep: int):
        self.dir = dir_logs
        self.days_to_keep = days_to_keep

    def __call__(self, source: str, dest: str) -> None:
        RemoveOldLogs(self.dir, self.days_to_keep)
        output_dated_name = os.path.splitext(dest)[1].replace(".", "")
        _gzip_file(source, output_dated_name)


class RemoveOldLogs:
    def __init__(self, logs_dir: str, days_to_keep: int) -> None:
        files_list = FileUtils.list_files(logs_dir, ends_with=".gz")
        for file in files_list:
            file_path = str(os.path.join(logs_dir, file))
            if FileUtils.is_older_than_x_days(file_path, days_to_keep):
                try:
                    FileUtils.remove(file_path)
                except Exception as e:
                    _write_stderr(f"[Unable to remove old logs]:{get_exception(e)}: {file_path}")


def _write_stderr(msg: str) -> None:
    sys.stdout.write(f"[ERROR]:{msg}\n")


def _get_level(level: str) -> logging:
    if not isinstance(level, str):
        _write_stderr("[Unable to get log level]. Default level to: 'info'")
        return logging.INFO
    match level.lower():
        case "debug":
            return logging.DEBUG
        case "warning":
            return logging.WARNING
        case "error":
            return logging.ERROR
        case "critical":
            return logging.CRITICAL
        case _:
            return logging.INFO


def _get_log_path(directory: str, filename: str) -> str:
    try:
        os.makedirs(directory, exist_ok=True) if not os.path.isdir(directory) else None
    except Exception as e:
        _write_stderr(f"[Unable to create logs directory]:{get_exception(e)}: {directory}")
        raise e

    log_file_path = str(os.path.join(directory, filename))

    try:
        open(log_file_path, "a+").close()
    except IOError as e:
        _write_stderr(f"[Unable to open log file for writing]:{get_exception(e)}: {log_file_path}")
        raise e

    return log_file_path


def _set_log_format(file_hdlr, level: logging) -> logging.Logger:
    _debug_formatt = ""
    if level == logging.DEBUG:
        _debug_formatt = f"[PID:{os.getpid()}]:[%(filename)s:%(funcName)s:%(lineno)d]:"

    formatt = f"[%(asctime)s.%(msecs)03d]:[%(levelname)s]:{_debug_formatt}%(message)s"
    formatter = logging.Formatter(formatt, datefmt="%Y-%m-%dT%H:%M:%S")

    logger = logging.getLogger()
    logger.setLevel(level)

    file_hdlr.setFormatter(formatter)
    file_hdlr.setLevel(level)
    logger.addHandler(file_hdlr)

    stream_hdlr = logging.StreamHandler()
    stream_hdlr.setFormatter(formatter)
    stream_hdlr.setLevel(level)
    logger.addHandler(stream_hdlr)

    return logger


def _gzip_file(source, output_partial_name):
    if os.path.isfile(source) and os.stat(source).st_size > 0:
        try:
            sfname, sext = os.path.splitext(source)
            renamed_dst = f"{sfname}_{output_partial_name}{sext}.gz"
            with open(source, "rb") as fin:
                with gzip.open(renamed_dst, "wb") as fout:
                    fout.writelines(fin)
            FileUtils.remove(source)
        except Exception as e:
            _write_stderr(f"[Unable to zip log file]:{get_exception(e)}: {source}")
