# -*- coding: utf-8 -*-
"""
Main CLI App API module.
"""


import os
import yaml

from core.interface import print_line
from core.webapi import WebAPI
from core.platform_helper.platform_helper import PlatformHelper
from core.project_helper.project_helper import ProjectHelper
from core.set_helper.set_helper import SetHelper
from core.show_helper.show_helper import ShowHelper
from core.components_helper.components_helper import ComponentsHelper
from core.os_parameters import get_os_platform
from core.os_parameters import get_os_version
from core.os_parameters import get_os_sp
from core.os_parameters import get_os_release
from core.os_parameters import get_os_machine

class API(object):
    """
    Main CLI App API class.
    """

    def __init__(self):
        self.web_api = WebAPI()

    # -------------------------------------------------------------------------
    # Run actions
    # -------------------------------------------------------------------------

    def run_action(self, api_data):
        """
        Main routing method for CLI app actions.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Validate api data set structure

        if not self.validate_api_data_structure_is_ok(api_data=api_data):
            return False

        # Validate actions

        if not self.validate_action_type_is_ok(api_data=api_data):
            return False

        # Action: save config into file and exit

        if api_data['action'] == Actions.SAVE_CONFIG:
            return self.save_config_to_file(api_data=api_data)

        # Select login method for current session

        if not self.select_login_method(api_data=api_data):
            return False

        # Action: Login into server

        if not self.action_login_server_success(api_data=api_data):
            return False

        # If login was successfull - get organization parameters from server

        if not self.get_organization_parameters_from_server(api_data=api_data):
            return False

        # Action: Create new Platform

        if api_data['action'] == Actions.CREATE_PLATFORM:
            return self.action_create_new_platform(api_data=api_data)

        # Action: Create new Project

        elif api_data['action'] == Actions.CREATE_PROJECT:
            return self.action_create_new_project(api_data=api_data)

        # Action: Create new Component Set

        elif api_data['action'] == Actions.CREATE_SET:
            return self.action_create_new_set(api_data=api_data)

        # Action: Show information about Platforms, Projects, Component Set or Issues

        elif api_data['action'] == Actions.SHOW_PLATFORMS or \
                api_data['action'] == Actions.SHOW_PROJECTS or \
                api_data['action'] == Actions.SHOW_SET or \
                api_data['action'] == Actions.SHOW_ISSUES:
            return self.action_show_platforms_projects_or_sets(api_data=api_data)

        # Action: Delete Platform

        elif api_data['action'] == Actions.DELETE_PLATFORM:
            return self.action_delete_platform(api_data=api_data)

        # Action: Delete Project

        elif api_data['action'] == Actions.DELETE_PROJECT:
            return self.action_delete_project(api_data=api_data)

        # Action: Archive Platform

        elif api_data['action'] == Actions.ARCHIVE_PLATFORM:
            return self.action_archive_platform(api_data=api_data)

        # Action: Archive Project

        elif api_data['action'] == Actions.ARCHIVE_PROJECT:
            return self.action_archive_project(api_data=api_data)

        # Action: Restore Platform

        elif api_data['action'] == Actions.RESTORE_PLATFORM:
            return self.action_restore_platform(api_data=api_data)

        # Action: Restore Project

        elif api_data['action'] == Actions.RESTORE_PROJECT:
            return self.action_restore_project(api_data=api_data)

        # Otherwise

        print_line("Unknown action code: {0}.".format(api_data['action']))
        return False

    # -------------------------------------------------------------------------
    # LOGIN
    # -------------------------------------------------------------------------

    def select_login_method(self, api_data):
        # type: (dict) -> bool
        """
        Select login method for current session.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # If auth_token or user/password presents in command line

        if api_data['login_method'] == 'token' or api_data['login_method'] == 'username_and_password':
            if api_data['team'] is None or api_data['team'] == '':
                print_line('Token authorization requires --team parameter.')
                return False

            return True

        # If login will be with data from config file

        elif api_data['login_method'] == 'config_file':
            if self.load_config_from_file(api_data=api_data):
                if api_data['auth_token'] is not None and api_data['auth_token'] != '':
                    api_data['login_method'] = 'token'
                else:
                    api_data['login_method'] = 'username_and_password'
                return True

        # Otherwise

        return False

    def action_login_server_success(self, api_data):
        """
        Log in into server.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # If login method is auth_token

        if api_data['login_method'] == 'token':
            return self.web_api.send_login_token_request(api_data=api_data)

        # If login method is user/password

        elif api_data['login_method'] == 'username_and_password':
            return self.web_api.send_login_user_password_request(api_data=api_data)

        # Otherwise

        return False

    # -------------------------------------------------------------------------
    # GET ORGANIZATION PARAMETERS
    # -------------------------------------------------------------------------

    def get_organization_parameters_from_server(self, api_data):
        """
        Get organization parameters from Surepatch server and fill the
        appropriate structure.
        :param api_data: api data set
        :return: result, modify api_data
        """

        return self.web_api.send_get_organization_parameters_request(api_data=api_data)

    # -------------------------------------------------------------------------
    # PLATFORM
    # -------------------------------------------------------------------------

    @staticmethod
    def action_create_new_platform(api_data):
        """
        Run action: CREATE New Platform.
        :param api_data: api data set
        :return: result, modify api_data
        """

        platform_helper = PlatformHelper()

        # Validate Platform parameters

        if not platform_helper.create_platform_validate(api_data=api_data):
            return False

        # Create new Platform

        return platform_helper.create_platform(api_data=api_data)

    # -------------------------------------------------------------------------
    # PROJECT
    # -------------------------------------------------------------------------

    def action_create_new_project(self, api_data):
        """
        Run action: CREATE New Project in different cases.
        :param api_data: api data set
        :return: result, modify api_data
        """

        project_helper = ProjectHelper()

        # Validate Project parameters

        if not project_helper.create_project_validate(api_data=api_data):
            return False

        # For loop -> for targets. and than, send web request

        targets = api_data['target']
        files = api_data['file']

        for i in range(0, len(targets)):
            # Select variant of CREATE Project action

            api_data['target'] = targets[i]
            api_data['file'] = files[i]

            # Create new project with OS packages {from shell request}

            if api_data['target'] == Targets.OS and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is None:
                if not project_helper.collect_data_for_project_os_auto_system_none(api_data=api_data):
                    return False

            # Create new project with OS packages from shell request unloading file {from path}

            if api_data['target'] == Targets.OS and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_os_auto_system_path(api_data=api_data):
                    return False

            # Create new project with Python 2 PIP packages {from shell request}

            if api_data['target'] == Targets.PIP and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is None:
                if not project_helper.collect_data_for_project_pip_auto_system_none(api_data=api_data):
                    return False

            # Create new project with Python 3 PIP packages {from shell request}

            if api_data['target'] == Targets.PIP3 and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is None:
                if not project_helper.collect_data_for_project_pip_auto_system_none(api_data=api_data):
                    return False

            # Create new project with Python 2 PIP from file {from path}

            if api_data['target'] == Targets.PIP and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_data_for_project_pip_auto_system_path(api_data=api_data):
                    return False

            # Create new project with Python 3 PIP from file {from path}

            if api_data['target'] == Targets.PIP3 and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_data_for_project_pip_auto_system_path(api_data=api_data):
                    return False

            # Create new project with Python 2 PIP from requirements.txt {from path}
            if api_data['target'] == Targets.REQ and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_requirements_auto_system_path(api_data=api_data):
                    return False

            # Create new project with Python 3 PIP from requirements.txt {from path}

            if api_data['target'] == Targets.REQ3 and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_requirements_auto_system_path(api_data=api_data):
                    return False

            # Create new project with Python 2 PIP from requirements.txt {from path}

            if api_data['target'] == Targets.REQUIREMENTS and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_requirements_auto_system_path(api_data=api_data):
                    return False

            # Create new project with Python 3 PIP from requirements.txt {from path}

            if api_data['target'] == Targets.REQUIREMENTS3 and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_requirements_auto_system_path(api_data=api_data):
                    return False

            # Create new project with NPM packages {from shell request} - from root path

            if api_data['target'] == Targets.NPM and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is None:
                if not project_helper.collect_data_for_project_npm_auto_system_none(api_data=api_data):
                    return False

            # Create new project with NPM packages {from shell request} - from local path

            if api_data['target'] == Targets.NPM_LOCAL and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_npm_local_auto_system_none(api_data=api_data):
                    return False

            # Create new project with NPM packages {from path}

            if api_data['target'] == Targets.NPM and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_npm_auto_system_path(api_data=api_data):
                    return False

            # Create new project with NPM package.json file {from path}

            if api_data['target'] == Targets.PACKAGE_JSON and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_package_json_auto_system_path(api_data=api_data):
                    return False

            # Create new project with NPM package_lock.json file {from path}

            if api_data['target'] == Targets.PACKAGE_LOCK_JSON and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_package_lock_json_auto_system_path(api_data=api_data):
                    return False

            # Create new project with GEM packages {from shell request}

            if api_data['target'] == Targets.GEM and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is None:
                if not project_helper.collect_data_for_project_gem_auto_system_none(api_data=api_data):
                    return False

            # Create new project with GEM packages from shell request unloading file {from path}

            if api_data['target'] == Targets.GEM and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_gem_auto_system_path(api_data=api_data):
                    return False

            # Create new project with GEMFILE file {from path}

            if api_data['target'] == Targets.GEMFILE and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_gemfile_auto_system_path(api_data=api_data):
                    return False

            # Create new project with GEMFILE.lock file {from path}

            if api_data['target'] == Targets.GEMFILE_LOCK and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_gemfile_lock_auto_system_path(api_data=api_data):
                    return False

            # Create new project from user format file {from path}

            if api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.USER and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_any_auto_user_path(api_data=api_data):
                    return False

            # Create new project from interactive mode

            if api_data['method'] == Methods.MANUAL and \
                    api_data['format'] == Formats.USER and \
                    api_data['file'] is None:
                if not project_helper.collect_data_for_project_any_manual_user_none(api_data=api_data):
                    return False

            # Create project with PHP Composer.json file {from path}

            if api_data['target'] == Targets.PHP_COMPOSER_JSON and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_php_composer_json_system_path(api_data=api_data):
                    return False

            # Create project with PHP Composer.lock file {from path}

            if api_data['target'] == Targets.PHP_COMPOSER_LOCK and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_php_composer_lock_system_path(api_data=api_data):
                    return False

            # Create project with Maven pom.xml file {from path}

            if api_data['target'] == Targets.POM and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_maven_pom_system_path(api_data=api_data):
                    return False

            # Create project with yarn.lock file {from path}

            if api_data['target'] == Targets.YARN and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not project_helper.collect_data_for_project_yarn_lock_system_path(api_data=api_data):
                    return False

        # If there are some collected components

        if len(api_data['components']) > 0:
            return self.web_api.send_create_new_project_request(api_data=api_data)

        # Otherwise

        print_line('Something wrong with app parameters or components list is empty. Please, look through README.md')
        return False

    # -------------------------------------------------------------------------
    # SET
    # -------------------------------------------------------------------------

    def action_create_new_set(self, api_data):
        """
        Run action: CREATE New Set in different cases.
        :param api_data: api data set
        :return: result, modify api_data
        """

        set_helper = SetHelper()

        # Validate new Component Set parameters

        if not set_helper.create_set_validate(api_data=api_data):
            return False

        targets = api_data['target']
        files = api_data['file']

        # For list of targets

        for i in range(0, len(targets)):

            api_data['target'] = targets[i]
            api_data['file'] = files[i]

            # Create new set with OS packages {from shell request}

            if api_data['target'] == Targets.OS and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is None:
                if not set_helper.collect_data_for_set_os_auto_system_none(api_data=api_data):
                    return False

            # Create set with OS packages from shell request unloading file {from path}

            if api_data['target'] == Targets.OS and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_os_auto_system_path(api_data=api_data):
                    return False

            # Create set with Python 2 PIP packages {from shell request}

            if api_data['target'] == Targets.PIP and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is None:
                if not set_helper.collect_data_for_set_pip_auto_system_none(api_data=api_data):
                    return False

            # Create set with Python 3 PIP packages {from shell request}

            if api_data['target'] == Targets.PIP3 and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is None:
                if not set_helper.collect_data_for_set_pip_auto_system_none(api_data=api_data):
                    return False

            # Create set with Python 2 PIP from file {from path}

            if api_data['target'] == Targets.PIP and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_pip_auto_system_path(api_data=api_data):
                    return False

            # Create set with Python 3 PIP from file {from path}

            if api_data['target'] == Targets.PIP3 and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_pip_auto_system_path(api_data=api_data):
                    return False

            # Create set with PIP requirements.txt {from path}

            if api_data['target'] == Targets.REQ and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_requirements_auto_system_path(api_data=api_data):
                    return False

            # Create set with requirements pip3

            if api_data['target'] == Targets.REQ3 and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_requirements_auto_system_path(api_data=api_data):
                    return False

            # Create set from requirements file

            if api_data['target'] == Targets.REQUIREMENTS and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_requirements_auto_system_path(api_data=api_data):
                    return False

            # Create set from requirements pip3 file

            if api_data['target'] == Targets.REQUIREMENTS3 and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_requirements_auto_system_path(api_data=api_data):
                    return False

            # Create set with NPM packages {from shell request} - global

            if api_data['target'] == Targets.NPM and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is None:
                if not set_helper.collect_data_for_set_npm_auto_system_none(api_data=api_data):
                    return False

            # Create set with NPM packages {from shell request} - local

            if api_data['target'] == Targets.NPM_LOCAL and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_npm_local_auto_system_path(api_data=api_data):
                    return False

            # Create set with NPM packages {from file}

            if api_data['target'] == Targets.NPM and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_npm_auto_system_path(api_data=api_data):
                    return False

            # Create set with NPM package.json file {from path}

            if api_data['target'] == Targets.PACKAGE_JSON and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_package_json_auto_system_path(api_data=api_data):
                    return False

            # Create set with NPM package_lock.json file {from path}

            if api_data['target'] == Targets.PACKAGE_LOCK_JSON and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_package_lock_json_auto_system_path(api_data=api_data):
                    return False

            # Create set with GEM packages {from shell request}

            if api_data['target'] == Targets.GEM and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is None:
                if not set_helper.collect_data_for_set_gem_auto_system_none(api_data=api_data):
                    return False

            # Create set with GEM packages from shell request unloading file {from path}

            if api_data['target'] == Targets.GEM and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_gem_auto_system_path(api_data=api_data):
                    return False

            # Create set with GEMLIST file {from path}

            if api_data['target'] == Targets.GEMFILE and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_gemfile_auto_system_path(api_data=api_data):
                    return False

            # Create set with GEMLIST file {from path}

            if api_data['target'] == Targets.GEMFILE_LOCK and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_gemfile_lock_auto_system_path(api_data=api_data):
                    return False

            # Create set with User defined packages in file (from path{

            if api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.USER and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_any_auto_user_path(api_data=api_data):
                    return False

            # Create set with User defined packages in interactive mode

            if api_data['method'] == Methods.MANUAL and \
                    api_data['format'] == Formats.USER and \
                    api_data['file'] is None:
                if not set_helper.collect_data_for_set_any_manual_user_none(api_data=api_data):
                    return False

            # Create set with PHP Composer.json file {from path}

            if api_data['target'] == Targets.PHP_COMPOSER_JSON and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                return set_helper.collect_data_for_set_php_composer_json_system_path(api_data=api_data)

            # Create set with PHP Composer.lock file {from path}

            if api_data['target'] == Targets.PHP_COMPOSER_LOCK and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_php_composer_lock_system_path(api_data=api_data):
                    return False

            # Create set with pom.xml

            if api_data['target'] == Targets.POM and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_maven_pom_system_path(api_data=api_data):
                    return False

            # Create set with yarn.lock file {from path}

            if api_data['target'] == Targets.YARN and \
                    api_data['method'] == Methods.AUTO and \
                    api_data['format'] == Formats.SYSTEM and \
                    api_data['file'] is not None:
                if not set_helper.collect_data_for_set_yarn_lock_system_path(api_data=api_data):
                    return False

        # If there are some components

        if len(api_data['components']) > 0:
            return self.web_api.send_create_new_component_set_request(api_data=api_data)

        # Otherwise

        print_line('Something wrong with app parameters. Please, look through README.md')
        return False

    # -------------------------------------------------------------------------
    # Show
    # -------------------------------------------------------------------------

    def action_show_platforms_projects_or_sets(self, api_data):
        """
        Run action: Show platforms, projects or component sets.
        :param api_data: api data set
        :return: result
        """

        show_helper = ShowHelper()

        # If action is Show Platforms

        if api_data['action'] == Actions.SHOW_PLATFORMS:
            return show_helper.action_show_platforms(api_data=api_data)

        # If action is Show Projects

        elif api_data['action'] == Actions.SHOW_PROJECTS:
            if api_data['platform'] is None or \
                    api_data['platform'] == '':
                print_line('Empty platform name.')
                return False

            # Get number of Platform in list of Platforms

            platform_number = self.web_api.get_platform_number_by_name(api_data=api_data)

            # It there are not such Platform in list of Platforms

            if platform_number == -1:
                print_line("No such platform: {0}.".format(api_data['platform']))
                return False

            # It is OK, so run action

            return show_helper.action_show_projects(api_data=api_data)

        # If action if Show current Component Set

        elif api_data['action'] == Actions.SHOW_SET:
            if api_data['platform'] is None or \
                    api_data['platform'] == '':
                print_line('Empty platform name.')
                return False

            # Get number of Platform in list of Platforms

            platform_number = self.web_api.get_platform_number_by_name(api_data=api_data)

            # It there are not such Platform in list of Platforms

            if platform_number == -1:
                print_line("No such platform: {0}.".format(api_data['platform']))
                return False

            # If Project name is empty

            if api_data['project'] is None or \
                    api_data['project'] == '':
                print_line('Empty project name.')
                return False

            # Get number of Project in list of Projects

            project_number = self.web_api.get_project_number_by_name(api_data=api_data)

            # If there are not such Project in list of Projects

            if project_number == -1:
                print_line("No such project {0} in platform {1}.".format(api_data['project'], api_data['platform']))
                return False

            # It is OK, so run action

            return show_helper.action_show_set(api_data=api_data)

        # If action is Show Issues

        elif api_data['action'] == Actions.SHOW_ISSUES:
            if api_data['platform'] is None or \
                    api_data['platform'] == '':
                print_line('Empty platform name.')
                return False

             # Get number of Platform in list of Platforms

            platform_number = self.web_api.get_platform_number_by_name(api_data=api_data)

            # It there are not such Platform in list of Platforms

            if platform_number == -1:
                print_line("No such platform: {0}.".format(api_data['platform']))
                return False

            # If Project name is empty

            if api_data['project'] is None or \
                    api_data['project'] == '':
                print_line('Empty platform name.')
                return False

            # Get number of Project in list of Projects

            project_number = self.web_api.get_project_number_by_name(api_data=api_data)

            # If there are not such Project in list of Projects

            if project_number == -1:
                print_line("No such project {0} in platform {1}.".format(api_data['project'], api_data['platform']))
                return False

            # It is OK, so run action

            return show_helper.action_show_issues(api_data=api_data)

        return False

    # -------------------------------------------------------------------------
    # Delete Platform ot Project
    # -------------------------------------------------------------------------

    @staticmethod
    def action_delete_platform(api_data):
        """
        Run action: Delete defined Platform.
        :param api_data: api data set
        :return: result
        """

        platform_helper = PlatformHelper()

        return platform_helper.delete_platform(api_data=api_data)

    @staticmethod
    def action_delete_project(api_data):
        """
        Run action: Delete defined Project.
        :param api_data: api data set
        :return: result
        """
        project_helper = ProjectHelper()

        return project_helper.delete_project(api_data=api_data)

    # -------------------------------------------------------------------------
    # Archive Platform or Project
    # -------------------------------------------------------------------------

    @staticmethod
    def action_archive_platform(api_data):
        """
        Run action: Archive defined Platform.
        :param api_data: api data set
        :return: result
        """
        platform_helper = PlatformHelper()

        return platform_helper.archive_platform(api_data=api_data)

    @staticmethod
    def action_archive_project(api_data):
        """
        Run action: Archive defined Project.
        :param api_data: api data set
        :return: result
        """
        project_helper = ProjectHelper()

        return project_helper.archive_project(api_data=api_data)

    # -------------------------------------------------------------------------
    # Restore Platform or Project
    # -------------------------------------------------------------------------

    @staticmethod
    def action_restore_platform(api_data):
        """
        Run action: restore Platform from Archive.
        :param api_data: api data set
        :return: result
        """
        platform_helper = PlatformHelper()

        return platform_helper.restore_platform(api_data=api_data)

    @staticmethod
    def action_restore_project(api_data):
        """
        Run action: Restore Project from Archive.
        :param api_data: api data set
        :return: result
        """
        project_helper = ProjectHelper()

        return project_helper.restore_project(api_data=api_data)

    # -------------------------------------------------------------------------
    # Validators
    # -------------------------------------------------------------------------

    @staticmethod
    def validate_api_data_structure_is_ok(api_data):
        # type: (dict) -> bool
        """
        Validate api_data contents.
        :param api_data: api data set
        :return: result
        """

        # If app execute as python module - redefine OS parameteres

        if 'os_type' not in api_data:
            api_data['os_type'] = get_os_platform()

        if 'os_version' not in api_data:
            api_data['os_version'] = get_os_version(get_os_platform())

        if 'os_sp' not in api_data:
            api_data['os_sp'] = get_os_sp(get_os_platform())

        if 'os_release' not in api_data:
            api_data['os_release'] = get_os_release()

        if 'os_machine' not in api_data:
            api_data['os_machine'] = get_os_machine()

        # For login mode

        if 'auth_token' not in api_data:
            api_data['auth_token'] = None

        if api_data['auth_token'] is not None and api_data['auth_token'] != '':
            api_data['login_method'] = 'token'

        else:
            if (api_data['user'] is not None and api_data['user'] != '') and \
                    api_data['password'] is not None and api_data['password'] != '':
                api_data['login_method'] = 'username_and_password'

            else:
                api_data['login_method'] = 'config_file'

        # For targets

        if 'target' not in api_data:
            api_data['target'] = None

        if api_data['target'] is None:
            api_data['target'] = ''

        # For files

        if 'file' not in api_data:
            api_data['file'] = None

        if api_data['file'] is None:
            api_data['file'] = 'no'

        # For methods

        if 'method' not in api_data:
            api_data['method'] = None

        if api_data['method'] is None:
            api_data['method'] = Methods.AUTO

        # For formats

        if 'format' not in api_data:
            api_data['format'] = None

        if api_data['format'] is None:
            api_data['format'] = Formats.SYSTEM

        # For logging

        if 'logging' not in api_data:
            api_data['logging'] = None

        if api_data['logging'] is None:
            api_data['logging'] = 'off'

        # Define if targets more than one

        targets = api_data['target'].replace('[', '').replace(']', '').replace(' ', '').split(',')

        if len(targets) == 0:
            print_line('Wrong number of targets.')
            return False

        api_data['target'] = targets

        # Define if files more than one, if it is true - redefine files as list with length of targets

        files = api_data['file'].replace('[', '').replace(']', '').replace(' ', '').split(',')

        if len(targets) != len(files):
            print_line('Number of targets not equals number of files. For targets, '
                       'that do not require files - use "no".')
            print_line('For example: ... --target[os,req] '
                       '--file=no,/home/user/project/requirements.txt.')
            return False

        api_data['file'] = []

        for file in files:
            if file == 'no':
                api_data['file'].append(None)
            else:
                api_data['file'].append(file)

        # Clear components and packages lists

        api_data['components'] = []
        api_data['packages'] = []

        return True

    @staticmethod
    def validate_action_type_is_ok(api_data):
        """
        Check if action type, pointed in arguments match with template.
        :param api_data: api data set
        :return: result
        """

        if 'action' not in api_data:
            return False

        if api_data['action'] != Actions.SAVE_CONFIG and \
                api_data['action'] != Actions.CREATE_PLATFORM and \
                api_data['action'] != Actions.CREATE_PROJECT and \
                api_data['action'] != Actions.CREATE_SET and \
                api_data['action'] != Actions.SHOW_PLATFORMS and \
                api_data['action'] != Actions.SHOW_PROJECTS and \
                api_data['action'] != Actions.SHOW_SET and \
                api_data['action'] != Actions.SHOW_ISSUES and \
                api_data['action'] != Actions.DELETE_PLATFORM and \
                api_data['action'] != Actions.DELETE_PROJECT and \
                api_data['action'] != Actions.ARCHIVE_PLATFORM and \
                api_data['action'] != Actions.ARCHIVE_PROJECT and \
                api_data['action'] != Actions.RESTORE_PLATFORM and \
                api_data['action'] != Actions.RESTORE_PROJECT:
            return False

        return True

    # -------------------------------------------------------------------------
    # Config actions
    # -------------------------------------------------------------------------

    @staticmethod
    def save_config_to_file(api_data):
        """
        Save data into config fle in yaml format.
        :param api_data: api data set
        :return: result
        """

        # Default parameters for config file

        file_name = '.surepatch.yaml'
        file_path = os.path.expanduser('~')
        full_path = os.path.join(file_path, file_name)

        # Config template

        config = dict(
            team=api_data['team'],
            user=api_data['user'],
            password=api_data['password'],
            auth_token=api_data['auth_token'],
            logo=api_data['logo'],
            logging=api_data['logging']
        )

        # open config file

        with open(full_path, 'w') as yaml_config_file:
            try:
                yaml.dump(config, yaml_config_file)
                return True

            except yaml.YAMLError as yaml_exception:
                print_line('Config file save in yaml format exception: {0}.'.format(yaml_exception))
                return False

            finally:
                yaml_config_file.close()

    def load_config_from_file(self, api_data):
        """
        Load data from config file in yaml format.
        :param api_data: api data set
        :return: result
        """

         # Default parameters for config file

        file_name = '.surepatch.yaml'
        file_path = os.path.expanduser('~')
        full_path = os.path.join(file_path, file_name)

        # If file does not exist

        if not os.path.isfile(full_path):
            print_line('Config file does not exist: ~/{0}.'.format(file_name))
            print_line('Create config file first with parameter --action=save_config.')
            return False

        components_helper = ComponentsHelper()

        # Define config file encoding

        if components_helper.define_file_encoding(full_path) == 'undefined':
            print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
            return False

        # Open config file

        with open(full_path, 'r') as yaml_config_file:
            try:

                # Load config file contents in YAML format

                config = yaml.load(yaml_config_file)

                # Analyse config elements

                if 'team' not in config:
                    config['team'] = None

                api_data['team'] = config['team']

                if 'user' not in config:
                    config['user'] = None

                api_data['user'] = config['user']

                if 'password' not in config:
                    config['password'] = None

                api_data['password'] = config['password']

                if 'auth_token' not in config:
                    config['auth-token'] = None

                api_data['auth_token'] = config['auth_token']

                if 'logo' not in config:
                    config['logo'] = 'off'

                api_data['logo'] = config['logo']

                if 'logging' not in config:
                    config['logging'] = 'off'

                api_data['logging'] = config['logging']

                return True

            except yaml.YAMLError as yaml_exception:
                print_line('Get an exception while read config file: {0}.'.format(yaml_exception))
                return False

            finally:
                yaml_config_file.close()


class Actions(object):
    """Class for constant actions names.
    """

    SAVE_CONFIG = 'save_config'
    CREATE_PLATFORM = 'create_platform'
    CREATE_PROJECT = 'create_project'
    CREATE_SET = 'create_set'
    SHOW_PLATFORMS = 'show_platforms'
    SHOW_PROJECTS = 'show_projects'
    SHOW_SET = 'show_set'
    SHOW_ISSUES = 'show_issues'
    DELETE_PLATFORM = 'delete_platform'
    DELETE_PROJECT = 'delete_project'
    ARCHIVE_PLATFORM = 'archive_platform'
    ARCHIVE_PROJECT = 'archive_project'
    RESTORE_PLATFORM = 'restore_platform'
    RESTORE_PROJECT = 'restore_project'


class Targets(object):
    """Class for constant targets names.
    """

    OS = 'os'
    PIP = 'pip'
    PIP3 = 'pip3'
    REQ = 'req'
    REQ3 = 'req3'
    REQUIREMENTS = 'requirements'
    REQUIREMENTS3 = 'requirements3'
    NPM = 'npm'
    NPM_LOCAL = 'npm_local'
    PACKAGE_JSON = 'package_json'
    PACKAGE_LOCK_JSON = 'package_lock_json'
    GEM = 'gem'
    GEMFILE = 'gemfile'
    GEMFILE_LOCK = 'gemfile_lock'
    PHP_COMPOSER_JSON = 'php_composer_json'
    PHP_COMPOSER_LOCK = 'php_composer_lock'
    POM = 'pom'
    YARN = 'yarn'


class Methods(object):
    """Class for constant methods names.
    """

    AUTO = 'auto'
    MANUAL = 'manual'


class Formats(object):
    """Class for constant format names.
    """

    SYSTEM = 'system'
    USER = 'user'


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
