#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Helper module.
"""


from core.interface import print_line
from core.components_helper.components_helper import ComponentsHelper
from core.webapi import WebAPI


class ProjectHelper(object):
    """
    Project Helper class.
    """

    def __init__(self):
        self.web_api = WebAPI()
        self.components_helper = ComponentsHelper()

    def create_project_validate(self, api_data):
        # type: (dict) -> bool
        """
        Run action: CREATE New Project in different cases.
        :return: result, modify api_data
        """

        # Validate Platform and Project parameters

        if 'platform' not in api_data:
            print_line('There are no --platform parameter given.')
            return False

        if 'project' not in api_data:
            print_line('There are no --platform parameter given.')
            return False

        if api_data['platform'] is None or api_data['platform'] == '':
            print_line('Empty platform name.')
            return False

        if api_data['project'] is None or api_data['project'] == '':
            print_line('Empty project name.')
            return False

        # Get Platforms

        platforms = self.get_my_platforms(api_data=api_data)

        if api_data['platform'] not in platforms:
            print_line("Platform {0} does not exists.".format(api_data['platform']))
            return False

        # Get Projects

        projects = self.get_my_projects(api_data=api_data)

        if api_data['project'] in projects:
            print_line("Project {0} already exists.".format(api_data['project']))
            return False

        # Normal output

        return True

    # Target = OS packages

    def collect_data_for_project_os_auto_system_none(self, api_data):
        # type: (dict) -> bool
        """
        Collect data from OS packages by shell command.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_os_auto_system_none(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_project_os_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Collect data from OS packages by shell command,
        stored in file, defined in path.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_os_auto_system_path(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    # Target = Python packages

    def collect_data_for_project_pip_auto_system_none(self, api_data):
        # type: (dict) -> bool
        """
        Collect Python PIP packages from shell command.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_pip_auto_system_none(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_data_for_project_pip_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Collect Python PIP packages from shell command,
        stored in file, defined in path.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_pip_auto_system_path(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_project_requirements_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Collect Python requirements.txt file, defined in path.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_requirements_auto_system_path(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    # Target = NodeJS NPM packages

    def collect_data_for_project_npm_auto_system_none(self, api_data):
        # type: (dict) -> bool
        """
        Collect NPM packages, collected from shell command (nmp list --json).
        Shell command runs global from root path.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_npm_auto_system_none(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_project_npm_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Collect NPM packages from shell command (npm list --json),
        stored in file, defined in path.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Got components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_npm_auto_system_path(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_project_npm_local_auto_system_none(self, api_data):
        # type: (dict) -> bool
        """
        Collect NPM packages from shell command (npm list --json).
        Shell command runs local from path, defined by --file parameter.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_npm_local_auto_system_none(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_project_package_lock_json_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Collect NPM packages from package-lock.json, defined by --file parameter.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_npm_lock_auto_system_path(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_project_package_json_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Collect NPM packages from package.json, defined by --file parameter.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_package_json_auto_system_path(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    # Target = Ruby packages

    def collect_data_for_project_gem_auto_system_none(self, api_data):
        # type: (dict) -> bool
        """
        Collect Ruby packages, collected from shell command.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_gem_auto_system_none(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_project_gem_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Collect Ruby packages from shell command and
        stored in gem list file, defined in --file parameter.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_gem_auto_system_path(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_project_gemfile_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Collect Ruby packages, collected from Gemfile, defined
        by --file parameter.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_gemfile_auto_system_path(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_project_gemfile_lock_auto_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Collect Ruby packages, collected from Gemfile.lock file,
        defined by --file parameter.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_gemfile_lock_auto_system_path(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_project_any_auto_user_path(self, api_data):
        # type: (dict) -> bool
        """
        Collect different packages, collected in file,
        defined by path with simple multiline format: name=version…
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_any_auto_user_path(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_project_any_manual_user_none(self, api_data):
        # type: (dict) -> bool
        """
        Collect different packages, asked in interactive mode.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_any_manual_user_none(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_project_php_composer_json_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Collect PHP packages from Composer.json file.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_php_composer_json_system_path(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_project_php_composer_lock_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Collect PHP packages from Composer.json file.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_php_composer_lock_system_path(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_project_maven_pom_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Collect packages with Maven pom.xml file
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components
        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_maven_pom(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def collect_data_for_project_yarn_lock_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Collect packages with yarn.lock file
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Get components

        components = api_data['components']
        api_data['components'] = []

        if self.components_helper.get_components_yarn_lock(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal output

            api_data['components'] = components
            return True

        # Otherwise

        return False

    def cllect_data_for_project_node_modules_system_path(self, api_data):
        # type: (dict) -> bool
        """
        Collect data for node_modules from file
        :param api_data: api data set
        :return: result
        """
        
        # Get components

        components = api_data['components']
        api_data['components']

        if self.components_helper.get_components_node_modules(api_data=api_data):
            for component in api_data['components']:
                components.append(component)

            # Normal utput

            api_data['components'] = components
            return True

        # Otherwise

        return False


    def delete_project(self, api_data):
        # type: (dict) -> bool
        """
        Run action: Delete defined Project.
        :param api_data: api data set
        :return: result
        """

        # Get Platform number

        api_data['platform_number'] = self.web_api.get_platform_number_by_name(api_data=api_data)

        if api_data['platform_number'] == -1:
            print_line("Platform {0} does not exist.".format(api_data['platform']))
            return False

        # Get Project number

        api_data['project_number'] = self.web_api.get_project_number_by_name(api_data=api_data)

        if api_data['project_number'] == -1:
            print_line("Project {0} does not exist.".format(api_data['project']))
            return False

        # Get Project ID

        api_data['project_id'] = api_data['organization']['platforms'][api_data['platform_number']]['projects'][api_data['project_number']]['id']

        # Send Delete request

        return self.web_api.send_delete_project_request(api_data=api_data)

    def archive_project(self, api_data):
        # type: (dict) -> bool
        """
        Run action: Archive defined Project.
        :param api_data: api data set
        :return: result
        """

        # get Platform number

        api_data['platform_number'] = self.web_api.get_platform_number_by_name(api_data=api_data)

        if api_data['platform_number'] == -1:
            print_line("Platform {0} does not exist.".format(api_data['platform']))
            return False

        # get Project number

        api_data['project_number'] = self.web_api.get_project_number_by_name(api_data=api_data)

        if api_data['project_number'] == -1:
            print_line("Project {0} does not exist.".format(api_data['project']))
            return False

        # Get parameters

        organization = api_data['organization']
        platforms = organization['platforms']
        platform = platforms[api_data['platform_number']]
        projects = platform['projects']
        project = projects[api_data['project_number']]
        project_id = project['id']
        project_url = project['url']
        api_data['project_id'] = project_id
        api_data['project_url'] = project_url

        # Send Archive request

        return self.web_api.send_archive_project_request(api_data=api_data)

    def restore_project(self, api_data):
        # type: (dict) -> bool
        """
        Run action: Restore Project from Archive.
        :param api_data:
        :return:
        """

        # Get Platform number

        if api_data['platform'] is None or api_data['platform'] == '':
            print_line('Empty platform name.')
            return False

        if api_data['project'] is None or api_data['project'] == '':
            print_line('Empty project name.')
            return False

        # Get archived projects

        if not self.web_api.send_get_archived_projects_request(api_data=api_data):
            print_line('There were errors in obtaining archived projects.')
            return False

        api_data['project_id'] = None
        api_data['project_url'] = None
        my_archived_project = dict()

        # Verify archived projects

        for archive_project in api_data['archive_projects']:
            if api_data['project'] == archive_project['name']:
                api_data['project_id'] = archive_project['_id']
                api_data['project_url'] = archive_project['url']
                my_archived_project = archive_project
                break

        if api_data['project_id']  is None:
            print_line("Not such project {0} in archive.".format(api_data['project']))
            return False

        if my_archived_project['platform_id']['name'] != api_data['platform']:
            print_line("Defined project {0} not in defined platform "
                       "{1}.".format(api_data['project'], api_data['platform']))
            return False

        # Sent Restore request

        return self.web_api.send_restore_project_request(api_data=api_data)

    @staticmethod
    def get_my_platforms(api_data):
        # type: (dict) -> list
        """
        Get platforms names as list.
        :param api_data: api data set
        :return: result
        """

        # Check organization and platforms

        if api_data['organization'] is None:
            return []

        if api_data['organization']['platforms'] is None:
            return []

        # Get Platform name

        platforms = []
        for platform in api_data['organization']['platforms']:
            platforms.append(platform['name'])

        return platforms

    def get_my_projects(self, api_data):
        # type: (dict) -> list
        """
        Get projects names as list.
        :param api_data: api data set
        :return: result
        """

        # Check organization and platforms

        if api_data['organization'] is None:
            return []

        if api_data['organization']['platforms'] is None:
            return []

        # Get Platform number

        platform_number = self.web_api.get_platform_number_by_name(api_data=api_data)

        if platform_number == -1:
            return []

        # Get Projects

        projects = []

        for project in api_data['organization']['platforms'][platform_number]['projects']:
            projects.append(project['name'])

        return projects
