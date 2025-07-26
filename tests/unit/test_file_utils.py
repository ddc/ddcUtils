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

    def test_open_file(self):
        # nonexistent file
        with pytest.raises(FileNotFoundError) as exc_info:
            FileUtils.open(self.unknown_file)
        assert exc_info.value.args[0] == 2
        assert exc_info.value.args[1] == "No such file or directory"
        assert exc_info.typename == "FileNotFoundError"

    def test_file_utils_init(self):
        # Test FileUtils constructor
        fu = FileUtils("arg1", "arg2", key1="value1", key2="value2")
        assert fu.args == ("arg1", "arg2")
        assert fu.kwargs == {"key1": "value1", "key2": "value2"}

    def test_open_with_exception(self):
        # Test open method exception handling
        import unittest.mock

        with unittest.mock.patch('ddcUtils.file_utils.OsUtils.get_os_name', side_effect=Exception("Test error")):
            with pytest.raises(Exception) as exc_info:
                FileUtils.open(self.test_file)
            assert "Test error" in str(exc_info.value)

    def test_open_darwin(self):
        # Test open on Darwin (macOS)
        import unittest.mock

        with unittest.mock.patch('ddcUtils.file_utils.OsUtils.get_os_name', return_value='Darwin'):
            with unittest.mock.patch('subprocess.call', return_value=0) as mock_call:
                result = FileUtils.open(self.test_file)
                assert result is True
                mock_call.assert_called_once_with(('open', self.test_file))

    def test_open_linux(self):
        # Test open on Linux
        import unittest.mock

        with unittest.mock.patch('ddcUtils.file_utils.OsUtils.get_os_name', return_value='linux'):
            with unittest.mock.patch('subprocess.call', return_value=0) as mock_call:
                result = FileUtils.open(self.test_file)
                assert result is True
                mock_call.assert_called_once_with(('xdg-open', self.test_file))

    def test_open_linux_failure(self):
        # Test open on Linux with failure
        import unittest.mock

        with unittest.mock.patch('ddcUtils.file_utils.OsUtils.get_os_name', return_value='linux'):
            with unittest.mock.patch('subprocess.call', return_value=1) as mock_call:
                result = FileUtils.open(self.test_file)
                assert result is False
                mock_call.assert_called_once_with(('xdg-open', self.test_file))

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

    def test_list_files_with_both_filters(self):
        # Test with both starts_with and ends_with
        result = FileUtils.list_files(self.test_files_dir, starts_with="test", ends_with=".ini")
        assert Path(self.test_file) in result

    def test_list_files_non_directory(self):
        # Test with non-directory path
        result = FileUtils.list_files("/nonexistent/directory")
        assert result == ()

    def test_list_files_exception(self):
        # Test exception handling in list_files
        import unittest.mock

        with unittest.mock.patch('os.path.isdir', side_effect=Exception("Test error")):
            with pytest.raises(Exception) as exc_info:
                FileUtils.list_files(self.test_files_dir)
            assert "Test error" in str(exc_info.value)

    def test_gzip_file(self):
        # test gzip file and delete afterward
        result_file = FileUtils.gzip(self.test_file, self.temp_test_dir)
        assert os.path.isfile(result_file)
        FileUtils.remove(str(result_file))

    @pytest.mark.skipif(os.name == 'nt', reason="Windows-specific test moved to test_file_utils_windows.py")
    def test_unzip_file(self):
        # test unzip file and delete afterwards (Unix/Linux)
        result = FileUtils.unzip(self.test_zip_file, self.temp_test_dir)
        assert result is not None
        test_file = os.path.join(self.temp_test_dir, result.filelist[0].filename)
        files_list = FileUtils.list_files(self.temp_test_dir)
        assert Path(test_file) in files_list
        FileUtils.remove(test_file)

    def test_copy_and_remove(self):
        # test copy - delete afterward
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
        # test copy and rename file - delete afterward
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
        # test download file with mock - delete afterward
        import unittest.mock

        dst_file = os.path.join(self.test_files_dir, "test_download.txt")

        # Mock the requests.get to avoid actual network call
        mock_response = unittest.mock.MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = [b"test content chunk"]
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None

        with unittest.mock.patch('requests.get', return_value=mock_response):
            result = FileUtils.download_file("https://example.com/test.txt", dst_file)
            assert result is True

        # Verify file was created and has content
        assert os.path.exists(dst_file)
        with open(dst_file, 'rb') as f:
            content = f.read()
            assert content == b"test content chunk"

        # Clean up
        result = FileUtils.remove(dst_file)
        assert result is True

    def test_get_binary_type(self):
        # test file binary type
        result = FileUtils.get_exe_binary_type(self.test_file)
        assert result == "Not an EXE file"

    @pytest.mark.skipif(os.name == 'nt', reason="Windows-specific test moved to test_file_utils_windows.py")
    def test_is_older_than_x_days(self):
        # Create a temporary file and set its modification time (Unix/Linux)
        from datetime import datetime, timedelta

        temp_file = os.path.join(self.temp_test_dir, "test_old_file_unix.txt")
        with open(temp_file, 'w') as f:
            f.write("test content")

        # Set file time to 2 days ago
        two_days_ago = datetime.now() - timedelta(days=2)
        old_timestamp = two_days_ago.timestamp()
        os.utime(temp_file, (old_timestamp, old_timestamp))

        # Test file is older than 1 day
        result = FileUtils.is_older_than_x_days(temp_file, 1)
        assert result is True

        # Test file is not older than 99999 days
        result = FileUtils.is_older_than_x_days(temp_file, 99999)
        assert result is False

        # Clean up
        FileUtils.remove(temp_file)

        # nonexistent file
        with pytest.raises(FileNotFoundError) as exc_info:
            FileUtils.is_older_than_x_days(self.unknown_file, 1)
        assert exc_info.value.args[0] == 2
        assert exc_info.value.args[1] == "No such file or directory"
        assert exc_info.typename == "FileNotFoundError"

    def test_gzip_file_no_output_dir(self):
        # test gzip file without specifying output directory
        result_file = FileUtils.gzip(self.test_file)
        assert os.path.isfile(result_file)
        assert result_file.parent == Path(self.test_file).parent
        FileUtils.remove(str(result_file))

    def test_gzip_file_exception(self):
        # Test gzip with invalid input file
        with pytest.raises(Exception):
            FileUtils.gzip("/nonexistent/file.txt")

    def test_unzip_file_no_output_path(self):
        # test unzip file without specifying output path
        result = FileUtils.unzip(self.test_zip_file)
        assert result is not None
        # Clean up extracted files
        for file_info in result.filelist:
            extracted_file = os.path.join(self.test_files_dir, file_info.filename)
            if os.path.exists(extracted_file):
                FileUtils.remove(extracted_file)

    def test_unzip_file_exception(self):
        # Test unzip with invalid file
        with pytest.raises(Exception):
            FileUtils.unzip("/nonexistent/file.zip")

    def test_copy_exception(self):
        # Test copy with exception
        with pytest.raises(Exception):
            FileUtils.copy("/nonexistent/file.txt", "/some/destination.txt")

    def test_rename_nonexistent_file(self):
        # Test rename with non-existent file (should still return True)
        result = FileUtils.rename("/nonexistent/file.txt", "/some/newname.txt")
        assert result is True

    def test_rename_exception(self):
        # Test rename with OS error
        import unittest.mock

        with unittest.mock.patch('os.path.exists', return_value=True):
            with unittest.mock.patch('os.rename', side_effect=OSError("Permission denied")):
                with pytest.raises(OSError):
                    FileUtils.rename(self.test_file, "/invalid/path/newname.txt")

    def test_copy_dir_with_symlinks(self):
        # test copy directory with symlinks enabled
        dst_dir = os.path.join(self.test_files_dir, "test_dir_symlinks")
        result = FileUtils.copy_dir(self.test_files_dir, dst_dir, symlinks=True)
        assert result is True
        result = FileUtils.remove(dst_dir)
        assert result is True

    def test_copy_dir_exception(self):
        # Test copy_dir with IO error
        with pytest.raises(Exception):
            FileUtils.copy_dir("/nonexistent/source", "/invalid/destination")

    def test_download_file_exception(self):
        # Test download with request exception
        import unittest.mock
        import requests

        dst_file = os.path.join(self.test_files_dir, "test_download_fail.txt")

        with unittest.mock.patch('requests.get', side_effect=requests.RequestException("Network error")):
            with pytest.raises(requests.RequestException):
                FileUtils.download_file("https://example.com/test.txt", dst_file)
