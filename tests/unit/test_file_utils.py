# -*- encoding: utf-8 -*-
import os
from pathlib import Path
import pytest
from ddcUtils import constants, file_utils


class TestFileUtils:
    @classmethod
    def setup_class(cls):
        cls.test_files_dir = os.path.join(constants.BASE_DIR, "tests", "data", "test_files")
        cls.test_file = os.path.join(cls.test_files_dir, "test_file.ini")
        cls.test_zip_file = os.path.join(cls.test_files_dir, "test_file.zip")
        cls.unknown_file = os.path.join(cls.test_files_dir, "unknown.ini")

    @classmethod
    def teardown_class(cls):
        pass

    def test_open_file(self):
        # nonexistent file
        with pytest.raises(FileNotFoundError) as exc_info:
            file_utils.open_file(self.unknown_file)
        assert exc_info.value.args[0] == 2
        assert exc_info.value.args[1] == "No such file or directory"
        assert exc_info.typename == "FileNotFoundError"

    def test_list_files(self):
        # list all files
        result = file_utils.list_files(self.test_files_dir)
        assert Path(self.test_file) in result

        # list all files by exntension
        result = file_utils.list_files(self.test_files_dir, ".zip")
        assert Path(self.test_zip_file) in result

    def test_gzip_file(self):
        # test gzip file and delete afterwards
        file_name = os.path.basename(self.test_file)
        result_file_path = os.path.join(self.test_files_dir, f"{file_name}.gz")
        result = file_utils.gzip_file(self.test_file)
        assert result == Path(result_file_path)
        os.remove(result_file_path)

    def test_unzip_file(self):
        # test unzip file and delete afterwards
        result = file_utils.unzip_file(self.test_zip_file)
        assert result is not None
        test_file = os.path.join(self.test_files_dir, result.filelist[0].filename)
        files_list = file_utils.list_files(self.test_files_dir)
        assert Path(test_file) in files_list
        os.remove(test_file)

    def test_get_all_file_values(self):
        # wrong file path
        with pytest.raises(FileNotFoundError) as exc_info:
            file_utils.get_all_file_values(self.unknown_file)
        assert exc_info.value.args[0] == 2
        assert exc_info.value.args[1] == "No such file or directory"
        assert exc_info.typename == "FileNotFoundError"

        # returnign one single dict - mixed values
        mixed_values = True
        result = file_utils.get_all_file_values(self.test_file, mixed_values)
        assert "files" in result
        assert "database" in result

        # return organized dict values
        mixed_values = False
        result = file_utils.get_all_file_values(self.test_file, mixed_values)
        assert "main" in result
        assert "database_credentials" in result

    def test_get_all_file_section_values(self):
        # wrong file
        section_name = "main"
        with pytest.raises(FileNotFoundError) as exc_info:
            file_utils.get_all_file_section_values(self.unknown_file, section_name)
        assert exc_info.value.args[0] == 2
        assert exc_info.value.args[1] == "No such file or directory"
        assert exc_info.typename == "FileNotFoundError"

        # get all section values
        section_name = "main"
        result = file_utils.get_all_file_section_values(self.test_file, section_name)
        assert "files" in result
        assert "path_logs" in result

    def test_get_file_section_value(self):
        # existing config_name
        section_name = "Database Credentials"
        config_name = "port"
        result = file_utils.get_file_value(self.test_file, section_name, config_name)
        assert result == 5432

        # nonexistent config_name
        section_name = "main"
        config_name = "filess"
        result = file_utils.get_file_value(self.test_file, section_name, config_name)
        assert result is None

    def test_set_file_value(self):
        # setting value and retrieving to check
        section_name = "main"
        config_name = "path_logs"
        new_value = "/tmp/test_dir"
        result = file_utils.set_file_value(self.test_file, section_name, config_name, new_value)
        assert result is True
        result = file_utils.get_file_value(self.test_file, section_name, config_name)
        assert result == new_value

    def test_get_binary_type(self):
        result = file_utils.get_exe_binary_type(self.test_file)
        assert result == "Not an EXE file"
