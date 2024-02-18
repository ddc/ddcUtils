# -*- encoding: utf-8 -*-
import os
import pytest
from ddcUtils import constants, ConfFileUtils


class TestConfFileUtils:
    @classmethod
    def setup_class(cls):
        cls.test_files_dir = os.path.join(constants.BASE_DIR, "tests", "data", "files")
        cls.test_file = os.path.join(cls.test_files_dir, "test_file.ini")
        cls.unknown_file = os.path.join(cls.test_files_dir, "unknown.ini")

    @classmethod
    def teardown_class(cls):
        """
        Leaving empty for further use
        """
        pass

    def test_get_all_values(self):
        # wrong file path
        with pytest.raises(FileNotFoundError) as exc_info:
            ConfFileUtils().get_all_values(self.unknown_file)
        assert exc_info.value.args[0] == 2
        assert exc_info.value.args[1] == "No such file or directory"
        assert exc_info.typename == "FileNotFoundError"

        # returnign one single dict - mixed values
        mixed_values = True
        result = ConfFileUtils().get_all_values(self.test_file, mixed_values)
        assert "main.files" in result.keys()
        assert "Database_Credentials.database" in result.keys()

        # return organized dict values
        mixed_values = False
        result = ConfFileUtils().get_all_values(self.test_file, mixed_values)
        assert "main" in result.keys()
        assert "Database_Credentials" in result.keys()

    def test_get_section_values(self):
        # wrong file
        section_name = "main"
        with pytest.raises(FileNotFoundError) as exc_info:
            ConfFileUtils().get_section_values(self.unknown_file, section_name)
        assert exc_info.value.args[0] == 2
        assert exc_info.value.args[1] == "No such file or directory"
        assert exc_info.typename == "FileNotFoundError"

        # get all section values
        section_name = "main"
        result = ConfFileUtils().get_section_values(self.test_file, section_name)
        assert "files" in result.keys()
        assert "path_logs" in result.keys()

    def test_get_value(self):
        # existing config_name
        section_name = "Database Credentials"
        config_name = "port"
        result = ConfFileUtils().get_value(self.test_file, section_name, config_name)
        assert result == 5432

        # nonexistent config_name
        section_name = "main"
        config_name = "filess"
        result = ConfFileUtils().get_value(self.test_file, section_name, config_name)
        assert result is None

    def test_set_value(self):
        # setting value and retrieving to check
        section_name = "main"
        config_name = "path_logs"
        new_value = "/tmp/test_dir"
        result = ConfFileUtils().set_value(self.test_file, section_name, config_name, new_value)
        assert result is True
        result = ConfFileUtils().get_value(self.test_file, section_name, config_name)
        assert result == new_value
