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
        # type: (dict) -> bool
        """
        Get components of OS by calling of shell script and than parse them.
        :param api_data: api data set
        :return: result
        """
        if api_data['os_type'] == OSs.WINDOWS:

            if api_data['os_version'] == '10' or api_data['os_version'] == '8':
                if self.load_windows_10_packages_from_shell(api_data=api_data):
                    try:
                        print(len(api_data['packages']))
                        print(type(api_data['packages']))
                        api_data['packages'] = api_data['packages'].decode('utf-8').replace('\r', '').split('\n')[9:]
                    except UnicodeDecodeError as decode_error:
                        try:
                            api_data['packages'] = api_data['packages'].replace('\r', '').split('\n')[9:]
                        except TypeError as type_error:
                            api_data['packages'] = api_data['packages'].decode("utf-8", "backslashreplace").replace('\r', '').split('\n')[9:]
                            print(len(api_data['packages']))
                    if self.parse_windows_10_packages(api_data=api_data):
                        print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                        return True

                print_line('Failed to load or parse OS components.')
                return False

            elif api_data['os_version'] == '7':
                print_line('Windows 7 does not support yet.')
                return False

            else:
                print_line('Windows type not defined.')
                return False

        elif api_data['os_type'] == OSs.MACOS:

            if self.load_macos_packages_from_shell(api_data=api_data):
                if self.parse_macos_packages(api_data=api_data):
                    print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                    return True

            print_line('Failed load or parse MACOS components.')
            return False

        elif api_data['os_type'] == OSs.CENTOS:
            print_line('CentOS not support yet.')
            return False

        elif api_data['os_type'] == OSs.DEBIAN:
            if self.load_ubuntu_packages_from_shell(api_data=api_data):
                if self.parse_ubuntu_packages(api_data=api_data):
                    print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                    return True

            print_line('Failed load or parse OS components.')
            return False

        elif api_data['os_type'] == OSs.UBUNTU:
            if self.load_ubuntu_packages_from_shell(api_data=api_data):
                if self.parse_ubuntu_packages(api_data=api_data):
                    print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                    return True

            print_line('Failed load or parse OS components.')
            return False

        elif api_data['os_type'] == OSs.FEDORA:
            if self.load_fedora_packages_from_shell(api_data=api_data):
                if self.parse_fedora_packages(api_data=api_data):
                    print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                    return True

            print_line('Failed parse OS components.')
            return False
        return False

    def get_components_os_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Get OS packages from file, defined by path, which were created by calling the shell command.
        :param api_data: api data set
        :return: result
        """
        if api_data['os_type'] == OSs.WINDOWS:
            if api_data['os_version'] == '10' or api_data['os_version'] == '8':
                if self.load_windows_10_packages_from_path(api_data=api_data):
                    if self.parse_windows_10_packages(api_data=api_data):
                        print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                        return True

                print_line('Failed load or parse Windows 10 components.')
                return False

            if api_data['os_version'] == '7':
                print_line('Windows 7 does not support yet.')
                return False

        elif api_data['os_type'] == OSs.MACOS:
            if self.load_macos_packages_from_path(api_data=api_data):
                if self.parse_macos_packages(api_data=api_data):
                    print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                    return True

            print_line('Failed load or parse MACOS components.')
            return False

        elif api_data['os_type'] == OSs.CENTOS:
            print_line('CentOS does not support yet.')
            return False

        elif api_data['os_type'] == OSs.DEBIAN or api_data['os_type'] == OSs.UBUNTU:
            if self.load_ubuntu_packages_from_path(api_data=api_data):
                if self.parse_ubuntu_packages(api_data=api_data):
                    print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                    return True

            print_line('Failed load or parse Debian OS components.')
            return False

        elif api_data['os_type'] == OSs.FEDORA:
            if self.load_fedora_packages_from_path(api_data=api_data):
                if self.parse_fedora_packages(api_data=api_data):
                    print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                    return True

            print_line('Failed parse Fedora OS components.')
            return False

        else:
            return False

    def get_components_pip_auto_system_none(self, api_data):
        # type: (dict) -> bool
        """
        Get Python PIP components, collected by pip frozen requirements call.
        :return: result
        """
        if self.load_pip_packages_from_shell_legacy(api_data=api_data):
            if self.parse_pip_packages_legacy(api_data=api_data):
                print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                return True

        print_line('Problems with PIP components loading.')
        return False

    def get_components_pip_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Get Python PIP components from file, defined by path.
        :param api_data: api data set
        :return: result
        """
        if self.load_pip_packages_from_path(api_data=api_data):
            if self.parse_pip_packages_from_path(api_data=api_data):
                print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                return True

        print_line('Something wrong with packages in file path {0}.'.format(api_data['file']))
        return False

    def get_components_requirements_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Get Python PIP components from requirements.txt file, defined by path.
        :param api_data: api data set
        :return: result
        """
        if self.load_pip_packages_from_path(api_data=api_data):
            if self.parse_pip_packages_from_path(api_data=api_data):
                print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                return True

        print_line('Something wrong with packages in file path {0}.'.format(api_data['file']))
        return False

    def get_components_npm_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Get NPM packages, collected from file, defined by path.
        :param api_data:
        :return:
        """
        if self.load_npm_packages_from_path(api_data=api_data):
            api_data['packages'] = raw_npm_components
            if self.parse_npm_packages(api_data=api_data):
                print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                return True

        print_line('Something wrong with packages in file path {0}.'.format(api_data['file']))
        return False

    def get_components_package_json_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Get NPM packages from package.json file, defined by path.
        :param api_data: api data set
        :return: result
        """
        if self.load_package_json_packages_from_path(api_data=api_data):
            if self.parse_package_json_packages_from_path(api_data=api_data):
                print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                return True

        print_line('Something wrong with packages in file path {0}.'.format(api_data['file']))
        return False

    def get_components_gem_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Get Ruby gem packages, collected from file, defined by path.
        :param api_data: api data set
        :return: result
        """
        if self.load_gem_packages_from_path(api_data=api_data):
            if self.parse_gem_packages_from_path(api_data=api_data):
                print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                return True

        print_line('Something wrong with packages in file path {0}.'.format(api_data['file']))
        return False

    def get_components_npm_auto_system_none(self, api_data):
        # type: (dict) -> bool
        """
        Get NPM packages, collected from shell command, that is called globally.
        :param api_data: api data set
        :return: result
        """
        if self.load_npm_packages(api_data=api_data, local=False):
            api_data['packages'] = raw_npm_components
            if self.parse_npm_packages(api_data=api_data):
            # if self.parse_npm_lock_packages(api_data=api_data):
                print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                return True

        print_line('Something wrong with packages in NPM system call.')
        return False

    def get_components_npm_local_auto_system_none(self, api_data):
        # type: (dict) -> bool
        """
        Get NPM packages, collected from shell command, that is called locally from path.
        :param api_data: api data set
        :return: result
        """
        if self.load_npm_packages(api_data=api_data, local=True):
            api_data['packages'] = raw_npm_components
            if self.parse_npm_packages(api_data=api_data):
            # if self.parse_npm_lock_packages(api_data=api_data):
                print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                return True

        print_line('Something wrong with packages in file path')
        return False

    def get_components_npm_lock_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Get NPM packages from lock file, defined by path.
        :param api_data: api data set
        :return: result
        """
        if self.load_npm_lock_packages_from_path(api_data=api_data):
            if self.parse_npm_lock_packages(api_data=api_data):
                print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                return True

        print_line('Something wrong with packages in file path')
        return False

    def get_components_gem_auto_system_none(self, api_data):
        # type: (dict) -> bool
        """
        Get Ruby gem packages, collected from shell command, that is called globally.
        :param api_data: api data set
        :return: result
        """
        if self.load_gem_packages_system(api_data=api_data, local=False):
            if self.parse_gem_packages_system(api_data=api_data):
                print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                return True

        print_line('Something wrong with packages in file path')
        return False

    def get_components_gemfile_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Get Ruby gem packages, collected from Gemfile, defined by path.
        :param api_data: api data set
        :return: result
        """
        if self.load_gemfile_packages_from_path(api_data=api_data):
            if self.parse_gemfile_packages(api_data=api_data):
                print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                return True

        print_line('Failed load or parse Gemfile packages.')
        return False

    def get_components_gemfile_lock_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Get Ruby gem packages, collected from Gemfile.lock, defined by path.
        :param api_data: api data set
        :return: result
        """
        if self.load_gemfile_lock_packages_from_path(api_data=api_data):
            if self.parse_gemfile_lock_packages(api_data=api_data):
                print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                return True

        print_line('Failed parse Gemfile packages.')
        return False

    def get_components_any_auto_user_path(self, api_data):
        # type: (dict) -> bool
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
                return False

            components = []
            with open(filename, 'r') as pf:
                packages = pf.read().split('\n')
                for package in packages:
                    if len(package) != 0:
                        if '=' in package:
                            splitted_package = package.split('=')
                            if len(splitted_package) == 2:
                                components.append({'name': splitted_package[0], 'version': splitted_package[1]})
                api_data['components'] = components
                print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                return True

        print_line('File {0} not found.'.format(filename))
        return False

    def get_components_any_manual_user_none(self, api_data):
        # type: (dict) -> bool
        """
        Get packages from console.
        :return: result
        """
        components = []
        if ask('Continue (y/n)? ') == 'n':
            return False
        while True:
            name = ask('Enter component name: ')
            version = ask('Enter component version: ')
            components.append({'name': name, 'version': version})
            if ask('Continue (y/n)? ') == 'n':
                break
        api_data['components'] = components
        print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
        return True

    def get_components_php_composer_json_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Get packages from PHP Composer.json file.
        :return: result
        """
        if self.load_php_composer_json_system_path(api_data=api_data):
            if self.parse_php_composer_json_system_path(api_data=api_data):
                print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                return True

        print_line('PHP Composer packages loading error.')
        return False

    def get_components_php_composer_lock_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Get packages from PHP Composer.lock file.
        :return: result
        """
        if self.load_php_composer_lock_system_path(api_data=api_data):
            if self.parse_php_composer_lock_system_path(api_data=api_data):
                print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
                return True

        print_line('PHP Composer.lock packages loading error.')
        return False

    def get_components_maven_pom(self, api_data):
        # type: (dict) -> bool
        """
        Get dependencies from Maven pom.xml file.
        :param api_data: api data set
        :return: result
        """
        if self.load_maven_pom_components_path(api_data=api_data):
            print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
            return True

        print_line('Maven pom.xml file packages loading error.')
        return False

    def get_components_yarn_lock(self, api_data):
        # type: (dict) -> bool
        """
        Get dependencies from yarn.lock file.
        :param api_data: api data set
        :return: result
        """
        if self.load_yarn_lock_components_path(api_data=api_data):
            print_line('Collect {0} raw components before processing and verification'.format(len(api_data['components'])))
            return True

        print_line('Yarn.lock file packages loading error.')
        return False

    # -------------------------------------------------------------------------
    # Loaders
    # -------------------------------------------------------------------------

    def load_maven_pom_components_path(self, api_data):
        # type: (dict) -> bool
        """
        Load packages from Maven pom.xml file.
        :param api_data: api data set
        :return: result
        """
        filename = api_data['file']
        components = []

        if os.path.exists(filename):
            enc = self.define_file_encoding(filename=filename)

            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return False

            try:
                with open(api_data['file'], 'r') as fd:
                    doc = xmltodict.parse(fd.read())

                if 'project' in doc:
                    project = doc['project']
                    if 'dependencies' in project:
                        dependencies = project['dependencies']
                        for dependency in dependencies['dependency']:
                            components.append({"name": dependency["groupId"], "version": dependency["version"]})
                api_data['components'] = components
                return True

            except Exception as e:
                print_line('File read exception {0}.'.format(e))
                return False

        print_line('File {0} does not exists.'.format(filename))
        return False

    def load_yarn_lock_components_path(self, api_data):
        # type: (dict) -> bool
        """
        Load packages from yarn.lock file.
        :param api_data: api data set
        :return: result
        """
        filename = api_data['file']
        components = []

        if os.path.exists(filename):
            enc = self.define_file_encoding(filename=filename)

            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return False

            try:
                with open(filename, 'r') as pf:
                    yarn_file = pf.read()

                yarn_sections = yarn_file.split('\n\n')

                components = []
                sections = []

                for section in yarn_sections:
                    ysection = []
                    ss = section.split('\n')
                    for s in ss:
                        if s.startswith('#'):
                            continue
                        if s == '':
                            continue
                        ysection.append(s)
                    if len(ysection) > 1:
                        sections.append(ysection)

                for section in sections:
                    name = section[0].replace(':', '')
                    name = name[:name.index('@')].replace('"', '')
                    version = section[1].replace(' ', '').replace('version', '').replace('"', '').replace('~', '')
                    if version != '*':
                        if '|' not in version:
                            components.append({"name": name, "version": version})
                    if len(section) > 4:
                        if 'dependencies' in section[3]:
                            for i in range(4, len(section)):
                                if 'optionalDependencies:' in section[i]:
                                    continue
                                ssection = section[i]\
                                    .replace(' ', '')\
                                    .replace('^', '')\
                                    .replace('<', '')\
                                    .replace('>', '')\
                                    .replace('=', '')
                                dname = ssection[:ssection.index('"')].replace('"', '')
                                dversion = ssection[ssection.index('"'):].replace('"', '').replace('~', '')
                                if dversion != '*':
                                    if '|' not in dversion:
                                        components.append({"name": dname, "version": dversion})

                api_data['components'] = components
                return True

            except Exception as e:
                print_line('File read exception {0}.'.format(e))
                return False

        print_line('File {0} does not exists.'.format(filename))
        return False


    def load_windows_10_packages_from_shell(self, api_data):
        # type: (dict) -> bool
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
                return False

            if output:
                api_data['packages'] = output
                return True

            return False

        except OSError as os_error:
            print_line('Powershell command throw errno: {0}, strerror: {1} and filename: {2}.'.format(os_error.errno, os_error.strerror, os_error.filename))
            return False

        except Exception as common_exception:
            print_line('Powershell command throw an exception: {0}.'.format(common_exception))
            return False

    def load_windows_10_packages_from_path(self, api_data):
        # type: (dict) -> bool
        """
        Get OS packages for Windows platform from unloaded file, that was created by shell command manually.
        :param filename: path to file
        :return: result
        """

        filename = api_data['file']

        if os.path.exists(filename):

            enc = self.define_file_encoding(filename=filename)

            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return False

            try:
                with open(filename, 'r') as cf:
                    os_packages = cf.read()

                    if os_packages is None:
                        print_line('Cant read file: {0}.'.format(filename))
                        return False

                    api_data['packages'] = os_packages.replace('\r', '').split('\n')[9:]
                    return True

            except Exception as e:
                print_line('File read exception {0}.'.format(e))
                return False

        print_line('File {0} does not exists.'.format(filename))
        return False

    def load_ubuntu_packages_from_shell(self, api_data):
        # type: (dict) -> bool
        """
        Load OS packages for Ubuntu platform by shell command.
        :return: result
        """

        cmd = "dpkg -l | grep '^ii '"

        try:
            if platform.system() == "Linux" or \
                    platform.system() == "linux" or \
                    platform.linux_distribution()[0] == 'debian':

                proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()

                if error:
                    print_line('Shell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                    return False

                if output:
                    api_data['packages'] = output.decode("utf-8")
                    return True

                return False

            print_line('Platform not defined as Debian.')
            return False

        except OSError as os_error:
            print_line('Shell command throw errno: {0}, strerror: {1} and filename: {2}.'.format(os_error.errno, os_error.strerror, os_error.filename))
            return False

        except Exception as common_exception:
            print_line('Shell command throw an exception: {0}.'.format(common_exception))
            return False

    def load_ubuntu_packages_from_path(self, api_data):
        # type: (dict) -> bool
        """
        Load OS packages for Ubuntu platform from filem created by shell command.
        :return: result
        """

        filename = api_data['file']

        if os.path.exists(filename):

            enc = self.define_file_encoding(filename=filename)

            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return False

            try:
                with open(filename, 'r') as cf:

                    os_packages = cf.read()

                    if os_packages is None:
                        print_line('Cant read file: {0}.'.format(filename))
                        return False

                    api_data['packages'] = os_packages
                    return True

            except Exception as e:
                print_line('File read exception {0}.'.format(e))
                return False

        print_line('File {0} does not exists.'.format(filename))
        return False

    def load_fedora_packages_from_shell(self, api_data):
        # type: (dict) -> bool
        """
        Load OS packages for Fedora platform by shell command.
        :return: result
        """

        cmd = "rpm -qa"

        try:
            api_data['packages'] = os.popen(cmd).readlines()
            return True

        except OSError as os_error:
            print_line('Shell command throw errno: {0}, strerror: {1} and filename: {2}.'.format(os_error.errno, os_error.strerror, os_error.filename))
            return False

        except Exception as common_exception:
            print_line('Shell command throw an exception: {0}.'.format(common_exception))
            return False

    def load_fedora_packages_from_path(self, api_data):
        # type: (dict) -> bool
        """
        Load OS packages for Fedora platform from file, created by shell command.
        :return: result
        """

        filename = api_data['file']

        if os.path.exists(filename):

            enc = self.define_file_encoding(filename=filename)

            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return False

            try:
                with open(filename, 'r') as cf:
                    os_packages = cf.read()

                    if os_packages is None:
                        print_line('Cant read file: {0}.'.format(filename))
                        return False

                    api_data['packages'] = os_packages
                    return True

            except Exception as e:
                print_line('File read exception {0}.'.format(e))
                return False

        print_line('File {0} does not exists.'.format(filename))
        return False

    def load_macos_packages_from_shell(self, api_data):
        # type: (dict) -> bool
        """
        Load OS packages for MacOS platform by shell command.
        :return: result
        """

        cmd = 'system_profiler -detailLevel full SPApplicationsDataType | grep "Location: /\| Version: "'

        try:
            if platform.system() == 'darwin' or platform.system() == 'Darwin':
                proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()

                if error:
                    print_line('Shell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                    return False

                if output:
                    api_data['packages'] = output.decode("utf-8").replace(' ', '').replace(',', '.').split('\n')
                    return True

                return False

        except OSError as os_error:
            print_line('Shell command throw errno: {0}, strerror: {1} and filename: {2}.'.format(os_error.errno, os_error.strerror, os_error.filename))
            return False

        except Exception as common_exception:
            print_line('Shell command throw an exception: {0}.'.format(common_exception))
            return False

    def load_macos_packages_from_path(self, api_data):
        # type: (dict) -> bool
        """
        Load OS packages for MacOS platform from file, created by shell command.
        :return: result
        """

        filename = api_data['file']

        if os.path.exists(filename):

            enc = self.define_file_encoding(filename=filename)

            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return False

            try:
                with open(filename, 'r') as cf:
                    os_packages = cf.read().replace(' ', '').replace(',', '.').split('\n')

                    if os_packages is None:
                        print_line('Cant read file: {0}.'.format(filename))
                        return False

                    api_data['packages'] = os_packages
                    return True

            except Exception as e:
                print_line('File read exception {0}.'.format(e))
                return False

        print_line('File {0} does not exists.'.format(filename))
        return False

    def load_pip_packages_from_shell_legacy(self, api_data):
        # type: (dict) -> bool
        """
        Load Python PI packages with pip.FrozenRequirement method.
        :return: result
        """
        if api_data['target'] == 'pip':
            cmd = "pip list --format=legacy"
        elif api_data['target'] == 'pip3':
            cmd = "pip3 list --format=legacy"

        try:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output, error = proc.communicate()

            if error:
                print('Get Python PIP packages from shell error.')
                return False

            if output:
                if len(output) > 0:
                    api_data['packages'] = output.decode('utf-8')
                    return True
                else:
                    return False

        except Exception as common_exception:
            print("An exception {0} occured while shell command was called.".format(common_exception))
            return False

    def load_pip_packages_from_path(self, api_data):
        # type: (dict) -> bool
        """
        Load Python PIP packages from file.
        :param filename: path to file
        :return: result
        """

        filename = api_data['file']

        if os.path.exists(filename):

            enc = self.define_file_encoding(filename)

            if enc == 'undefined':
                print_line('Undefined file {0} encoding.'.format(filename))
                return False

            try:
                with open(filename, 'r') as cf:
                    rfp = cf.read()
                    api_data['packages'] = rfp.replace(' ', '').split('\n')
                    return True

            except Exception as e:
                print_line('Get an exception {0}, when read file {1}'.format(e, filename))
                return False

        print_line('File {0} does not exists.'.format(filename))
        return False

    def load_npm_packages_from_path(self, api_data):
        # type: (dict) -> bool
        """
        Load NPM packages from file, defined by path.
        :param filename: path to file
        :return: result
        """

        filename = api_data['file']

        if os.path.exists(filename):

            enc = self.define_file_encoding(filename)

            if enc == 'undefined':
                print_line('Undefined file {0} encoding.'.format(filename))
                return False

            try:
                with open(filename, 'r') as pf:
                    data = json.load(pf)
                    walkdict(data)
                    return True

            except Exception as e:
                print_line('File read exception: {0}'.format(e))
                return False

        print_line('File {0} does not exist.'.format(filename))
        return False

    def load_npm_packages(self, api_data, local):
        path = api_data['file']
        if local:
            os.chdir(path)
        else:
            if api_data['os_type'] == OSs.WINDOWS:
                os.chdir('c:\\')
            else:
                os.chdir('/')

        cmd = "npm list --json"

        if api_data['os_type'] == OSs.WINDOWS:
            proc = subprocess.Popen(["powershell", cmd], stdout=subprocess.PIPE, shell=True)
            output, error = proc.communicate()
        elif api_data['os_type'] == OSs.MACOS or \
                api_data['os_type'] == OSs.UBUNTU or \
                api_data['os_type'] == OSs.DEBIAN or \
                api_data['os_type'] == OSs.FEDORA:
            proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = proc.communicate()

        if output:
            if output == '{}\n' or output == '{}':
                raw_npm_components = []
                return True
            else:
                if isinstance(output, bytes):
                    data = json.loads(output.decode("utf-8"))
                elif isinstance(output, str):
                    data = json.loads(output)
                walkdict(data)
                return True

        return False

    def load_package_json_packages_from_path(self, api_data):
        # type: (dict) -> bool
        """
        Load NPM packages from package.json file, defined by path.
        :param filename: path to file
        :return: result
        """

        filename = api_data['file']

        if os.path.exists(filename):
            enc = self.define_file_encoding(filename=filename)

            if enc == 'undefined':
                print_line('Undefined file {0} encoding.'.format(filename))
                return False

            try:
                with open(filename, 'r') as pf:
                    api_data['packages'] = json.load(pf)
                    return True

            except Exception as e:
                print_line('File {0} read exception: {1}'.format(filename, e))
                return False

        print_line('File does not exist.')
        return False

    def load_npm_lock_packages_from_path(self, api_data):
        # type: (dict) -> bool
        """
        Load NPM packages from lock file, defined by path.
        :param filename: path to file
        :return: result
        """

        filename = api_data['file']

        if os.path.exists(filename):

            enc = self.define_file_encoding(filename=filename)

            if enc == 'undefined':
                print_line('Undefined file {0} encoding.'.format(filename))
                return False

            try:
                with open(filename, 'r') as pf:
                    try:
                        api_data['packages'] = json.load(pf)
                        return True

                    except json.JSONDecodeError as json_decode_error:
                        print_line('An exception occured with json decoder: {0}.'.format(json_decode_error))
                        return False

            except Exception as e:
                print_line('File {0} read exception: {1}'.format(filename, e))
                return False

        print_line('File does not exist.')
        return False

    def load_gem_packages_from_path(self, api_data):
        # type: (dict) -> bool
        """
        Load Ruby gem packages from file, defined by path.
        :param filename: path to file
        :return: result
        """

        filename = api_data['file']

        if os.path.exists(filename):

            enc = self.define_file_encoding(filename)

            if enc == 'undefined':
                print_line('Undefined file {0} encoding.'.format(filename))
                return False

            try:
                with open(filename, 'r') as pf:
                    cont = pf.read().replace('default: ', '').replace(' ', '').replace(')', '')
                    api_data['packages'] = cont.split('\n')
                    return True

            except Exception as e:
                print_line('File {0} read exception: {1}'.format(filename, e))
                return False

        print_line('File {0} does not exist.'.format(filename))
        return False

    def load_gem_packages_system(self, api_data, local):
        # type: (dict, bool) -> bool
        """
        Load Ruby gem packages from global or local call of shell commend.
        :param local: local or global
        :param api_data: api data set
        :return: result
        """

        if local:
            try:
                os.chdir(api_data['file'])
            except Exception as common_exception:
                print_line('OS.Chdir get an exception {common_exception}'.format(common_exception))
                return False
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
                    return False

                if output:
                    api_data['packages'] = output
                    return True

            elif api_data['os_type'] == OSs.CENTOS or \
                    api_data['os_type'] == OSs.DEBIAN or \
                    api_data['os_type'] == OSs.UBUNTU or \
                    api_data['os_type'] == OSs.FEDORA or \
                    api_data['os_type'] == OSs.MACOS:
                proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()
                output = output.decode('utf-8').replace('\r', '').split('\n')

                if error:
                    print_line('Shell command throw {0} code and {1} error message.'.format(proc.returncode, error.strip()))
                    return False

                if output:
                    api_data['packages'] = output
                    return True

        except OSError as os_error:
            print_line('Shell command throw errno: {0}, strerror: {1} and filename: {2}.'.format(os_error.errno, os_error.strerror, os_error.filename))
            return False

        except Exception as common_exception:
            print_line('Shell command throw an exception: {0}.'.format(common_exception))
            return False

    def load_gemfile_packages_from_path(self, api_data):
        # type: (dict) -> bool
        """
        Load packages from Gemfile. defined by path.
        :param filename: filename
        :return: result
        """

        filename = api_data['file']

        if os.path.isfile(filename):

            enc = self.define_file_encoding(filename=filename)

            if enc == 'undefined':
                print_line('Undefined file {0} encoding.'.format(filename))
                return False

            try:
                with open(filename, 'r') as pf:
                    cont = pf.read()
                    api_data['packages'] = cont.split('\n')
                    return True

            except Exception as e:
                print_line('File {0} read exception: {1}'.format(filename, e))
                return False

        print_line('File does not exist.')
        return False

    def load_gemfile_lock_packages_from_path(self, api_data):
        # type: (dict) -> bool
        """
        Load packages from Gemfile.lock defined by path.
        :param filename: filename
        :return: result
        """

        filename = api_data['file']

        if os.path.isfile(filename):

            enc = self.define_file_encoding(filename=filename)

            if enc == 'undefined':
                print_line('Undefined file {0} encoding.'.format(filename))
                return False

            try:
                with open(filename, 'r') as pf:
                    cont = pf.read()
                    api_data['packages'] = cont.split('\n')
                    return True

            except Exception as e:
                print_line('File {0} read exception: {1}'.format(filename, e))
                return False

        print_line('File does not exist.')
        return False

    def load_php_composer_json_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Load packages from PHP Composer.json defined by path.
        :param filename: filename
        :return: result
        """

        filename = api_data['file']

        if os.path.isfile(filename):

            enc = self.define_file_encoding(filename=filename)

            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return False

            with open(filename, mode='r') as pf:
                try:
                    api_data['packages'] = json.load(pf)
                    return True

                except json.JSONDecodeError as json_decode_error:
                    print_line('An exception occured with json decoder: {0}.'.format(json_decode_error))
                    return False

        print_line('File {0} not found.'.format(filename))
        return False

    def load_php_composer_lock_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Load packages from PHP Composer.lock defined by path.
        :param filename: filename
        :return: result
        """

        filename = api_data['file']

        if os.path.isfile(filename):

            enc = self.define_file_encoding(filename=filename)

            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return False

            with open(filename, 'r') as pf:
                try:
                    api_data['packages'] = json.load(pf)
                    return True

                except json.JSONDecodeError as json_decode_error:
                    print_line('An exception occured with json decoder: {0}.'.format(json_decode_error))
                    return False

        print_line('File {0} not found.'.format(filename))
        return False

    # -------------------------------------------------------------------------
    # Parsers
    # -------------------------------------------------------------------------

    @staticmethod
    def parse_windows_10_packages(api_data):
        # type: (dict) -> bool
        """
        Parse Windows 10 packages.
        :param report: raw report
        :return: result
        """
        report = api_data['packages']
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
            api_data['components'] = packages
            return True

        except Exception as common_exception:
            print_line('Exception {0} occured.'.format(common_exception))
            return False

    @staticmethod
    def parse_ubuntu_packages(api_data):
        # type: (dict) -> bool
        """
        Parse Ubuntu package list.
        :param _report: raw packages.
        :return: result
        """
        if isinstance(api_data['packages'], list):
            number_of_line_breaks = api_data['packages']
        else:
            number_of_line_breaks = api_data['packages'].split('\n')
        # number_of_line_breaks = api_data['packages']
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
        api_data['components'] = new_components
        return True

    @staticmethod
    def parse_fedora_packages(api_data):
        # type: (dict) -> bool
        """
        Parse Fedora package list.
        :param _report: raw packages.
        :return: result
        """

        new_components = []
        number_of_line_breaks = api_data['packages']
        for line in number_of_line_breaks:
            line = line.replace('\n', '')
            pattern = '\s*\-\s*'
            component_array = re.split(pattern, line)
            if len(component_array) >= 2:
                name = component_array[0]
                version = component_array[1]
                new_components.append({'name': name, 'version': version})
        api_data['components'] = new_components
        return True

    @staticmethod
    def parse_macos_packages(api_data):
        # type: (dict) -> bool
        """
        Parse MacOS packages.
        :param _report: raw packages
        :return: result
        """
        output = api_data['packages']

        templ = {'name': '', 'version': ''}
        packages = []

        ver_or_loc = 1

        if len(output) == 0:
            exit(1)

        # check first string
        if 'Version:' in output[0].upper():
            ver_or_loc = 1
        elif 'Location:' in output[0].upper():
            ver_or_loc = 2

        for out in output:
            if 'Version:' in out:
                templ['version'] = out.replace('Version:', '')
                templ['name'] = None

            elif 'Location:' in out:
                templ['name'] = out.replace('Location:', '')
                if templ['version'] is None:
                    i = templ['name'].rfind('/')
                    templ['version'] = templ['name'][i:].replace('.app', '').replace('/', '')
                package = {"name": None, "version": None}
                i = templ['name'].rfind('/')
                package["name"] = templ["name"][i:].replace('.app', '').replace('/', '')
                package["version"] = templ["version"]

                # delete all except digits and .
                package["version"] = re.sub(r'[^0123456789\.]', '', package["version"])

                # delete all digits
                package["name"] = re.sub(r'[^\w\s]+|[\d]+', r'', package["name"])

                if package["version"] != '':
                    packages.append(package)
                del package
                templ['version'] = None
        api_data['components'] = packages
        return True

    @staticmethod
    def parse_pip_packages_legacy(api_data):
        # type: (dict) -> bool
        """
        Parse PIP legacy packages.
        :param _report: raw packages
        :return: result
        """

        packages = api_data['packages']
        packages = packages.replace(')', '')
        packages = packages.replace(' ', '')
        packages = packages.split('\r\n')
        if len(packages) == 1:
            packages = packages[0].split('\n')
        components = []
        for package in packages:
            if len(package) <= 3:
                continue
            line = package.split('(')
            name = line[0]
            version = line[1]
            components.append({'name': name, 'version': version})
        api_data['components'] = components
        return True

    @staticmethod
    def parse_pip_packages_from_path(api_data):
        # type: (dict) -> bool
        """
        Parse Python PIP packages report.
        :param packages: raw packages
        :return: result
        """
        packages = api_data['packages']
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
                        # components.append({'name': ref, 'version': '*'})
                        continue
        api_data['components'] = components
        return True

    @staticmethod
    def parse_npm_packages(api_data):
        # type: (dict) -> bool
        """
        Parse NPM raw packages.
        :param api_data: api data set
        :param comp: raw packages.
        :return: result
        """
        npm_components = api_data['packages']
        components = []

        for comp in npm_components:
            if 'from' in comp['name']:
                if '@' in comp['version']:
                    name = comp['version'].split('@')[0]
                    version = comp['version'].split('@')[1]
                    myversion = version
                    if version == 'latest':
                        cmd = 'npm view {0} version'.format(name)
                        try:
                            if api_data['os_type'] == OSs.WINDOWS:
                                proc = subprocess.Popen(["powershell", cmd], shell=True, stdout=subprocess.PIPE)
                                version, error = proc.communicate()
                            else:
                                proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                                version, error = proc.communicate()
                            if version:
                                myversion = version.decode('utf-8').replace('\n', '')
                        except Exception as e:
                            print_line('Get an exception {0} for npm component {1} version info.'.format(e, name))
                            myversion = 'latest'
                    components.append({'name': name, 'version': myversion})

        api_data['components'] = components
        return True

    @staticmethod
    def parse_npm_lock_packages(api_data):
        # type: (dict) -> bool
        """
        Parse NPM lock packages.
        :param packages: raw packages.
        :return: result
        """
        def already_in_components(components, key):
            # type: (str) -> bool
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

        packages = api_data['packages']
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
        api_data['components'] = components
        return True

    @staticmethod
    def parse_package_json_packages_from_path(api_data):
        # type: (dict) -> bool
        """
        Parse package.json file.
        :param packages: raw packages
        :return: result
        """
        packages = api_data['packages']
        components = []
        if 'dependencies' in packages:
            dependencies = packages['dependencies']
        else:
            dependencies = {}
        if 'devDependencies' in packages:
            dev_dependencies = packages['devDependencies']
        else:
            dev_dependencies = {}
        if dev_dependencies != {}:
            for key in dev_dependencies.keys():
                components.append({'name': key, 'version': str(dev_dependencies[key]).replace('^', '')})
        if dependencies != {}:
            for key in dependencies.keys():
                components.append({'name': key, 'version': str(dependencies[key]).replace('^', '')})
        api_data['components'] = components
        return True

    def parse_gem_packages_system(self, api_data):
        # type: (dict) -> bool
        """
        Parse Ruby gem packages.
        :param packages: raw packages.
        :return: result
        """
        return self.parse_gem_packages_from_path(api_data=api_data)

    @staticmethod
    def parse_gem_packages_from_path(api_data):
        # type: (dict) -> bool
        """
        Parse Ruby gem packages from path.
        :param packages: raw packages
        :return: result
        """
        packages = api_data['packages']
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
        api_data['components'] = components
        return True

    @staticmethod
    def parse_gemfile_packages( api_data):
        # type: (dict) -> bool
        """
        Parse packages from Gemfile.
        :param packages: list of packages
        :return: result
        """
        content_splitted_by_strings = api_data['packages']
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
        api_data['components'] = unique_packages
        return True

    @staticmethod
    def parse_gemfile_lock_packages(api_data):
        # type: (dict) -> bool
        """
        Parse packages from Gemfile
        :param packages: list of packages
        :return: result
        """
        splitted_content_by_strings = api_data['packages']
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
        api_data['components'] = unique_packages
        return True

    @staticmethod
    def parse_php_composer_json_system_path(api_data):
        # type: (dict) -> bool
        """
        Parse packages from PHP Composer json file
        :param packages: list of packages
        :return: result
        """
        content = api_data['packages']
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

        api_data['components'] = unique_packages
        return True

    @staticmethod
    def parse_php_composer_lock_system_path(api_data):
        # type: (dict) -> bool
        """
        Parse packages from PHP Composer.lock file.
        :param _packages: list of packages
        :return: result
        """
        content = api_data['packages']
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

        api_data['components'] = unique_packages
        return True

    # -------------------------------------------------------------------------
    # Addition methods
    # -------------------------------------------------------------------------

    @staticmethod
    def define_file_encoding(filename):
        # type: (str) -> str
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
        # type: (dict) -> str
        """
        Get current component set name.
        :param api_data: api data set
        :return: result
        """
        if api_data['organization'] is None:
            return False
        if api_data['organization']['platforms'] is None:
            return False
        platform_number = self.web_api.get_platform_number_by_name(api_data=api_data)
        if platform_number == -1:
            return False
        project_number = self.web_api.get_project_number_by_name(api_data=api_data)
        if project_number == -1:
            return ['0.0.1']
        return [api_data['organization']['platforms'][platform_number]['projects'][project_number]['current_component_set']['name']]

    def get_current_component_set(self, api_data):
        # type: (dict) -> list
        """
        Get current component set for platform/project.
        :param api_data: api data set
        :return: result
        """
        if api_data['organization'] is None:
            return False
        if api_data['organization']['platforms'] is None:
            return False
        platform_number = self.web_api.get_platform_number_by_name(api_data=api_data)
        if platform_number == -1:
            return False
        project_number = self.web_api.get_project_number_by_name(api_data=api_data)
        if project_number == -1:
            return False
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