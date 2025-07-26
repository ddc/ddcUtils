from datetime import datetime, timezone
from ddcUtils import constants, MiscUtils, Object


class TestMiscUtils:
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

    def test_convert_datetime_to_str_long(self):
        now_utc = datetime.now(timezone.utc)
        result = MiscUtils.convert_datetime_to_str_long(now_utc)
        assert result == now_utc.strftime(f"{constants.DATE_TIME_FORMATTER_STR}")

    def test_convert_datetime_to_str_short(self):
        now_utc = datetime.now(timezone.utc)
        result = MiscUtils.convert_datetime_to_str_short(now_utc)
        assert result == now_utc.strftime(f"{constants.DATE_FORMATTER} {constants.TIME_FORMATTER}")

    def test_convert_str_to_datetime_short(self):
        date_str = "2024-01-01 00:00:00.000000"
        result = MiscUtils.convert_str_to_datetime_short(date_str)
        assert result == datetime.strptime(date_str, f"{constants.DATE_FORMATTER} {constants.TIME_FORMATTER}")

    def test_get_current_date_time_str_long(self):
        result = MiscUtils().get_current_date_time_str_long()
        now_utc = datetime.now(timezone.utc)
        assert result == now_utc.strftime(constants.DATE_TIME_FORMATTER_STR)

    def test_object(self):
        new_object = Object()
        new_object.test = "tttt"
        t1 = new_object.to_json()
        t2 = new_object.to_dict()
        assert type(t1) is str
        assert type(t2) is dict

    def test_get_current_date_time(self):
        result = MiscUtils.get_current_date_time()
        assert result.tzinfo == timezone.utc
        assert isinstance(result, datetime)

    def test_clear_screen(self):
        # Test that clear_screen doesn't raise an exception
        try:
            MiscUtils.clear_screen()
        except Exception:
            assert False, "clear_screen should not raise an exception"

    def test_user_choice(self):
        # Cannot easily test interactive input, but test structure
        import builtins

        original_input = builtins.input
        builtins.input = lambda _: "test input"
        try:
            result = MiscUtils.user_choice()
            assert result == "test input"
        finally:
            builtins.input = original_input

    def test_get_active_branch_name_no_git(self):
        result = MiscUtils.get_active_branch_name("/nonexistent/path/.git")
        assert result is None
