# -*- encoding: utf-8 -*-
from ddcUtils import os_utils


class TestOsUtils:
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_get_current_path(self):
        result = os_utils.get_current_path()
        assert result.parts[-1] == "ddcUtils"

    def test_get_pictures_path(self):
        result = os_utils.get_pictures_path()
        assert "Pictures" in result.parts[-1]

    def test_get_downloads_path(self):
        result = os_utils.get_downloads_path()
        assert "Downloads" in result.parts[-1]
