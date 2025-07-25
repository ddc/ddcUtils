# -*- encoding: utf-8 -*-
from ddcUtils import OsUtils


class TestOsUtils:
    @classmethod
    def setup_class(cls):
        """
        Leaving empty for further use
        """
        pass

    @classmethod
    def teardown_class(cls):
        """
        Leaving empty for further use
        """
        pass

    def test_get_current_path(self):
        result = OsUtils.get_current_path()
        assert result.parts[-1] == "ddcUtils"

    def test_get_pictures_path(self):
        result = OsUtils().get_pictures_path()
        assert "Pictures" in result.parts[-1]

    def test_get_downloads_path(self):
        result = OsUtils().get_downloads_path()
        assert "Downloads" in result.parts[-1]

    def test_get_os_name(self):
        result = OsUtils.get_os_name()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_is_windows(self):
        result = OsUtils.is_windows()
        assert isinstance(result, bool)

    def test_get_pictures_path_windows(self):
        # Test Windows path with mock
        import unittest.mock
        
        mock_winreg = unittest.mock.MagicMock()
        mock_key_context = unittest.mock.MagicMock()
        mock_winreg.OpenKey.return_value.__enter__.return_value = mock_key_context
        mock_winreg.QueryValueEx.return_value = ("C:\\Users\\Test\\Pictures", None)
        mock_winreg.HKEY_CURRENT_USER = "HKEY_CURRENT_USER"
        
        with unittest.mock.patch('ddcUtils.os_utils.OsUtils.is_windows', return_value=True):
            with unittest.mock.patch.dict('sys.modules', {'winreg': mock_winreg}):
                ou = OsUtils()
                result = ou.get_pictures_path()
                assert "Pictures" in str(result)

    def test_get_pictures_path_unix(self):
        # Test Unix/Linux path
        import unittest.mock
        import os
        
        with unittest.mock.patch('ddcUtils.os_utils.OsUtils.is_windows', return_value=False):
            with unittest.mock.patch.dict(os.environ, {'HOME': '/home/testuser'}):
                ou = OsUtils()
                result = ou.get_pictures_path()
                assert str(result) == "/home/testuser/Pictures"

    def test_get_downloads_path_windows(self):
        # Test Windows downloads path with mock
        import unittest.mock
        
        mock_winreg = unittest.mock.MagicMock()
        mock_key_context = unittest.mock.MagicMock()
        mock_winreg.OpenKey.return_value.__enter__.return_value = mock_key_context
        mock_winreg.QueryValueEx.return_value = ("C:\\Users\\Test\\Downloads", None)
        mock_winreg.HKEY_CURRENT_USER = "HKEY_CURRENT_USER"
        
        with unittest.mock.patch('ddcUtils.os_utils.OsUtils.is_windows', return_value=True):
            with unittest.mock.patch.dict('sys.modules', {'winreg': mock_winreg}):
                ou = OsUtils()
                result = ou.get_downloads_path()
                assert "Downloads" in str(result)

    def test_get_downloads_path_unix(self):
        # Test Unix/Linux downloads path
        import unittest.mock
        import os
        
        with unittest.mock.patch('ddcUtils.os_utils.OsUtils.is_windows', return_value=False):
            with unittest.mock.patch.dict(os.environ, {'HOME': '/home/testuser'}):
                ou = OsUtils()
                result = ou.get_downloads_path()
                assert str(result) == "/home/testuser/Downloads"

    def test_is_windows_with_cli_platform(self):
        # Test Windows detection with CLI platform
        import unittest.mock
        
        with unittest.mock.patch('sys.platform', 'cli'):
            with unittest.mock.patch('os.name', 'nt'):
                result = OsUtils.is_windows()
                assert result is True

    def test_is_windows_false_cases(self):
        # Test cases where is_windows should return False
        import unittest.mock
        
        with unittest.mock.patch('sys.platform', 'linux'):
            with unittest.mock.patch('os.name', 'posix'):
                result = OsUtils.is_windows()
                assert result is False

    def test_get_current_path_type(self):
        # Test that get_current_path returns a Path object
        result = OsUtils.get_current_path()
        from pathlib import Path
        assert isinstance(result, Path)
        assert result.is_absolute()
