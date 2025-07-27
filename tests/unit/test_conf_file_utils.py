import configparser
import os
import tempfile
import pytest
from ddcUtils import ConfFileUtils, constants


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
        new_value = f"{tempfile.gettempdir()}/test_dir"
        result = ConfFileUtils().set_value(self.test_file, section_name, config_name, new_value)
        assert result is True
        result = ConfFileUtils().get_value(self.test_file, section_name, config_name)
        assert result == new_value

    def test_get_default_parser(self):
        parser = ConfFileUtils._get_default_parser()
        assert parser is not None
        assert hasattr(parser, 'read')
        assert hasattr(parser, 'get')

    def test_get_parser_value_with_commas(self):
        # Test with comma-separated values
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write("[section]\nkey=1,2,3,4,5\n")
            temp_file = f.name

        try:
            parser = ConfFileUtils._get_default_parser()
            parser.read(temp_file)
            result = ConfFileUtils._get_parser_value(parser, "section", "key")
            assert isinstance(result, list)
            assert result == [1, 2, 3, 4, 5]
        finally:
            os.unlink(temp_file)

    def test_get_parser_value_with_string(self):
        # Test with string values
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write("[section]\nkey=\"test_value\"\n")
            temp_file = f.name

        try:
            parser = ConfFileUtils._get_default_parser()
            parser.read(temp_file)
            result = ConfFileUtils._get_parser_value(parser, "section", "key")
            assert result == "test_value"
        finally:
            os.unlink(temp_file)

    def test_set_value_with_commas(self):
        # Test setting value with commas
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write("[section]\nkey=old_value\n")
            temp_file = f.name

        try:
            result = ConfFileUtils().set_value(temp_file, "section", "key", "1,2,3", commas=True)
            assert result is True

            # Verify the value was set (it gets parsed as a list)
            value = ConfFileUtils().get_value(temp_file, "section", "key")
            assert value == [1, 2, 3]
        finally:
            os.unlink(temp_file)

    def test_get_parser_value_empty_value(self):
        # Test with empty value to cover line 43
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write("[section]\nkey=\n")
            temp_file = f.name

        try:
            parser = ConfFileUtils._get_default_parser()
            parser.read(temp_file)
            result = ConfFileUtils._get_parser_value(parser, "section", "key")
            assert result is None
        finally:
            os.unlink(temp_file)

    def test_get_parser_value_exception(self):
        # Test exception handling in _get_parser_value
        import unittest.mock

        parser = ConfFileUtils._get_default_parser()
        with unittest.mock.patch.object(parser, 'get', side_effect=ValueError("Test error")):
            result = ConfFileUtils._get_parser_value(parser, "section", "key")
            assert result is None

    def test_get_all_values_exception(self):
        # Test exception handling in get_all_values
        import unittest.mock

        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write("[section]\nkey=value\n")
            temp_file = f.name

        try:
            with unittest.mock.patch('configparser.ConfigParser.read', side_effect=configparser.Error("Parse error")):
                result = ConfFileUtils().get_all_values(temp_file)
                assert result == {}
        finally:
            os.unlink(temp_file)

    def test_get_section_values_exception(self):
        # Test exception handling in get_section_values
        import unittest.mock

        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write("[section]\nkey=value\n")
            temp_file = f.name

        try:
            with unittest.mock.patch('configparser.ConfigParser.read', side_effect=configparser.Error("Parse error")):
                result = ConfFileUtils().get_section_values(temp_file, "section")
                assert result == {}
        finally:
            os.unlink(temp_file)

    def test_get_value_nonexistent_file(self):
        # Test get_value with nonexistent file to cover line 131
        with pytest.raises(FileNotFoundError) as exc_info:
            ConfFileUtils().get_value(self.unknown_file, "section", "key")
        assert exc_info.value.args[0] == 2

    def test_set_value_nonexistent_file(self):
        # Test set_value with nonexistent file to cover line 151
        with pytest.raises(FileNotFoundError) as exc_info:
            ConfFileUtils().set_value(self.unknown_file, "section", "key", "value")
        assert exc_info.value.args[0] == 2

    def test_set_value_duplicate_option_error(self):
        # Test DuplicateOptionError handling in set_value to cover lines 161-163
        import unittest.mock
        import tempfile
        import configparser

        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write("[section]\nkey=value\n")
            temp_file = f.name

        try:
            # Mock ConfigParser.write to raise DuplicateOptionError
            with unittest.mock.patch(
                'configparser.ConfigParser.write',
                side_effect=configparser.DuplicateOptionError("section", "key", "source"),
            ):
                result = ConfFileUtils().set_value(temp_file, "section", "key", "new_value")
                assert result is False
        finally:
            os.unlink(temp_file)
