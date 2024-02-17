# -*- encoding: utf-8 -*-
import datetime
import os
import tempfile
from ddcUtils import FileUtils, TimedRotatingLog


class TestLog:
    @classmethod
    def setup_class(cls):
        cls.level = "debug"
        cls.directory = os.path.join(tempfile.gettempdir())
        cls.filename = "TestFileUtils.log"
        cls.file_path = os.path.join(cls.directory, cls.filename)

    @classmethod
    def teardown_class(cls):
        FileUtils.remove(str(os.path.join(cls.directory, cls.filename)))

    def test_midnight_timed_rotating_log(self):
        log = TimedRotatingLog(directory=self.directory, level=self.level, filename=self.filename).init()
        log.debug("start")

        epoch_times = datetime.datetime(2020, 1, 1, 1, 1, 1).timestamp()
        os.utime(self.file_path, (epoch_times, epoch_times))

        log.debug("end")

        assert os.path.exists(self.file_path)
