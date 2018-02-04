#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import re
import os
import sys
import json
import xmltodict
import platform
import importlib
import subprocess

from core.interface import ask
from core.interface import print_line
from core.webapi import WebAPI

raw_npm_components = []


def walkdict(data):
    """
    Recursive dict processing for npm list parsing.
    :param data:
    :return:
    """
    for k, v in data.items():
        if isinstance(v, dict):
            walkdict(v)
        else:
            raw_npm_components.append({"name": k, "version": v})


class ComponentsHelper(object):

    def __init__(self):
        self.web_api = WebAPI()

    # -------------------------------------------------------------------------
    # Components
    # -------------------------------------------------------------------------

    def get_components_os_auto_system_none(self, api_data):
        """
        Get components of OS by calling of shell script and than parse them.
        :param api_data: api data set
        :return: result
        """
        if api_data['os_type'] == OSs.WINDOWS:
            if api_data['os_version'] == '10' or api_data['os_version'] == '8':
                os_packages = self.load_windows_10_packages_from_shell()[0]
                if os_packages is None:
                    print_line('Failed to load OS components.')
                    return [None]
                report = os_packages.decode('utf-8').replace('\r', '').split('\n')[9:]
                components = self.parse_windows_10_packages(report)
                if components[0] is None:
                    print_line('Failed parse OS components.')
                    return [None]
                return components
            elif api_data['os_version'] == '7':
                print_line('Windows 7 does not support yet.')
                return [None]
            else:
                print_line('Windows type not defined.')
                return [None]
        elif api_data['os_type'] == OSs.MACOS:
            os_packages = self.load_macos_packages_from_shell()[0]
            if os_packages is None:
                print_line('Failed to load OS components.')
                return [None]
            components = self.parse_macos_packages(os_packages)
            if components[0] is None:
                print_line('Failed parse OS components.')
                return [None]
            return components
        elif api_data['os_type'] == OSs.CENTOS:
            print_line('CentOS not support yet.')
            return [None]
        elif api_data['os_type'] == OSs.DEBIAN:
            os_packages = self.load_ubuntu_packages_from_shell()[0]
            if os_packages is None:
                print_line('Failed to load OS components.')
                return [None]
            components = self.parse_ubuntu_packages(os_packages)
            if components[0] is None:
                print_line('Failed parse OS components.')
                return [None]
            return components
        elif api_data['os_type'] == OSs.FEDORA:
            os_packages = self.load_fedora_packages_from_shell()[0]
            if os_packages is None:
                print_line('Failed to load OS components.')
                return [None]
            components = self.parse_fedora_packages(os_packages)
            if components[0] is None:
                print_line('Failed parse OS components.')
                return [None]
            return components
        return [None]

    def get_components_os_auto_system_path(self, api_data):
        """
        Get OS packages from file, defined by path, which were created by calling the shell command.
        :param api_data: api data set
        :return: result
        """
        if api_data['os_type'] == OSs.WINDOWS:
            if api_data['os_version'] == '10' or api_data['os_version'] == '8':
                report = self.load_windows_10_packages_from_path(api_data['file'])[0]
                if report is None:
                    return [None]
                components = self.parse_windows_10_packages(report=report)
                if components[0] is None:
                    return [None]
                return components
            if api_data['os_version'] == '7':
                print_line('Windows 7 does not support yet.')
                return [None]
        elif api_data['os_type'] == OSs.MACOS:
            os_packages = self.load_macos_packages_from_path(api_data['file'])[0]
            if os_packages is None:
                print_line('Failed to load OS components.')
                return [None]
            components = self.parse_macos_packages(os_packages)
            if components[0] is None:
                print_line('Failed parse OS components.')
                return [None]
            return components
        elif api_data['os_type'] == OSs.CENTOS:
            print_line('CentOS does not support yet.')
            return [None]
        elif api_data['os_type'] == OSs.DEBIAN or api_data['os_type'] == OSs.UBUNTU:
            os_packages = self.load_ubuntu_packages_from_path(api_data['file'])[0]
            if os_packages is None:
                print_line('Failed to load OS components.')
                return [None]
            components = self.parse_ubuntu_packages(os_packages)
            if components[0] is None:
                print_line('Failed parse OS components.')
                return [None]
            return components
        elif api_data['os_type'] == OSs.FEDORA:
            os_packages = self.load_fedora_packages_from_path(api_data['file'])[0]
            if os_packages is None:
                print_line('Failed to load OS components.')
                return [None]
            components = self.parse_fedora_packages(os_packages)
            if components[0] is None:
                print_line('Failed parse OS components.')
                return [None]
            return components
        else:
            return [None]

    def get_components_pip_auto_system_none(self):
        """
        Get Python PIP components, collected by pip frozen requirements call.
        :return: result
        """
        report = self.load_pip_packages_from_shell_legacy()

        if report[0] is None:
            print_line('Problems with PIP components loading.')
            return [None]

        return self.parse_pip_packages_legacy(report)

    def get_components_pip_auto_system_path(self, api_data):
        """
        Get Python PIP components from file, defined by path.
        :param api_data: api data set
        :return: result
        """
        packages = self.load_pip_packages_from_path(api_data['file'])
        if packages[0] is not None:
            return self.parse_pip_packages_from_path(packages=packages)
        print_line('Something wrong with packages in file path {0}.'.format(api_data['file']))
        return [None]

    def get_components_requirements_auto_system_path(self, api_data):
        """
        Get Python PIP components from requirements.txt file, defined by path.
        :param api_data: api data set
        :return: result
        """
        packages = self.load_pip_packages_from_path(api_data['file'])
        if packages[0] is not None:
            return self.parse_pip_packages_from_path(packages=packages)
        print_line('Something wrong with packages in file path {0}.'.format(api_data['file']))
        return [None]

    def get_components_npm_auto_system_path(self, api_data):
        """
        Get NPM packages, collected from file, defined by path.
        :param api_data:
        :return:
        """
        packages = self.load_npm_packages_from_path(api_data['file'])
        if packages[0] is not None:
            return self.parse_npm_packages(api_data=api_data, comp=raw_npm_components)
        print_line('Something wrong with packages in file path {0}.'.format(api_data['file']))
        return [None]

    def get_components_package_json_auto_system_path(self, api_data):
        """
        Get NPM packages from package.json file, defined by path.
        :param api_data: api data set
        :return: result
        """
        packages = self.load_package_json_packages_from_path(api_data['file'])
        if packages[0] is not None:
            return self.parse_package_json_packages_from_path(packages[0])
        print_line('Something wrong with packages in file path {0}.'.format(api_data['file']))
        return [None]

    def get_components_gem_auto_system_path(self, api_data):
        """
        Get Ruby gem packages, collected from file, defined by path.
        :param api_data: api data set
        :return: result
        """
        packages = self.load_gem_packages_from_path(api_data['file'])
        if packages[0] is not None:
            return self.parse_gem_packages_from_path(packages[0])
        print_line('Something wrong with packages in file path {0}.'.format(api_data['file']))
        return [None]

    def get_components_npm_auto_system_none(self, api_data):
        """
        Get NPM packages, collected from shell command, that is called globally.
        :param api_data: api data set
        :return: result
        """
        packages = self.load_npm_packages(api_data=api_data, local=False)
        if packages[0] is not None:
            return self.parse_npm_packages(api_data=api_data, comp=raw_npm_components)
        print_line('Something wrong with packages in NPM system call.')
        return [None]

    def get_components_npm_local_auto_system_none(self, api_data):
        """
        Get NPM packages, collected from shell command, that is called locally from path.
        :param api_data: api data set
        :return: result
        """
        packages = self.load_npm_packages(api_data=api_data, local=True)
        if packages[0] is not None:
            return self.parse_npm_packages(api_data=api_data, comp=raw_npm_components)
        print_line('Something wrong with packages in file path')
        return [None]

    def get_components_npm_lock_auto_system_path(self, api_data):
        """
        Get NPM packages from lock file, defined by path.
        :param api_data: api data set
        :return: result
        """
        packages = self.load_npm_lock_packages_from_path(filename=api_data['file'])
        if packages[0] is not None:
            return self.parse_npm_lock_packages(packages[0])
        print_line('Something wrong with packages in file path')
        return [None]

    def get_components_gem_auto_system_none(self, api_data):
        """
        Get Ruby gem packages, collected from shell command, that is called globally.
        :param api_data: api data set
        :return: result
        """
        packages = self.load_gem_packages_system(local=False, api_data=api_data)
        if packages[0] is not None:
            return self.parse_gem_packages_system(packages=packages[0])
        print_line('Something wrong with packages in file path')
        return [None]

    def get_components_gemfile_auto_system_path(self, api_data):
        """
        Get Ruby gem packages, collected from Gemfile, defined by path.
        :param api_data: api data set
        :return: result
        """
        packages = self.load_gemfile_packages_from_path(filename=api_data['file'])
        if packages[0] is None:
            print('Gemfile packages loading error.')
            return [None]
        components = self.parse_gemfile_packages(packages=packages)
        if components[0] is None:
            print_line('Failed parse Gemfile packages.')
            return [None]
        return components

    def get_components_gemfile_lock_auto_system_path(self, api_data):
        """
        Get Ruby gem packages, collected from Gemfile.lock, defined by path.
        :param api_data: api data set
        :return: result
        """
        packages = self.load_gemfile_lock_packages_from_path(filename=api_data['file'])
        if packages[0] is None:
            print('Gemfile packages loading error.')
            return [None]
        components = self.parse_gemfile_lock_packages(packages=packages)
        if components[0] is None:
            print_line('Failed parse Gemfile packages.')
            return [None]
        return components

    def get_components_any_auto_user_path(self, api_data):
        """
        Get any components from file, defined by path.
        :param api_data: api data set
        :return: result
        """
        filename = api_data['file']
        if os.path.isfile(filename):
            enc = self.define_file_encoding(filename=filename)
            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return [None]
            components = []
            with open(filename, 'r', encoding=enc) as pf:
                packages = pf.read().split('\n')
                for package in packages:
                    if len(package) != 0:
                        if '=' in package:
                            splitted_package = package.split('=')
                            if len(splitted_package) == 2:
                                components.append({'name': splitted_package[0], 'version': splitted_package[1]})
                return components
        print_line('File {0} not found.'.format(filename))
        return [None]

    @staticmethod
    def get_components_any_manual_user_none():
        """
        Get packages from console.
        :return:
        """
        components = []
        if ask('Continue (y/n)? ') == 'n':
            return [None]
        while True:
            name = ask('Enter component name: ')
            version = ask('Enter component version: ')
            components.append({'name': name, 'version': version})
            if ask('Continue (y/n)? ') == 'n':
                break
        return components

    def get_components_php_composer_json_system_path(self, api_data):
        packages = self.load_php_composer_json_system_path(filename=api_data['file'])[0]
        if packages is None:
            print('Gemfile packages loading error.')
            return [None]
        components = self.parse_php_composer_json_system_path(_packages=packages)
        return components

    def get_components_php_composer_lock_system_path(self, api_data):
        packages = self.load_php_composer_lock_system_path(filename=api_data['file'])[0]
        if packages is None:
            print('Gemfile packages loading error.')
            return [None]
        components = self.parse_php_composer_lock_system_path(_packages=packages)
        return components

    # -------------------------------------------------------------------------
    # Loaders
    # -------------------------------------------------------------------------

    @staticmethod
    def load_windows_10_packages_from_shell():
        """
        Load OS packages for Windows platform by powershell command.
        :return: result
        """
        cmd = "Get-AppxPackage -AllUsers | Select Name, PackageFullName"
        try:
            proc = subprocess.Popen(["powershell", cmd], stdout=subprocess.PIPE)
            output, error = proc.communicate()
            if error:
                print_line('Powershell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                return [None]
            if output:
                return [output]
        except OSError as os_error:
            print_line('Powershell command throw errno: {0}, '
                       'strerror: {1} and '
                       'filename: {2}.'.format(os_error.errno, os_error.strerror, os_error.filename))
            return [None]
        except Exception as common_exception:
            print_line('Powershell command throw an exception: {0}.'.format(common_exception))
            return [None]

    def load_windows_10_packages_from_path(self, filename: str):
        """
        Get OS packages for Windows platform from unloaded file, that was created by shell command manually.
        :param filename: path to file
        :return: result
        """
        if os.path.exists(filename):
            enc = self.define_file_encoding(filename=filename)
            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return [None]
            try:
                with open(filename, 'r', encoding=enc) as cf:
                    os_packages = cf.read()
                    if os_packages is None:
                        print_line('Cant read file: {0}.'.format(filename))
                        return [None]
                    report = os_packages.replace('\r', '').split('\n')[9:]
                    return [report]
            except Exception as e:
                print_line('File read exception {0}.'.format(e))
                return [None]

        print_line('File {0} does not exists.'.format(filename))
        return [None]

    @staticmethod
    def load_ubuntu_packages_from_shell():
        """
        Load OS packages for Ubuntu platform by shell command.
        :return: result
        """
        cmd = "dpkg -l | grep '^ii '"
        try:
            if platform.system() == "Linux" or \
                    platform.system() == "linux" or \
                    platform.linux_distribution()[0] == 'debian':
                proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()
                if error:
                    print_line('Shell command throw {0} code and {error.strip()} error message.'.format(proc.returncode))
                    return [None]
                if output:
                    return [output]
            print_line('Platform not defined as Debian.')
            return [None]
        except OSError as os_error:
            print_line('Shell command throw errno: {0}, strerror: {1} and filename: {2}.'.format(os_error.errno, os_error.strerror, os_error.filename))
            return [None]
        except Exception as common_exception:
            print_line('Shell command throw an exception: {0}.'.format(common_exception))
            return [None]

    def load_ubuntu_packages_from_path(self, filename: str):
        """
        Load OS packages for Ubuntu platform from filem created by shell command.
        :return: result
        """
        if os.path.exists(filename):
            enc = self.define_file_encoding(filename=filename)
            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return [None]
            try:
                with open(filename, 'r', encoding=enc) as cf:
                    os_packages = cf.read()
                    if os_packages is None:
                        print_line('Cant read file: {0}.'.format(filename))
                        return [None]
                    return [os_packages]
            except Exception as e:
                print_line('File read exception {0}.'.format(e))
                return [None]
        print_line('File {0} does not exists.'.format(filename))
        return [None]

    @staticmethod
    def load_fedora_packages_from_shell():
        """
        Load OS packages for Fedora platform by shell command.
        :return: result
        """
        cmd = "rpm -qa"
        try:
            return [os.popen(cmd).readlines()]
        except OSError as os_error:
            print_line('Shell command throw errno: {0}, strerror: {1} and filename: {2}.'.format(os_error.errno, os_error.strerror, os_error.filename))
            return [None]
        except Exception as common_exception:
            print_line('Shell command throw an exception: {0}.'.format(common_exception))
            return [None]

    def load_fedora_packages_from_path(self, filename: str):
        """
        Load OS packages for Fedora platform from file, created by shell command.
        :return: result
        """
        if os.path.exists(filename):
            enc = self.define_file_encoding(filename=filename)
            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return [None]
            try:
                with open(filename, 'r', encoding=enc) as cf:
                    os_packages = cf.read()
                    if os_packages is None:
                        print_line('Cant read file: {0}.'.format(filename))
                        return [None]
                    return [os_packages]
            except Exception as e:
                print_line('File read exception {0}.'.format(e))
                return [None]
        print_line('File {0} does not exists.'.format(filename))
        return [None]

    @staticmethod
    def load_macos_packages_from_shell():
        """
        Load OS packages for MacOS platform by shell command.
        :return: result
        """
        cmd = "cat /Library/Receipts/InstallHistory.plist"
        try:
            if platform.system() == 'darwin' or platform.system() == 'Darwin':
                proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()
                if error:
                    print_line('Shell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                    return [None]
                if output:
                    return [output]
        except OSError as os_error:
            print_line('Shell command throw errno: {0}, strerror: {1} and filename: {2}.'.format(os_error.errno, os_error.strerror, os_error.filename))
            return [None]
        except Exception as common_exception:
            print_line('Shell command throw an exception: {0}.'.format(common_exception))
            return [None]

    def load_macos_packages_from_path(self, filename: str):
        """
        Load OS packages for MacOS platform from file, created by shell command.
        :return: result
        """
        if os.path.exists(filename):
            enc = self.define_file_encoding(filename=filename)
            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return [None]
            try:
                with open(filename, 'r', encoding=enc) as cf:
                    os_packages = cf.read()
                    if os_packages is None:
                        print_line('Cant read file: {0}.'.format(filename))
                        return [None]
                    return [os_packages]
            except Exception as e:
                print_line('File read exception {0}.'.format(e))
                return [None]
        print_line('File {0} does not exists.'.format(filename))
        return [None]

    @staticmethod
    def load_pip_packages_from_shell_legacy():
        """
        Load Python PI packages with pip.FrozenRequirement method.
        :return: result
        """
        cmd = "pip list --format=legacy"
        try:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output, error = proc.communicate()
            if error:
                print('Error')
                return [None]
            if output:
                if len(output) > 0:
                    return output.decode('utf-8')
                else:
                    return [None]
        except Exception as common_exception:
            print("An exception {0} occured while shell command was called.".format(common_exception))
            return [None]
        return [None]

    def load_pip_packages_from_path(self, filename: str):
        """
        Load Python PIP packages from file.
        :param filename: path to file
        :return: result
        """
        if os.path.exists(filename):
            enc = self.define_file_encoding(filename)
            if enc == 'undefined':
                print_line('Undefined file {0} encoding.'.format(filename))
                return [None]
            try:
                with open(filename, encoding=enc) as cf:
                    rfp = cf.read()
                    rfps = rfp.replace(' ', '').split('\n')
                    return rfps
            except Exception as e:
                print_line('Get an exception {0}, when read file {1}'.format(e, filename))
                return [None]

        print_line('File {0} does not exists.'.format(filename))
        return [None]

    def load_npm_packages_from_path(self, filename: str):
        """
        Load NPM packages from file, defined by path.
        :param filename: path to file
        :return: result
        """
        if os.path.exists(filename):
            enc = self.define_file_encoding(filename)
            if enc == 'undefined':
                print_line('Undefined file {0} encoding.'.format(filename))
                return [None]
            try:
                with open(filename, 'r', encoding=enc) as pf:
                    data = json.load(pf)
                    walkdict(data)
                    return [True]
            except Exception as e:
                print_line('File read exception: {0}'.format(e))
                return [None]
        print_line('File {0} does not exist.'.format(filename))
        return [None]

    def load_npm_packages(self, api_data, local: bool):
        """
        Load NPM packages from shell command through temporary file.
        :param path: path to directory, if method call locally
        :param local: run local or global
        :return: result
        """
        path = api_data['file']
        tmp_file_name = 'tmp_npm_list_json.txt'
        file_path = os.path.expanduser('~')
        full_path = os.path.join(file_path, tmp_file_name)
        try:
            with open(full_path, mode='w', encoding='utf-8') as temp:
                temp.write('')
                temp.seek(0)
        except Exception as e:
            print_line('Cant create temp file, get an exception: {0}.'.format(e))
            return [None]
        cmd = "npm list --json > {0}".format(full_path)
        if local:
            os.chdir(path)
        else:
            if api_data['os_type'] == OSs.WINDOWS:
                os.chdir("c:\\")
            else:
                os.chdir("/")
        output = error = None
        try:
            if api_data['os_type'] == OSs.WINDOWS:
                proc = subprocess.Popen(["powershell", cmd], stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()
                if error:
                    print_line('Powershell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                    return [None]
                return output
            elif api_data['os_type'] == OSs.MACOS:
                proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()
                if error:
                    print_line('Shell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                    return [None]
            elif api_data['os_type'] == OSs.UBUNTU:
                proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()
                if error:
                    print_line('Shell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                    return [None]
            elif api_data['os_type'] == OSs.DEBIAN:
                proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()
                if error:
                    print_line('Shell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                    return [None]
            elif api_data['os_type'] == OSs.FEDORA:
                proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()
                if error:
                    print_line('Shell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                    return [None]

            try:
                enc = self.define_file_encoding(full_path)
                if enc == 'undefined':
                    print_line('An error with encoding occured in temp file.')
                    return [None]
                with open(full_path, encoding=enc) as cf:
                    data = json.load(cf)
                    walkdict(data)
                    return [True]
            except Exception as e:
                print_line('File read exception: {0}'.format(e))
                return [None]
            finally:
                if os.path.isfile(full_path):
                    os.remove(full_path)
        except OSError as os_error:
            print_line('Shell command throw errno: {0}, strerror: {1} and filename: {2}.'.format(os_error.errno, os_error.strerror, os_error.filename))
            if os.path.isfile(full_path):
                os.remove(full_path)
            return [None]
        finally:
            if os.path.isfile(full_path):
                os.remove(full_path)

    def load_package_json_packages_from_path(self, filename):
        """
        Load NPM packages from package.json file, defined by path.
        :param filename: path to file
        :return: result
        """
        if os.path.exists(filename):
            enc = self.define_file_encoding(filename)
            if enc == 'undefined':
                print_line('Undefined file {0} encoding.'.format(filename))
                return [None]
            try:
                with open(filename, 'r', encoding=enc) as pf:
                    packages = json.load(pf)
                    return [packages]
            except Exception as e:
                print_line('File {0} read exception: {1}'.format(filename, e))
                return [None]
        print_line('File does not exist.')
        return [None]

    def load_npm_lock_packages_from_path(self, filename):
        """
        Load NPM packages from lock file, defined by path.
        :param filename: path to file
        :return: result
        """
        if os.path.exists(filename):
            enc = self.define_file_encoding(filename)
            if enc == 'undefined':
                print_line('Undefined file {0} encoding.'.format(filename))
                return [None]
            try:
                with open(filename, 'r', encoding=enc) as pf:
                    try:
                        packages = json.load(pf)
                        return [packages]
                    except json.JSONDecodeError as json_decode_error:
                        print_line('An exception occured with json decoder: {0}.'.format(json_decode_error))
                        return [None]
            except Exception as e:
                print_line('File {0} read exception: {1}'.format(filename, e))
                return [None]
        print_line('File does not exist.')
        return [None]

    def load_gem_packages_from_path(self, filename):
        """
        Load Ruby gem packages from file, defined by path.
        :param filename: path to file
        :return: result
        """
        if os.path.exists(filename):
            enc = self.define_file_encoding(filename)
            if enc == 'undefined':
                print_line('Undefined file {0} encoding.'.format(filename))
                return [None]
            try:
                with open(filename, 'r', encoding=enc) as pf:
                    cont = pf.read().replace('default: ', '').replace(' ', '').replace(')', '')
                    cont = cont.split('\n')
                    return [cont]
            except Exception as e:
                print_line('File {0} read exception: {1}'.format(filename, e))
                return [None]
        print_line('File does not exist.')
        return [None]

    @staticmethod
    def load_gem_packages_system(local, api_data):
        """
        Load Ruby gem packages from global or local call of shell commend.
        :param local: local or global
        :param api_data: api data set
        :return: result
        """
        if local:
            os.chdir(api_data['file'])
        else:
            if api_data['os_type'] == OSs.WINDOWS:
                os.chdir("c:\\")
            else:
                os.chdir("/")
        cmd = "gem list"
        output = error = None
        try:
            if api_data['os_type'] == OSs.WINDOWS:
                proc = subprocess.Popen(["powershell", cmd], stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()
                output = output.decode('utf-8').replace('\r', '').split('\n')
                if error:
                    print_line('Powershell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                    return [None]
                if output:
                    return [output]
                return [None]
            elif api_data['os_type'] == OSs.CENTOS:
                proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()
                output = output.decode('utf-8').replace('\r', '').split('\n')
                if error:
                    print_line('Shell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                    return [None]
                if output:
                    return [output]
                return [None]
            elif api_data['os_type'] == OSs.DEBIAN:
                proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()
                output = output.decode('utf-8').replace('\r', '').split('\n')
                if error:
                    print_line('Shell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                    return [None]
                if output:
                    return [output]
                return [None]
            elif api_data['os_type'] == OSs.UBUNTU:
                proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()
                output = output.decode('utf-8').replace('\r', '').split('\n')
                if error:
                    print_line('Shell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                    return [None]
                if output:
                    return [output]
                return [None]
            elif api_data['os_type'] == OSs.FEDORA:
                proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()
                output = output.decode('utf-8').replace('\r', '').split('\n')
                if error:
                    print_line('Shell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                    return [None]
                if output:
                    return [output]
                return [None]
            elif api_data['os_type'] == OSs.MACOS:
                proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()
                output = output.decode('utf-8').replace('\r', '').split('\n')
                if error:
                    print_line('Shell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                    return [None]
                if output:
                    return [output]
                return [None]
        except OSError as os_error:
            print_line('Shell command throw errno: {0}, strerror: {1} and filename: {2}.'.format(os_error.errno, os_error.strerror, os_error.filename))
            return [None]
        except Exception as common_exception:
            print_line('Shell command throw an exception: {0}.'.format(common_exception))
            return [None]

    def load_gemfile_packages_from_path(self, filename):
        """
        Load packages from Gemfile. defined by path.
        :param filename: filename
        :return: result
        """
        if os.path.isfile(filename):
            enc = self.define_file_encoding(filename=filename)
            if enc == 'undefined':
                print_line('Undefined file {0} encoding.'.format(filename))
                return [None]
            try:
                with open(filename, 'r', encoding=enc) as pf:
                    cont = pf.read()
                    packages = cont.split('\n')
                    return packages
            except Exception as e:
                print_line('File {0} read exception: {1}'.format(filename, e))
                return [None]
        print_line('File does not exist.')
        return [None]

    def load_gemfile_lock_packages_from_path(self, filename):
        """
        Load packages from Gemfile.lock defined by path.
        :param filename: filename
        :return: result
        """
        if os.path.isfile(filename):
            enc = self.define_file_encoding(filename=filename)
            if enc == 'undefined':
                print_line('Undefined file {0} encoding.'.format(filename))
                return [None]
            try:
                with open(filename, 'r', encoding=enc) as pf:
                    cont = pf.read()
                    packages = cont.split('\n')
                    return packages
            except Exception as e:
                print_line('File {0} read exception: {1}'.format(filename, e))
                return [None]
        print_line('File does not exist.')
        return [None]

    def load_php_composer_json_system_path(self, filename):
        if os.path.isfile(filename):
            enc = self.define_file_encoding(filename=filename)
            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return [None]
            with open(filename, 'r', encoding=enc) as pf:
                try:
                    packages = json.load(pf)
                    return [packages]
                except json.JSONDecodeError as json_decode_error:
                    print_line('An exception occured with json decoder: {0}.'.format(json_decode_error))
                    return [None]
        print_line('File {0} not found.'.format(filename))
        return [None]

    def load_php_composer_lock_system_path(self, filename):
        if os.path.isfile(filename):
            enc = self.define_file_encoding(filename=filename)
            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return [None]
            with open(filename, 'r', encoding=enc) as pf:
                try:
                    packages = json.load(pf)
                    return [packages]
                except json.JSONDecodeError as json_decode_error:
                    print_line('An exception occured with json decoder: {0}.'.format(json_decode_error))
                    return [None]
        print_line('File {0} not found.'.format(filename))
        return [None]

    # -------------------------------------------------------------------------
    # Parsers
    # -------------------------------------------------------------------------

    @staticmethod
    def parse_windows_10_packages(report):
        """
        Parse Windows 10 packages.
        :param report: raw report
        :return: result
        """
        packages = []
        try:
            for report_element in report:
                if len(report_element) > 0:
                    splitted_report_element = report_element.split()
                    component_and_version = splitted_report_element[len(splitted_report_element) - 1]
                    element_array = component_and_version.split('_')
                    if len(element_array) >= 2:
                        common_component_name = element_array[0]
                        common_component_version = element_array[1]
                        component = {'name': common_component_name.split('.')}
                        if len(common_component_name.split('.')) >= 3 and component['name'][1] == 'NET':
                            component['name'] = 'net_framework'
                        else:
                            component['name'] = common_component_name.split('.')
                            component['name'] = component['name'][len(component['name']) - 1]
                        component['version'] = common_component_version.split('.')
                        component['version'] = component['version'][0] + '.' + component['version'][1]
                        packages.append(component)
            return packages
        except Exception as common_exception:
            print_line('Exception {0} occured.'.format(common_exception))
            return [None]

    @staticmethod
    def parse_ubuntu_packages(_report):
        """
        Parse Ubuntu package list.
        :param _report: raw packages.
        :return: result
        """
        number_of_line_breaks = _report.split('\n')
        new_components = []
        pattern1 = "(\d+[.]\d+[.]?\d*)"
        pattern = re.compile(pattern1)
        for line in number_of_line_breaks:
            l = re.sub(r'\s+', ' ', line)
            l2 = l.split()
            if len(l2) > 2:
                start = l2[0]
                name = l2[1]
                raw_version = l2[2]
                if start == 'ii' or start == 'rc':
                    if pattern.match(raw_version):
                        m = re.search(pattern1, raw_version)
                        ver = m.group()
                        if ':' in name:
                            name = name[:name.index(':')]
                        new_components.append({"name": name, "version": ver})
        return new_components

    @staticmethod
    def parse_fedora_packages(_report):
        """
        Parse Fedora package list.
        :param _report: raw packages.
        :return: result
        """
        new_components = []
        number_of_line_breaks = _report
        for line in number_of_line_breaks:
            line = line.replace('\n', '')
            pattern = '\s*\-\s*'
            component_array = re.split(pattern, line)
            if len(component_array) >= 2:
                name = component_array[0]
                version = component_array[1]
                new_components.append({'name': name, 'version': version})
        return new_components

    @staticmethod
    def parse_macos_packages(_report):
        """
        Parse MacOS packages.
        :param _report: raw packages
        :return: result
        """
        new_components = []
        packages = xmltodict.parse(_report, xml_attribs=True)
        pdict = packages['plist']['array']['dict']
        for pd in pdict:
            name = pd['string'][0]
            version = pd['string'][1]
            if version is not None:
                new_components.append({'name': name, 'version': version})
        return new_components

    @staticmethod
    def parse_pip_packages_legacy(packages):
        packages = packages.replace(')', '')
        packages = packages.replace(' ', '')
        packages = packages.split('\r\n')
        components = []
        for package in packages:
            if len(package) <= 3:
                continue
            line = package.split('(')
            name = line[0]
            version = line[1]
            components.append({'name': name, 'version': version})
        return components

    @staticmethod
    def parse_pip_packages_from_path(packages):
        """
        Parse Python PIP packages report.
        :param packages: raw packages
        :return: result
        """
        components = []
        for ref in packages:
            if len(ref) > 0:
                if '==' in ref:
                    refs = ref.split('==')
                    components.append({'name': refs[0], 'version': refs[1]})
                elif '>' in ref:
                    refs = ref.split('>')
                    components.append({'name': refs[0], 'version': refs[1]})
                elif '<' in ref:
                    refs = ref.split('<')
                    components.append({'name': refs[0], 'version': refs[1]})
                elif '>=' in ref:
                    refs = ref.split('>=')
                    components.append({'name': refs[0], 'version': refs[1]})
                elif '<=' in ref:
                    refs = ref.split('<-')
                    components.append({'name': refs[0], 'version': refs[1]})
                else:
                    try:
                        mm = importlib.import_module(ref)
                        components.append({'name': ref, 'version': mm.__version__})
                    except ImportError as import_exception:
                        print_line('Get an exception {0} when define component version.'.format(import_exception))
                        components.append({'name': ref, 'version': '*'})
                        continue
        return components

    @staticmethod
    def parse_npm_packages(api_data, comp):
        """
        Parse NPM raw packages.
        :param api_data: api data set
        :param comp: raw packages.
        :return: result
        """
        components2 = []
        for c in comp:
            if c["name"] == "from":
                if '@' in c['version']:
                    p = c["version"].split('@')
                    p[1] = p[1].replace('~', '')
                    components2.append({"name": p[0], "version": p[1]})
                else:
                    name = c["version"]
                    cmd = "npm view {0} version".format(name)
                    try:
                        if api_data['os_type'] == OSs.WINDOWS:
                            proc = subprocess.Popen(["powershell", cmd], stdout=subprocess.PIPE)
                            version, error = proc.communicate()
                            version = version.decode("utf-8").replace('\n', '')
                            if error:
                                print_line('Shell command throw {0} code and {1} error message.'
                                           .format(proc.returncode, error.strip()))
                            else:
                                components2.append({"name": name, "version": version})
                        elif api_data['os_type'] == OSs.MACOS:
                            proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                            version, error = proc.communicate()
                            version = version.decode("utf-8").replace('\n', '')
                            if error:
                                print_line('Shell command throw {0} code and {1} error message.'
                                           .format(proc.returncode, error.strip()))
                            else:
                                components2.append({"name": name, "version": version})
                        elif api_data['os_type'] == OSs.DEBIAN:
                            proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                            version, error = proc.communicate()
                            version = version.decode("utf-8").replace('\n', '')
                            if error:
                                print_line('Shell command throw {0} code and {1} error message.'
                                           .format(proc.returncode, error.strip()))
                            else:
                                components2.append({"name": name, "version": version})
                        elif api_data['os_type'] == OSs.UBUNTU:
                            proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                            version, error = proc.communicate()
                            version = version.decode("utf-8").replace('\n', '')
                            if error:
                                print_line('Shell command throw {0} code and {1} error message.'
                                           .format(proc.returncode, error.strip()))
                            else:
                                components2.append({"name": name, "version": version})
                        elif api_data['os_type'] == OSs.FEDORA:
                            proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                            version, error = proc.communicate()
                            version = version.decode("utf-8").replace('\n', '')
                            if error:
                                print_line('Shell command throw {0} code and {1} error message.'
                                           .format(proc.returncode, error.strip()))
                            else:
                                components2.append({"name": name, "version": version})
                        elif api_data['os_type'] == OSs.CENTOS:
                            proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                            version, error = proc.communicate()
                            version = version.decode("utf-8").replace('\n', '')
                            if error:
                                print_line('Shell command throw {0} code and {1} error message.'
                                           .format(proc.returncode, error.strip()))
                            else:
                                components2.append({"name": name, "version": version})
                    except OSError as os_error:
                        print_line('Shell command throw errno: {0}, strerror: {1}.'
                                   .format(os_error.errno, os_error.strerror))
                        print_line('and filename: {0}.'.format(os_error.filename))
                        continue
                    except:
                        continue
        return components2

    @staticmethod
    def parse_npm_lock_packages(packages):
        """
        Parse NPM lock packages.
        :param packages: raw packages.
        :return: result
        """
        def already_in_components(components, key: str) -> bool:
            """
            Filter if component already in list.
            :param components: component list
            :param key: component key
            :return: filtered list
            """
            for component in components:
                if component['name'] == key:
                    return True
            return False

        dependencies = packages['dependencies']
        keys = dependencies.keys()
        components = []
        for key in keys:
            if not already_in_components(components=components, key=key):
                components.append({'name': key, "version": dependencies[key]['version']})
            if 'requires' in dependencies[key].keys():
                requires = dependencies[key]['requires']
                for rkey in requires.keys():
                    if not already_in_components(components=components, key=rkey):
                        components.append({'name': rkey, 'version': requires[rkey]})
            if 'dependencies' in dependencies[key].keys():
                deps = dependencies[key]['dependencies']
                for dkey in deps.keys():
                    if not already_in_components(components=components, key=dkey):
                        components.append({'name': dkey, 'version': deps[dkey]})
        return components

    @staticmethod
    def parse_package_json_packages_from_path(packages):
        """
        Parse package.json file.
        :param packages: raw packages
        :return: result
        """
        components = []
        dependencies = packages['dependencies']
        dev_dependencies = packages['devDependencies']
        if dev_dependencies != {}:
            for key in dev_dependencies.keys():
                components.append({'name': key, 'version': str(dev_dependencies[key]).replace('^', '')})
        if dependencies != {}:
            for key in dependencies.keys():
                components.append({'name': key, 'version': str(dependencies[key]).replace('^', '')})
        return components

    def parse_gem_packages_system(self, packages):
        """
        Parse Ruby gem packages.
        :param packages: raw packages.
        :return: result
        """
        return self.parse_gem_packages_from_path(packages=packages)

    @staticmethod
    def parse_gem_packages_from_path(packages):
        """
        Parse Ruby gem packages from path.
        :param packages: raw packages
        :return: result
        """
        components = []
        for c in packages:
            if len(c) > 0:
                c = c.replace(' ', '').replace(')', '').replace('default:', '')
                cs = c.split('(')
                try:
                    if len(cs) == 2:
                        components.append({'name': cs[0], 'version': cs[1]})
                except:
                    continue
        return components

    def parse_gemfile_packages(self, packages):
        """
        Parse packages from Gemfile.
        :param packages: list of packages
        :return: result
        """
        content_splitted_by_strings = packages
        content_without_empty_strings = []
        for string in content_splitted_by_strings:
            if len(string) > 0:
                content_without_empty_strings.append(string)
        content_without_comments = []
        for string in content_without_empty_strings:
            if not string.lstrip().startswith('#'):
                if '#' in string:
                    content_without_comments.append(string.lstrip().split('#')[0])
                else:
                    content_without_comments.append(string.lstrip())
        cleared_content = []
        for string in content_without_comments:
            if string.startswith('gem '):
                cleared_content.append(string.split('gem ')[1])
            elif string.startswith("gem('"):
                cleared_content.append(string.split("gem('")[1][:-1])
        prepared_data_for_getting_packages_names_and_versions = []
        for string in cleared_content:
            intermediate_result = re.findall(
                r'''('.*',\s*'.*\d.*?'|".*",\s*".*\d.*?"|".*",\s*'.*\d.*?'|'.*',\s*".*\d.*?"|.*',\s*'.*\d.*?')''', string)
            if intermediate_result:
                prepared_data_for_getting_packages_names_and_versions.append(intermediate_result[0])
        packages = []
        for prepared_string in prepared_data_for_getting_packages_names_and_versions:
            package = {
                'name': '*',
                'version': '*'
            }
            splitted_string_by_comma = prepared_string.split(',')
            package_name = splitted_string_by_comma[0][1:-1]
            package['name'] = package_name
            if len(splitted_string_by_comma) == 2:
                package['version'] = re.findall(r'(\d.*)', splitted_string_by_comma[1])[0][0:-1]
                packages.append(package)
            elif len(splitted_string_by_comma) == 3:
                min_package_version = re.findall(r'(\d.*)', splitted_string_by_comma[1])[0][0:-1]
                package['version'] = min_package_version
                packages.append(package)
                package = {
                    'name': '*',
                    'version': '*'
                }
                max_package_version = re.findall(r'(\d.*)', splitted_string_by_comma[2])[0][0:-1]
                package['name'] = package_name
                package['version'] = max_package_version
                packages.append(package)
        formed_packages = []
        buff_packages = []
        for package in packages:
            buff_package = {
                'name': '*',
                'version': '*',
                'origin_version': '*'
            }
            splitted_packages_by_dot = package['version'].split('.')
            if len(splitted_packages_by_dot) == 1:
                buff_package['name'] = package['name']
                buff_package['origin_version'] = package['version']
                package['version'] = '{}.0.0'.format(splitted_packages_by_dot[0])
                formed_packages.append(package)
                buff_package['version'] = package['version']
                buff_packages.append(buff_package)
            elif len(splitted_packages_by_dot) == 2:
                buff_package['name'] = package['name']
                buff_package['origin_version'] = package['version']
                package['version'] = '{}.{}.0'.format(splitted_packages_by_dot[0], splitted_packages_by_dot[1])
                formed_packages.append(package)
                buff_package['version'] = package['version']
                buff_packages.append(buff_package)
            else:
                formed_packages.append(package)
        unique_packages = []
        for i in range(len(formed_packages)):
            package = formed_packages.pop()
            if package not in unique_packages:
                unique_packages.append(package)
        for package in unique_packages:
            for buff_package in buff_packages:
                if package['name'] == buff_package['name'] and package['version'] == buff_package['version']:
                    package['version'] = buff_package['origin_version']
        return unique_packages

    @staticmethod
    def parse_gemfile_lock_packages(packages):
        """
        Parse packages from Gemfile
        :param packages: list of packages
        :return: result
        """
        splitted_content_by_strings = packages
        ignore_strings_startswith = (
            'GIT', 'remote', 'revision',
            'specs', 'PATH', 'GEM',
            'PLATFORMS', 'DEPENDENCIES', 'BUNDLED')
        cleared_content = []
        for string in splitted_content_by_strings:
            if not string.lstrip().startswith(ignore_strings_startswith):
                cleared_content.append(string.lstrip())
        prepared_data_for_getting_packages_names_and_versions = []
        for string in cleared_content:
            intermediate_result = re.findall(r'(.*\s*\(.*\))', string)
            if intermediate_result:
                prepared_data_for_getting_packages_names_and_versions.append(intermediate_result)
        packages = []
        for data in prepared_data_for_getting_packages_names_and_versions:
            package = {
                'name': '*',
                'version': '*'
            }
            splitted_data = data[0].split(' ')
            package_name = splitted_data[0]
            package['name'] = package_name
            if len(splitted_data) == 2:
                package['version'] = splitted_data[1][1:-1]
                packages.append(package)
            elif len(splitted_data) == 3:
                package['version'] = splitted_data[2][0:-1]
                packages.append(package)
            elif len(splitted_data) == 5:
                min_version = splitted_data[2][0:-1]
                package['version'] = min_version
                packages.append(package)
                package = {
                    'name': '*',
                    'version': '*'
                }
                max_version = splitted_data[4][0:-1]
                package['name'] = package_name
                package['version'] = max_version
                packages.append(package)
        formed_packages = []
        buff_packages = []
        for package in packages:
            buff_package = {
                'name': '*',
                'version': '*',
                'origin_version': '*'
            }
            splitted_packages_by_dot = package['version'].split('.')
            if len(splitted_packages_by_dot) == 1:
                buff_package['name'] = package['name']
                buff_package['origin_version'] = package['version']
                package['version'] = '{}.0.0'.format(splitted_packages_by_dot[0])
                formed_packages.append(package)
                buff_package['version'] = package['version']
                buff_packages.append(buff_package)
            elif len(splitted_packages_by_dot) == 2:
                buff_package['name'] = package['name']
                buff_package['origin_version'] = package['version']
                package['version'] = '{}.{}.0'.format(splitted_packages_by_dot[0], splitted_packages_by_dot[1])
                formed_packages.append(package)
                buff_package['version'] = package['version']
                buff_packages.append(buff_package)
            else:
                formed_packages.append(package)
        unique_packages = []
        for i in range(len(formed_packages)):
            package = formed_packages.pop()
            if package not in unique_packages:
                unique_packages.append(package)
        for package in unique_packages:
            for buff_package in buff_packages:
                if package['name'] == buff_package['name'] and package['version'] == buff_package['version']:
                    package['version'] = buff_package['origin_version']
        return unique_packages

    @staticmethod
    def parse_php_composer_json_system_path(_packages):
        content = _packages
        packages = []
        for key in content:
            if key == 'require' or key == 'require-dev':
                for inner_key, value in content[key].items():
                    if '/' in inner_key:
                        package_name = inner_key.split('/')[1]
                    else:
                        package_name = inner_key

                    if '||' in value:
                        splitted_values = value.split('||')
                    elif '|' in value:
                        splitted_values = value.split('|')
                    else:
                        splitted_values = value.split(',')

                    for splitted_value in splitted_values:
                        package = {
                            'name': '*',
                            'version': '*'
                        }

                        version = re.findall(r'(\d.*)', splitted_value)

                        if version:
                            package['name'] = package_name
                            package['version'] = version[0].lstrip().rstrip()
                            packages.append(package)

        formed_packages = []
        buff_packages = []
        for package in packages:
            buff_package = {
                'name': '*',
                'version': '*',
                'origin_version': '*'
            }

            splitted_packages_by_dot = package['version'].split('.')

            if len(splitted_packages_by_dot) == 1:
                buff_package['name'] = package['name']
                buff_package['origin_version'] = package['version']

                package['version'] = '{}.0.0'.format(splitted_packages_by_dot[0])
                formed_packages.append(package)

                buff_package['version'] = package['version']
                buff_packages.append(buff_package)
            elif len(splitted_packages_by_dot) == 2:
                buff_package['name'] = package['name']
                buff_package['origin_version'] = package['version']

                package['version'] = '{}.{}.0'.format(splitted_packages_by_dot[0], splitted_packages_by_dot[1])
                formed_packages.append(package)

                buff_package['version'] = package['version']
                buff_packages.append(buff_package)
            else:
                formed_packages.append(package)

        unique_packages = []
        for i in range(len(formed_packages)):
            package = formed_packages.pop()

            if package not in unique_packages:
                unique_packages.append(package)

        for package in unique_packages:
            for buff_package in buff_packages:
                if package['name'] == buff_package['name'] and package['version'] == buff_package['version']:
                    package['version'] = buff_package['origin_version']

        return unique_packages

    @staticmethod
    def parse_php_composer_lock_system_path(_packages):
        """
        Parse packages from PHP Composer.lock file.
        :param _packages: list of packages
        :return: result
        """
        content = _packages
        packages = []
        for key in content:
            if key == 'packages' or key == 'packages-dev':
                key_packages = content[key]

                for k_package in key_packages:
                    if 'require' in k_package:
                        for inner_key, value in k_package['require'].items():
                            if '/' in inner_key:
                                package_name = inner_key.split('/')[1]
                            else:
                                package_name = inner_key

                            if '||' in value:
                                splitted_values = value.split('||')
                            elif '|' in value:
                                splitted_values = value.split('|')
                            else:
                                splitted_values = value.split(',')

                            for splitted_value in splitted_values:
                                package = {
                                    'name': '*',
                                    'version': '*'
                                }

                                version = re.findall(r'(\d.*)', splitted_value)

                                if version:
                                    package['name'] = package_name
                                    package['version'] = version[0].lstrip().rstrip()
                                    packages.append(package)

                    if 'require-dev' in k_package:
                        for inner_key, value in k_package['require-dev'].items():
                            if '/' in inner_key:
                                package_name = inner_key.split('/')[1]
                            else:
                                package_name = inner_key

                            if '||' in value:
                                splitted_values = value.split('||')
                            elif '|' in value:
                                splitted_values = value.split('|')
                            else:
                                splitted_values = value.split(',')

                            for splitted_value in splitted_values:
                                package = {
                                    'name': '*',
                                    'version': '*'
                                }

                                version = re.findall(r'(\d.*)', splitted_value)

                                if version:
                                    package['name'] = package_name
                                    package['version'] = version[0].lstrip().rstrip()
                                    packages.append(package)

        formed_packages = []
        buff_packages = []
        for package in packages:
            buff_package = {
                'name': '*',
                'version': '*',
                'origin_version': '*'
            }

            splitted_packages_by_dot = package['version'].split('.')

            if len(splitted_packages_by_dot) == 1:
                buff_package['name'] = package['name']
                buff_package['origin_version'] = package['version']

                package['version'] = '{}.0.0'.format(splitted_packages_by_dot[0])
                formed_packages.append(package)

                buff_package['version'] = package['version']
                buff_packages.append(buff_package)
            elif len(splitted_packages_by_dot) == 2:
                buff_package['name'] = package['name']
                buff_package['origin_version'] = package['version']

                package['version'] = '{}.{}.0'.format(splitted_packages_by_dot[0], splitted_packages_by_dot[1])
                formed_packages.append(package)

                buff_package['version'] = package['version']
                buff_packages.append(buff_package)
            else:
                formed_packages.append(package)

        unique_packages = []
        for i in range(len(formed_packages)):
            package = formed_packages.pop()

            if package not in unique_packages:
                unique_packages.append(package)

        for package in unique_packages:
            for buff_package in buff_packages:
                if package['name'] == buff_package['name'] and package['version'] == buff_package['version']:
                    package['version'] = buff_package['origin_version']

        return unique_packages

    # -------------------------------------------------------------------------
    # Addition methods
    # -------------------------------------------------------------------------

    @staticmethod
    def define_file_encoding(filename):
        """
        Define encoding of file.
        :param filename:
        :return:
        """
        encodings = ['utf-16', 'utf-8', 'windows-1250', 'windows-1252', 'iso-8859-7', 'macgreek']
        for e in encodings:
            try:
                import codecs
                fh = codecs.open(filename, 'r', encoding=e)
                fh.readlines()
                fh.seek(0)
                return e
            except:
                continue
        return 'undefined'

    def get_current_set_name(self, api_data):
        """
        Get current component set name.
        :param api_data: api data set
        :return: result
        """
        if api_data['organization'] is None:
            return [None]
        if api_data['organization']['platforms'] is None:
            return [None]
        platform_number = self.web_api.get_platform_number_by_name(api_data=api_data)
        if platform_number == -1:
            return [None]
        project_number = self.web_api.get_project_number_by_name(api_data=api_data)
        if project_number == -1:
            return ['0.0.1']
        return [api_data['organization']['platforms'][platform_number]['projects'][project_number]['current_component_set']['name']]

    def get_current_component_set(self, api_data):
        """
        Get current component set for platform/project.
        :param api_data: api data set
        :return: result
        """
        if api_data['organization'] is None:
            return [None]
        if api_data['organization']['platforms'] is None:
            return [None]
        platform_number = self.web_api.get_platform_number_by_name(api_data=api_data)
        if platform_number == -1:
            return [None]
        project_number = self.web_api.get_project_number_by_name(api_data=api_data)
        if project_number == -1:
            return [None]
        return [api_data['organization']['platforms'][platform_number]['projects'][project_number]['current_component_set']]


class OSs(object):
    """Class for OS constant names.
    """

    WINDOWS = 'windows'
    UBUNTU = 'ubuntu'
    DEBIAN = 'debian'
    CENTOS = 'centos'
    FEDORA = 'fedora'
    OPENSUSE = 'opensuse'
    MACOS = 'macos'