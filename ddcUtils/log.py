# -*- encoding: utf-8 -*-
import gzip
import logging.handlers
import os
import sys


class Log:
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
        dir_logs: str = "logs",
        level: str = "info",
        filename: str = "app",
        days_to_keep: int = 7,
        when: str = "midnight",
        utc: bool = True,
    ):
        self.dir = dir_logs
        self.filename = filename
        self.days_to_keep = days_to_keep
        self.when = when
        self.utc = utc
        self.level = _get_level(level)

    def setup_logging(self):
        try:
            os.makedirs(self.dir, exist_ok=True) if not os.path.isdir(self.dir) else None
        except Exception as e:
            sys.stderr.write(f"[ERROR]:[Unable to create logs directory]:{str(e)}: {self.dir}\n")
            sys.exit(1)

        log_file_path = os.path.join(self.dir, f"{self.filename}.log")

        try:
            open(log_file_path, "a+").close()
        except IOError as e:
            sys.stderr.write(f"[ERROR]:[Unable to open log file for writing]:{str(e)}: {log_file_path}\n")
            sys.exit(1)

        _debug_formatt = ""
        if self.level == logging.DEBUG:
            _debug_formatt = "[%(filename)s:%(funcName)s:%(lineno)d]:"

        formatt = f"[%(asctime)s.%(msecs)03d]:[%(levelname)s]:{_debug_formatt}%(message)s"
        formatter = logging.Formatter(formatt, datefmt="%Y-%m-%dT%H:%M:%S")

        logger = logging.getLogger()
        logger.setLevel(self.level)

        file_hdlr = logging.handlers.TimedRotatingFileHandler(filename=log_file_path,
                                                              encoding="UTF-8",
                                                              when=self.when,
                                                              utc=self.utc,
                                                              backupCount=self.days_to_keep)

        file_hdlr.setFormatter(formatter)
        file_hdlr.suffix = "%Y%m%d"
        file_hdlr.rotator = GZipRotator(self.dir, self.days_to_keep)
        file_hdlr.setLevel(self.level)
        logger.addHandler(file_hdlr)

        stream_hdlr = logging.StreamHandler()
        stream_hdlr.setFormatter(formatter)
        stream_hdlr.setLevel(self.level)
        logger.addHandler(stream_hdlr)

        return logger


class GZipRotator:
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
                sys.stderr.write(f"[ERROR]:[Unable to zip log file]:{str(e)}: {source}\n")


class RemoveOldLogs:
    def __init__(self, logs_dir, days_to_keep):
        files_list = [f for f in os.listdir(logs_dir)
                      if os.path.isfile(f"{logs_dir}/{f}") and os.path.splitext(f)[1] == ".gz"]
        for file in files_list:
            file_path = f"{logs_dir}/{file}"
            if self._is_file_older_than_x_days(file_path, days_to_keep):
                try:
                    os.remove(file_path)
                except Exception as e:
                    sys.stderr.write(f"[ERROR]:[Unable to remove old logs]:{str(e)}: {file_path}\n")

    @staticmethod
    def _is_file_older_than_x_days(file_path, days_to_keep):
        from datetime import datetime, timedelta
        file_time = datetime.fromtimestamp(os.path.getctime(file_path))
        if int(days_to_keep) == 1:
            cutoff_time = datetime.today()
        else:
            cutoff_time = datetime.today() - timedelta(days=int(days_to_keep))
        file_time = file_time.replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_time = cutoff_time.replace(hour=0, minute=0, second=0, microsecond=0)
        if file_time < cutoff_time:
            return True
        return False


def _get_level(level: str):
    if not isinstance(level, str):
        sys.stdout.write("[ERROR]:[Unable to get log level]. Default level to: 'info'\n")
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
