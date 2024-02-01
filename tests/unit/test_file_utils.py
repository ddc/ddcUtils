# -*- encoding: utf-8 -*-
import os
from pathlib import Path
import pytest
from ddcUtils import constants, FileUtils


class TestFileUtils:
    @classmethod
    def setup_class(cls):
        cls.test_files_dir = os.path.join(constants.BASE_DIR, "tests", "data", "test_files")
        cls.test_file = os.path.join(cls.test_files_dir, "test_file.ini")
        cls.test_zip_file = os.path.join(cls.test_files_dir, "test_file.zip")
        cls.unknown_file = os.path.join(cls.test_files_dir, "unknown.ini")

    @classmethod
    def teardown_class(cls):
        """
        Leaving empty for further use
        """
        pass

    def test_open_file(self):
        # nonexistent file
        with pytest.raises(FileNotFoundError) as exc_info:
            FileUtils.open_file(self.unknown_file)
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
        file_name = os.path.basename(self.test_file)
        result_file_path = os.path.join(self.test_files_dir, f"{file_name}.gz")
        result = FileUtils.gzip_file(self.test_file)
        assert result == Path(result_file_path)
        os.remove(result_file_path)

    def test_unzip_file(self):
        # test unzip file and delete afterwards
        result = FileUtils.unzip_file(self.test_zip_file)
        assert result is not None
        test_file = os.path.join(self.test_files_dir, result.filelist[0].filename)
        files_list = FileUtils.list_files(self.test_files_dir)
        assert Path(test_file) in files_list
        os.remove(test_file)

    def test_get_file_values(self):
        # wrong file path
        with pytest.raises(FileNotFoundError) as exc_info:
            FileUtils().get_file_values(self.unknown_file)
        assert exc_info.value.args[0] == 2
        assert exc_info.value.args[1] == "No such file or directory"
        assert exc_info.typename == "FileNotFoundError"

        # returnign one single dict - mixed values
        mixed_values = True
        result = FileUtils().get_file_values(self.test_file, mixed_values)
        assert "main.files" in result.keys()
        assert "Database_Credentials.database" in result.keys()

        # return organized dict values
        mixed_values = False
        result = FileUtils().get_file_values(self.test_file, mixed_values)
        assert "main" in result.keys()
        assert "Database_Credentials" in result.keys()

    def test_get_file_section_values(self):
        # wrong file
        section_name = "main"
        with pytest.raises(FileNotFoundError) as exc_info:
            FileUtils().get_file_section_values(self.unknown_file, section_name)
        assert exc_info.value.args[0] == 2
        assert exc_info.value.args[1] == "No such file or directory"
        assert exc_info.typename == "FileNotFoundError"

        # get all section values
        section_name = "main"
        result = FileUtils().get_file_section_values(self.test_file, section_name)
        assert "files" in result.keys()
        assert "path_logs" in result.keys()

    def test_get_file_value(self):
        # existing config_name
        section_name = "Database Credentials"
        config_name = "port"
        result = FileUtils().get_file_value(self.test_file, section_name, config_name)
        assert result == 5432

        # nonexistent config_name
        section_name = "main"
        config_name = "filess"
        result = FileUtils().get_file_value(self.test_file, section_name, config_name)
        assert result is None

    def test_set_file_value(self):
        # setting value and retrieving to check
        section_name = "main"
        config_name = "path_logs"
        new_value = "/tmp/test_dir"
        result = FileUtils().set_file_value(self.test_file, section_name, config_name, new_value)
        assert result is True
        result = FileUtils().get_file_value(self.test_file, section_name, config_name)
        assert result == new_value

    def test_get_binary_type(self):
        result = FileUtils.get_exe_binary_type(self.test_file)
        assert result == "Not an EXE file"
