# -*- encoding: utf-8 -*-
import errno
import gzip
import json
import os
import shutil
import struct
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zipfile import ZipFile
import fsspec
import requests
from .exceptions import get_exception
from .os_utils import OsUtils


class FileUtils:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def show(path: str) -> bool:
        """
        Open the given file or directory in explorer or notepad and returns True for success or False for failed access
        :param path:
        :return: bool
        """

        if not os.path.exists(path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
        try:
            return_code = 0
            match OsUtils.get_os_name():
                case "Windows":
                    os.startfile(path)
                case "Darwin":
                    return_code = subprocess.call(("open", path))
                case _:
                    return_code = subprocess.call(("xdg-open", path))
            return not bool(return_code)
        except Exception as e:
            sys.stderr.write(get_exception(e))
            raise e

    @staticmethod
    def list_files(directory: str, starts_with: str | tuple[str, ...] | list[str] = None, ends_with: str | tuple[str, ...] | list[str] = None) -> tuple:
        """
        List all files in the given directory and returns them in a list sorted by creation time in ascending order
        :param directory:
        :param starts_with:
        :param ends_with:
        :return: tuple
        """

        try:
            result = []
            if os.path.isdir(directory):
                if starts_with and ends_with:
                    result = [Path(os.path.join(directory, f)) for f in os.listdir(directory) if
                              f.lower().startswith(tuple(starts_with)) and
                              f.lower().endswith(tuple(ends_with))]
                elif starts_with:
                    result = [Path(os.path.join(directory, f)) for f in os.listdir(directory) if
                              f.lower().startswith(tuple(starts_with))]
                elif ends_with:
                    result = [Path(os.path.join(directory, f)) for f in os.listdir(directory) if
                              f.lower().endswith(tuple(ends_with))]
                else:
                    result = [Path(os.path.join(directory, f)) for f in os.listdir(directory)]
                result.sort(key=os.path.getctime)
            return tuple(result)
        except Exception as e:
            sys.stderr.write(get_exception(e))
            raise e

    @staticmethod
    def gzip(input_file_path: str, output_dir: str = None) -> Path | None:
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
            sys.stderr.write(get_exception(e))
            if os.path.isfile(output_file):
                os.remove(output_file)
            raise e

    @staticmethod
    def unzip(file_path: str, out_path: str = None) -> ZipFile | None:
        """
        Unzips the given file.zip and returns ZipFile for success or None if failed
        :param file_path:
        :param out_path:
        :return: ZipFile | None
        """

        try:
            out_path = out_path or os.path.dirname(file_path)
            with ZipFile(file_path) as zipf:
                zipf.extractall(out_path)
            return zipf
        except Exception as e:
            sys.stderr.write(get_exception(e))
            raise e

    @staticmethod
    def remove(path: str) -> bool:
        """
        Remove the given file and returns True if the file was successfully removed
        :param path:
        :return:
        """
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.exists(path):
                shutil.rmtree(path)
        except OSError as e:
            sys.stderr.write(get_exception(e))
            raise e
        return True

    @staticmethod
    def rename(from_name: str, to_name: str) -> bool:
        """
        Rename the given file and returns True if the file was successfully
        :param from_name:
        :param to_name:
        :return: bool
        """

        try:
            if os.path.exists(from_name):
                os.rename(from_name, to_name)
        except OSError as e:
            sys.stderr.write(get_exception(e))
            raise e
        return True

    @staticmethod
    def copy_dir(src, dst, symlinks=False, ignore=None) -> bool:
        """
        Copy files from src to dst and returns True or False
        :param src:
        :param dst:
        :param symlinks:
        :param ignore:
        :return: True or False
        """

        try:
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, symlinks, ignore)
                else:
                    shutil.copy2(s, d)
        except IOError as e:
            sys.stderr.write(get_exception(e))
            return False
        return True

    @staticmethod
    def download_file(remote_file_url, local_file_path) -> bool:
        """
        Download file from remote url to local and returns True or False
        :param remote_file_url:
        :param local_file_path:
        :return: True or False
        """

        try:
            req = requests.get(remote_file_url)
            if req.status_code == 200:
                with open(local_file_path, "wb") as outfile:
                    outfile.write(req.content)
                return True
        except requests.HTTPError as e:
            sys.stderr.write(get_exception(e))
        return False

    def download_github_dir(self, remote_dir_url: str, local_dir_path: str) -> bool:
        """
        Download directory from remote url to local and returns True or False
        Need to specify the branch on remote url
            example: https://github.com/ddc/ddcutils/blob/master/ddcutils/databases

        :param remote_dir_url:
        :param local_dir_path:
        :return:
        """

        try:
            if not os.path.exists(local_dir_path):
                os.makedirs(local_dir_path, exist_ok=True)

            req_dir = requests.get(remote_dir_url)
            if req_dir.status_code == 200:
                data_dict = json.loads(req_dir.content)
                files_list = data_dict["payload"]["tree"]["items"]
                for file in files_list:
                    remote_file_url = f"{remote_dir_url}/{file['name']}"
                    local_file_path = f"{local_dir_path}/{file['name']}"
                    if file["contentType"] == "directory":
                        self.download_github_dir(remote_file_url, local_file_path)
                    else:
                        req_file = requests.get(remote_file_url)
                        if req_file.status_code == 200:
                            data_dict = json.loads(req_file.content)
                            content = data_dict["payload"]["blob"]["rawLines"]
                            if not content:
                                payload = data_dict['payload']
                                url = (f"https://raw.githubusercontent.com/"
                                       f"{payload['repo']['ownerLogin']}/"
                                       f"{payload['repo']['name']}/"
                                       "master/"
                                       f"{payload['path']}")
                                req_file = requests.get(url)
                                with open(local_file_path, "wb") as outfile:
                                    outfile.write(req_file.content)
                            else:
                                with open(local_file_path, "w") as outfile:
                                    outfile.writelines([f"{line}\n" for line in content])

        except Exception as e:
            sys.stderr.write(get_exception(e))
            return False
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

    @staticmethod
    def copy(src_path, dst_path):
        """
        Copy a file to another location
        :param src_path:
        :param dst_path:
        :return:
        """

        try:

            shutil.copy(src_path, dst_path)
        except Exception as e:
            return e
        return True

    @staticmethod
    def download_filesystem_directory(org: str,
                                      repo: str,
                                      branch: str,
                                      remote_dir: str,
                                      local_dir: str,
                                      filesystem: str = "github",
                                      exist_ok: bool = True,
                                      parents: bool = True,
                                      recursive: bool = False) -> bool:
        """
        Downloads a filesystem directory and save it to a local directory
        :param org:
        :param repo:
        :param branch:
        :param remote_dir:
        :param local_dir:
        :param filesystem:
        :param exist_ok:
        :param parents:
        :param recursive:
        :return:
        """

        try:
            destination = Path(local_dir)
            destination.mkdir(exist_ok=exist_ok, parents=parents)
            fs = fsspec.filesystem(filesystem, org=org, repo=repo, sha=branch)
            remote_files = fs.ls(remote_dir)
            fs.get(remote_files, destination.as_posix(), recursive=recursive)
        except requests.HTTPError as e:
            sys.stderr.write(get_exception(e))
            return False
        return True
