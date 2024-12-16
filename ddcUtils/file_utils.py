# -*- encoding: utf-8 -*-
import errno
import gzip
import os
import shutil
import struct
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from zipfile import ZipFile
import requests
from .os_utils import OsUtils


class FileUtils:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def open(path: str) -> bool:
        """
        Open the given file or directory in explorer or notepad
            and returns True for success or False for failed access

        :param path:
        :return: bool
        """

        if not os.path.exists(path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
        try:
            return_code: int = 0
            match OsUtils.get_os_name():
                case "Windows":
                    os.startfile(path)
                case "Darwin":
                    return_code = subprocess.call(("open", path))
                case _:
                    return_code = subprocess.call(("xdg-open", path))
            return not bool(return_code)
        except Exception as e:
            sys.stderr.write(repr(e))
            raise e

    @staticmethod
    def list_files(
        directory: str,
        starts_with: Optional[str] = None,
        ends_with: Optional[str] = None
    ) -> tuple:

        """
        List all files in the given directory and returns them in a list
            sorted by creation time in ascending order

        :param directory:
        :param starts_with:
        :param ends_with:
        :return: tuple
        """

        try:
            result: list = []
            if os.path.isdir(directory):
                if starts_with and ends_with:
                    result: list = [Path(os.path.join(directory, f)) for f in os.listdir(directory) if
                                    f.lower().startswith(starts_with) and
                                    f.lower().endswith(ends_with.lower())]
                elif starts_with:
                    result: list = [Path(os.path.join(directory, f)) for f in os.listdir(directory) if
                                    f.lower().startswith(starts_with.lower())]
                elif ends_with:
                    result: list = [Path(os.path.join(directory, f)) for f in os.listdir(directory) if
                                    f.lower().endswith(ends_with.lower())]
                else:
                    result: list = [Path(os.path.join(directory, f)) for f in os.listdir(directory)]
                result.sort(key=os.path.getctime)
            return tuple(result)
        except Exception as e:
            sys.stderr.write(repr(e))
            raise e

    @staticmethod
    def gzip(input_file_path: str, output_dir: Optional[str] = None) -> Path | None:
        """
        Compress the given file and returns the Path for success or None if failed

        :param input_file_path:
        :param output_dir:
        :return: Path | None:
        """

        if not output_dir:
            output_dir = os.path.dirname(input_file_path)

        input_file_name = os.path.basename(input_file_path)
        output_filename = f"{os.path.splitext(input_file_name)[0]}.gz"
        output_file = os.path.join(output_dir, output_filename)

        try:
            with open(input_file_path, "rb") as fin:
                with gzip.open(output_file, "wb") as fout:
                    fout.writelines(fin)
            return Path(output_file)
        except Exception as e:
            sys.stderr.write(repr(e))
            if os.path.isfile(output_file):
                os.remove(output_file)
            raise e

    @staticmethod
    def unzip(file_path: str, out_path: Optional[str]  = None) -> ZipFile | None:
        """
        Unzips the given file.zip and returns ZipFile for success or None if failed

        :param file_path:
        :param out_path:
        :return: ZipFile | None
        """

        try:
            out_path: str = out_path or os.path.dirname(file_path)
            with ZipFile(file_path) as zipf:
                zipf.extractall(out_path)
            return zipf
        except Exception as e:
            sys.stderr.write(repr(e))
            raise e

    @staticmethod
    def copy(src_path: str, dst_path: str) -> bool:
        """
        Copy a file to another location

        :param src_path:
        :param dst_path:
        :return:
        """

        try:

            shutil.copy(src_path, dst_path)
            return True
        except Exception as e:
            sys.stderr.write(repr(e))
            raise e


    @staticmethod
    def remove(path: str) -> bool:
        """
        Remove the given file and returns True if the file was successfully removed

        :param path:
        :return: True
        """
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.exists(path):
                shutil.rmtree(path)
            else:
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
        except OSError as e:
            sys.stderr.write(repr(e))
            raise e
        return True

    @staticmethod
    def rename(from_name: str, to_name: str) -> bool:
        """
        Rename the given file and returns True if the file was successfully renamed

        :param from_name:
        :param to_name:
        :return: True
        """

        try:
            if os.path.exists(from_name):
                os.rename(from_name, to_name)
            return True
        except OSError as e:
            sys.stderr.write(repr(e))
            raise e

    @staticmethod
    def copy_dir(
        src: str,
        dst: str,
        symlinks: Optional[bool] = False,
        ignore: Optional = None
    ) -> bool:

        """
        Copy files from src to dst and returns True if the copy was successfull

        :param src:
        :param dst:
        :param symlinks:
        :param ignore:
        :return: True
        """

        try:
            shutil.copytree(src, dst, symlinks, ignore, dirs_exist_ok=True)
        except IOError as e:
            sys.stderr.write(repr(e))
            raise e
        return True

    @staticmethod
    def download_file(remote_file_url: str, local_file_path: str) -> bool:
        """
        Download file from remote url to local
            and returns True if the download was successfull

        :param remote_file_url:
        :param local_file_path:
        :return: True
        """

        try:
            req = requests.get(remote_file_url)
            if req.status_code == 200:
                with open(local_file_path, "wb") as outfile:
                    outfile.write(req.content)
        except requests.HTTPError as e:
            sys.stderr.write(repr(e))
            raise e
        return True

    @staticmethod
    def get_exe_binary_type(file_path: str) -> str | None:
        """
        Returns the binary type of the given EXE file

        :param file_path:
        :return: str | None
        """

        with open(file_path, "rb") as f:
            s = f.read(2)
            if s != b"MZ":
                return "Not an EXE file"
            f.seek(60)
            s = f.read(4)
            header_offset = struct.unpack("<L", s)[0]
            f.seek(header_offset + 4)
            s = f.read(2)
            machine = struct.unpack("<H", s)[0]
            match machine:
                case 332:
                    # IA32 (32-bit x86)
                    binary_type = "IA32"
                case 512:
                    # IA64 (Itanium)
                    binary_type = "IA64"
                case 34404:
                    # IAMD64 (64-bit x86)
                    binary_type = "AMD64"
                case 452:
                    # IARM eabi (32-bit)
                    binary_type = "ARM-32bits"
                case 43620:
                    # IAArch64 (ARM-64, 64-bit)
                    binary_type = "ARM-64bits"
                case _:
                    binary_type = None
        return binary_type

    @staticmethod
    def is_older_than_x_days(path: str, days: int) -> bool:
        """
        Check if a file or directory is older than the specified number of days

        :param path:
        :param days:
        :return:
        """

        if not os.path.exists(path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

        if int(days) == 1:
            cutoff_time = datetime.today()
        else:
            cutoff_time = datetime.today() - timedelta(days=int(days))

        stats = os.stat(path)
        days_epoch = cutoff_time.timestamp()
        if stats.st_ctime < days_epoch:
            return True
        return False
