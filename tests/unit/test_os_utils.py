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
