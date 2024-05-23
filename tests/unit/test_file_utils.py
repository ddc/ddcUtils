# -*- encoding: utf-8 -*-
import os
import tempfile
from pathlib import Path
import pytest
from ddcUtils import constants, FileUtils


class TestFileUtils:
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

    def test_show_file(self):
        # nonexistent file
        with pytest.raises(FileNotFoundError) as exc_info:
            FileUtils.show(self.unknown_file)
        assert exc_info.value.args[0] == 2
        assert exc_info.value.args[1] == "No such file or directory"
        assert exc_info.typename == "FileNotFoundError"

    def test_list_files(self):
        # list all files
        result = FileUtils.list_files(self.test_files_dir)
        assert Path(self.test_file) in result

        # list all files with "test"
        result = FileUtils.list_files(directory=self.test_files_dir, starts_with="test")
        assert Path(self.test_zip_file) in result

        # list all files by exntension
        result = FileUtils.list_files(directory=self.test_files_dir, ends_with=".zip")
        assert Path(self.test_zip_file) in result

    def test_gzip_file(self):
        # test gzip file and delete afterwards
        result_file = FileUtils.gzip(self.test_file, self.temp_test_dir)
        assert os.path.isfile(result_file)
        FileUtils.remove(str(result_file))

    def test_unzip_file(self):
        # test unzip file and delete afterwards
        result = FileUtils.unzip(self.test_zip_file, self.temp_test_dir)
        assert result is not None
        test_file = os.path.join(self.temp_test_dir, result.filelist[0].filename)
        files_list = FileUtils.list_files(self.temp_test_dir)
        assert Path(test_file) in files_list
        FileUtils.remove(test_file)

    def test_copy_and_remove(self):
        # test copy - delete afterwards
        dst_file = os.path.join(self.test_files_dir, "test_copy.ini")
        result = FileUtils.copy(self.test_file, dst_file)
        assert result is True
        result = FileUtils.remove(dst_file)
        assert result is True

    def test_remove(self):
        # test remove of nonexistent file
        with pytest.raises(FileNotFoundError) as exc_info:
            FileUtils.remove(self.unknown_file)
        assert exc_info.value.args[0] == 2
        assert exc_info.value.args[1] == "No such file or directory"
        assert exc_info.typename == "FileNotFoundError"

    def test_rename(self):
        # test copy and rename file - delete afterwards
        dst_file = os.path.join(self.test_files_dir, "test_copy.ini")
        result = FileUtils.copy(self.test_file, dst_file)
        assert result is True
        renamed_filename = os.path.join(self.test_files_dir, "test_renamed.ini")
        result = FileUtils.rename(dst_file, renamed_filename)
        assert result is True
        result = FileUtils.remove(renamed_filename)
        assert result is True

    def test_copy_dir(self):
        # test copy directory - delete afterward
        dst_dir = os.path.join(self.test_files_dir, "test_dir")
        result = FileUtils.copy_dir(self.test_files_dir, dst_dir)
        assert result is True
        result = FileUtils.remove(dst_dir)
        assert result is True

    def test_download_file(self):
        # test downlaod file - delete afterward
        remote_url = "https://raw.githubusercontent.com/ddc/ddcUtils/main/README.md"
        dst_file = os.path.join(self.test_files_dir, "README.md")
        result = FileUtils.download_file(remote_url, dst_file)
        assert result is True
        result = FileUtils.remove(dst_file)
        assert result is True

    def test_get_binary_type(self):
        # test file binary type
        result = FileUtils.get_exe_binary_type(self.test_file)
        assert result == "Not an EXE file"

    def test_is_older_than_x_days(self):
        # test if file is older than the specified number of days
        test_file = os.path.join(constants.BASE_DIR, ".gitignore")

        days = 1
        result = FileUtils.is_older_than_x_days(test_file, days)
        assert result is True

        days = 2
        result = FileUtils.is_older_than_x_days(test_file, days)
        assert result is True

        days = 99999
        result = FileUtils.is_older_than_x_days(test_file, days)
        assert result is False

        # nonexistent file
        with pytest.raises(FileNotFoundError) as exc_info:
            FileUtils.is_older_than_x_days(self.unknown_file, days)
        assert exc_info.value.args[0] == 2
        assert exc_info.value.args[1] == "No such file or directory"
        assert exc_info.typename == "FileNotFoundError"
