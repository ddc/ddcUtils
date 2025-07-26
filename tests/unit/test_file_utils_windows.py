import os
import tempfile
from pathlib import Path
import pytest
from ddcUtils import constants, FileUtils


@pytest.mark.skipif(os.name != 'nt', reason="Windows-specific tests")
class TestFileUtilsWindows:
    @classmethod
    def setup_class(cls):
        cls.test_files_dir = os.path.join(constants.BASE_DIR, "tests", "data", "files")
        cls.test_file = os.path.join(cls.test_files_dir, "test_file.ini")
        cls.test_zip_file = os.path.join(cls.test_files_dir, "test_file.zip")
        cls.unknown_file = os.path.join(cls.test_files_dir, "unknown.ini")
        cls.temp_test_dir = tempfile.gettempdir()

    @classmethod
    def teardown_class(cls):
        """
        Leaving empty for further use
        """
        pass

    def test_unzip_file_windows(self):
        # test unzip file on Windows with better cleanup
        import tempfile
        import shutil

        # Create a unique temp directory for this test
        temp_dir = tempfile.mkdtemp(prefix="test_unzip_")
        try:
            result = FileUtils.unzip(self.test_zip_file, temp_dir)
            assert result is not None
            test_file = os.path.join(temp_dir, result.filelist[0].filename)
            files_list = FileUtils.list_files(temp_dir)
            assert Path(test_file) in files_list
        finally:
            # Clean up the entire temp directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)

    def test_is_older_than_x_days_windows(self):
        # Create a temporary file and test on Windows
        import tempfile
        import shutil
        from datetime import datetime, timedelta

        # Create a unique temp directory for this test
        temp_dir = tempfile.mkdtemp(prefix="test_age_")
        temp_file = os.path.join(temp_dir, "test_old_file.txt")

        try:
            with open(temp_file, 'w') as f:
                f.write("test content")

            # Set file time to 2 days ago using Windows-compatible method
            two_days_ago = datetime.now() - timedelta(days=2)
            old_timestamp = two_days_ago.timestamp()

            # Use Windows-compatible time setting
            import time

            os.utime(temp_file, (old_timestamp, old_timestamp))

            # Give Windows a moment to update file times
            time.sleep(0.1)

            # Test file is older than 1 day
            result = FileUtils.is_older_than_x_days(temp_file, 1)
            assert result is True

            # Test file is not older than 365 days (1 year)
            result = FileUtils.is_older_than_x_days(temp_file, 365)
            assert result is False

        finally:
            # Clean up the entire temp directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)

        # nonexistent file
        with pytest.raises(FileNotFoundError) as exc_info:
            FileUtils.is_older_than_x_days(self.unknown_file, 1)
        assert exc_info.value.args[0] == 2
        assert exc_info.value.args[1] == "No such file or directory"
        assert exc_info.typename == "FileNotFoundError"

    def test_open_windows(self):
        # Test open on Windows with mock
        import unittest.mock

        with unittest.mock.patch('ddcUtils.file_utils.OsUtils.get_os_name', return_value='Windows'):
            with unittest.mock.patch.object(os, 'startfile', create=True) as mock_startfile:
                result = FileUtils.open(self.test_file)
                assert result is True
                mock_startfile.assert_called_once_with(self.test_file)
