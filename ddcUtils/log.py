# -*- encoding: utf-8 -*-
import gzip
import logging.handlers
import os
import sys
from .exceptions import get_exception
from .file_utils import FileUtils
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


class TimedRotatingLog:
    """
    Logging class

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
        directory: str = "./logs",
        level: str = "info",
        filename: str = "app.log",
        encoding: str = "UTF-8",
        days_to_keep: int = 7,
        when: str = "midnight",
        utc: bool = True,
    ):
        self.directory = directory
        self.filename = filename
        self.encoding = encoding
        self.days_to_keep = days_to_keep
        self.when = when
        self.utc = utc
        self.level = _get_level(level)

    def init(self):
        log_file_path = _get_log_path(self.directory, self.filename)
        file_hdlr = TimedRotatingFileHandler(filename=log_file_path,
                                             encoding=self.encoding,
                                             when=self.when,
                                             utc=self.utc,
                                             backupCount=self.days_to_keep)
        return _set_log_format(file_hdlr, self.level, self.directory, self.days_to_keep)


class SizeRotatingLog:
    """
    Logging class
    """

    def __init__(
        self,
        directory: str = "./logs",
        filename: str = "app.log",
        encoding: str = "UTF-8",
        days_to_keep: int = 7,
        level: str = "info",
        max_mbytes: int = 5
    ):
        self.directory = directory
        self.filename = filename
        self.encoding = encoding
        self.days_to_keep = days_to_keep
        self.max_mbytes = max_mbytes
        self.level = _get_level(level)

    def init(self):
        log_file_path = _get_log_path(self.directory, self.filename)
        file_hdlr = RotatingFileHandler(filename=log_file_path,
                                        mode="a",
                                        maxBytes=self.max_mbytes * 1024 * 1024,
                                        backupCount=self.days_to_keep,
                                        encoding=self.encoding,
                                        delay=False,
                                        errors=None)
        return _set_log_format(file_hdlr, self.level, self.directory, self.days_to_keep)


class GZipTimeRotator:
    def __init__(self, dir_logs, days_to_keep):
        self.dir = dir_logs
        self.days_to_keep = days_to_keep

    def __call__(self, source, dest):
        RemoveOldLogs(self.dir, self.days_to_keep)
        if os.path.isfile(source) and os.stat(source).st_size > 0:
            try:
                sfname, sext = os.path.splitext(source)
                _, dext = os.path.splitext(dest)
                renamed_dst = f"{sfname}_{dext.replace('.', '')}{sext}.gz"
                with open(source, "rb") as fin:
                    with gzip.open(renamed_dst, "wb") as fout:
                        fout.writelines(fin)
                os.remove(source)
            except Exception as e:
                _write_stderr(f"[Unable to zip log file]:{get_exception(e)}: {source}")


class GZipSizeRotator:
    def __init__(self, dir_logs, days_to_keep):
        self.dir = dir_logs
        self.days_to_keep = days_to_keep

    def __call__(self, source, dest):
        RemoveOldLogs(self.dir, self.days_to_keep)
        if os.path.isfile(source) and os.stat(source).st_size > 0:
            try:
                sfname, sext = os.path.splitext(source)
                _, dext = os.path.splitext(dest)
                renamed_dst = f"{sfname}_{dext.replace('.', '')}{sext}.gz"
                with open(source, "rb") as fin:
                    with gzip.open(renamed_dst, "wb") as fout:
                        fout.writelines(fin)
                os.remove(source)
            except Exception as e:
                _write_stderr(f"[Unable to zip log file]:{get_exception(e)}: {source}")


class RemoveOldLogs:
    def __init__(self, logs_dir, days_to_keep):
        files_list = [f for f in os.listdir(logs_dir)
                      if os.path.isfile(f"{logs_dir}/{f}") and os.path.splitext(f)[1] == ".gz"]
        for file in files_list:
            file_path = os.path.join(logs_dir, file)
            if FileUtils.is_file_older_than_x_days(file_path, days_to_keep):
                try:
                    os.remove(file_path)
                except Exception as e:
                    _write_stderr(f"[Unable to remove old logs]:{get_exception(e)}: {file_path}")


def _write_stderr(msg):
    sys.stdout.write(f"[ERROR]:{msg}\n")


def _get_level(level: str):
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


def _get_log_path(directory, filename):
    try:
        os.makedirs(directory, exist_ok=True) if not os.path.isdir(directory) else None
    except Exception as e:
        _write_stderr(f"[Unable to create logs directory]:{get_exception(e)}: {directory}")
        raise e

    log_file_path = os.path.join(directory, filename)

    try:
        open(log_file_path, "a+").close()
    except IOError as e:
        _write_stderr(f"[Unable to open log file for writing]:{get_exception(e)}: {log_file_path}")
        raise e

    return str(log_file_path)


def _set_log_format(file_hdlr, level, directory, days_to_keep):
    _debug_formatt = ""
    if level == logging.DEBUG:
        _debug_formatt = f"[PID:{os.getpid()}]:[%(filename)s:%(funcName)s:%(lineno)d]:"

    formatt = f"[%(asctime)s.%(msecs)03d]:[%(levelname)s]:{_debug_formatt}%(message)s"
    formatter = logging.Formatter(formatt, datefmt="%Y-%m-%dT%H:%M:%S")

    logger = logging.getLogger()
    logger.setLevel(level)

    file_hdlr.setFormatter(formatter)
    if isinstance(file_hdlr, logging.handlers.TimedRotatingFileHandler):
        file_hdlr.suffix = "%Y%m%d"
        file_hdlr.rotator = GZipTimeRotator(directory, days_to_keep)
    else:
        file_hdlr.rotator = GZipSizeRotator(directory, days_to_keep)

    file_hdlr.setLevel(level)
    logger.addHandler(file_hdlr)

    stream_hdlr = logging.StreamHandler()
    stream_hdlr.setFormatter(formatter)
    stream_hdlr.setLevel(level)
    logger.addHandler(stream_hdlr)

    return logger
