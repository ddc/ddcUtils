# -*- encoding: utf-8 -*-
import configparser
import errno
import gzip
import json
import os
import shutil
import struct
import subprocess
import sys
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
    def _get_default_parser() -> configparser.ConfigParser:
        """
        Returns the parser
        :return configparser.ConfigParser:
        """

        parser = configparser.ConfigParser(delimiters="=", allow_no_value=True)
        parser.optionxform = str  # this will not change all values to lowercase
        parser._interpolation = configparser.ExtendedInterpolation()
        return parser

    @staticmethod
    def _get_parser_value(parser: configparser.ConfigParser, section: str, config_name: str) -> str | int | None:
        """
        Returns the value of the specified section in the given parser
        :param parser:
        :param section:
        :param config_name:
        :return: str | int | None
        """

        try:
            value = parser.get(section, config_name).replace("\"", "")
            lst_value = list(value.split(","))
            if len(lst_value) > 1:
                values = []
                for each in lst_value:
                    values.append(int(each.strip()) if each.strip().isnumeric() else each.strip())
                value = values
            elif value is not None and type(value) is str:
                if len(value) == 0:
                    value = None
                elif value.isnumeric():
                    value = int(value)
                elif "," in value:
                    value = sorted([x.strip() for x in value.split(",")])
            else:
                value = None
        except Exception as e:
            sys.stderr.write(get_exception(e))
            value = None
        return value

    def _get_section_data(self, parser: configparser.ConfigParser, section: str, final_data: dict, mixed_values: bool = True, include_section_name: bool = False):
        """
        Returns the section data from the given parser
        :param parser:
        :param section:
        :param final_data:
        :param mixed_values:
        :param include_section_name:
        :return: dict
        """

        for name in parser.options(section):
            section_name = section.replace(" ", "_")
            config_name = name.replace(" ", "_")
            value = self._get_parser_value(parser, section, name)
            if mixed_values and include_section_name:
                final_data[f"{section_name}.{config_name}"] = value
            elif mixed_values and not include_section_name:
                final_data[config_name] = value
            else:
                final_data[section_name][config_name] = value
        return final_data

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
            match OsUtils.get_os_name():
                case "Windows":
                    os.startfile(path)
                    return_code = 0
                case "Darwin":
                    return_code = subprocess.call(("open", path))
                case _:
                    return_code = subprocess.call(("xdg-open", path))
            return not bool(return_code)
        except Exception as e:
            sys.stderr.write(get_exception(e))
            return False

    @staticmethod
    def list_files(directory: str, starts_with: str = None, ends_with: str = None) -> list:
        """
        List all files in the given directory and returns them in a list
        :param directory:
        :param starts_with:
        :param ends_with:
        :return: list
        """

        result_list = []
        if os.path.isdir(directory):
            if starts_with and ends_with:
                result_list = [Path(os.path.join(directory, f)) for f in os.listdir(directory) if
                               f.lower().startswith(starts_with.lower()) and
                               f.lower().endswith(ends_with.lower())]
            elif starts_with:
                result_list = [Path(os.path.join(directory, f)) for f in os.listdir(directory) if
                               f.lower().startswith(starts_with.lower())]
            elif ends_with:
                result_list = [Path(os.path.join(directory, f)) for f in os.listdir(directory) if
                               f.lower().endswith(ends_with.lower())]
            else:
                result_list = [Path(os.path.join(directory, f)) for f in os.listdir(directory)]
            result_list.sort(key=os.path.getctime)
        return result_list

    @staticmethod
    def gzip(file_path: str) -> Path | None:
        """
        Compress the given file and returns the Path for success or None if failed
        :param file_path:
        :return: Path | None:
        """

        file_name = os.path.basename(file_path)
        gz_out_file_path = os.path.join(os.path.dirname(file_path), f"{file_name}.gz")

        try:
            with open(file_path, "rb") as fin:
                with gzip.open(gz_out_file_path, "wb") as fout:
                    fout.writelines(fin)
            return Path(gz_out_file_path)
        except Exception as e:
            sys.stderr.write(get_exception(e))
            if os.path.isfile(gz_out_file_path):
                os.remove(gz_out_file_path)
        return None

    @staticmethod
    def unzip(file_path: str, out_path: str = None) -> ZipFile | None:
        """
        Unzips the given file and returns ZipFile for success or None if failed
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
            return None

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
            return False
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
            return False
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

    def get_file_values(self, file_path: str, mixed_values: bool = False) -> dict:
        """
        Get all values from an .ini config file structure and returns them as a dictionary
        :param file_path:
        :param mixed_values:
        :return: dict
        """

        if not os.path.isfile(file_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
        final_data = {}
        parser = self._get_default_parser()
        try:
            parser.read(file_path)
            for section in parser.sections():
                if not mixed_values:
                    section_name = section.replace(" ", "_")
                    final_data[section_name] = {}
                final_data = self._get_section_data(parser, section, final_data, mixed_values, True)
        except Exception as e:
            sys.stderr.write(get_exception(e))
        return final_data

    def get_file_section_values(self, file_path: str, section: str) -> dict:
        """
        Get all section values from an .ini config file structure and returns them as a dictionary
        :param file_path:
        :param section:
        :return: dict
        """

        if not os.path.isfile(file_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
        final_data = {}
        parser = self._get_default_parser()
        try:
            parser.read(file_path)
            final_data = self._get_section_data(parser, section, final_data)
        except Exception as e:
            sys.stderr.write(get_exception(e))
        return final_data

    def get_file_value(self, file_path: str, section: str, config_name: str) -> str | int | None:
        """
        Get value from an .ini config file structure and returns it
        :param file_path:
        :param section:
        :param config_name:
        :return: str | int | None
        """

        if not os.path.isfile(file_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
        parser = self._get_default_parser()
        parser.read(file_path)
        value = self._get_parser_value(parser, section, config_name)
        return value

    def set_file_value(self, file_path: str, section_name: str, config_name: str, new_value) -> bool:
        """
        Set value from an .ini config file structure and returns True or False
        :param file_path:
        :param section_name:
        :param config_name:
        :param new_value:
        :return: True or False
        """

        if not os.path.isfile(file_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
        parser = self._get_default_parser()
        parser.read(file_path)
        if isinstance(new_value, str):
            new_value = f'"{new_value}"'
        parser.set(section_name, config_name, new_value)
        try:
            with open(file_path, "w") as configfile:
                parser.write(configfile, space_around_delimiters=False)
        except configparser.DuplicateOptionError as e:
            sys.stderr.write(get_exception(e))
            return False
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
        Downloads a GitHub directory and save it to a local directory
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
