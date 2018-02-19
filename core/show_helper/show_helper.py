#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys

from core.interface import print_line
from core.interface import print_issues
from core.interface import print_platforms
from core.interface import print_projects
from core.interface import print_components
from core.components_helper.components_helper import ComponentsHelper
from core.webapi import WebAPI


class ShowHelper(object):

    def __init__(self):
        self.web_api = WebAPI()
        self.components_helper = ComponentsHelper()

    @staticmethod
    def action_show_platforms(api_data):
        # type: (dict) -> bool
        """
        Print existing platforms.
        :param api_data: api data set
        :return: result
        """
        platforms = []

        if 'organization' not in api_data:
            print_line('Organization info error.')
            return False

        if 'platforms' not in api_data['organization']:
            print_line('Platform info error.')
            return False

        if len(api_data['organization']['platforms']) == 0:
            print_line('You have not Platforms.')
            return False

        for platform in api_data['organization']['platforms']:
            platforms.append({'name': platform['name'], 'description': platform['description']})

        if 'file' not in api_data:
            api_data['file'] = None

        print_platforms(platforms=platforms, title="Platforms", filename=api_data['file'])

        return True

    def action_show_projects(self, api_data):
        # type: (dict) -> bool
        """
        Print existing project for defined Platform.
        :param api_data: api data set
        :return: result
        """
        projects = []

        if 'organization' not in api_data:
            print_line('Organization info error.')
            return False

        if 'platforms' not in api_data['organization']:
            print_line('Platform info error.')
            return False

        if len(api_data['organization']['platforms']) == 0:
            print_line('You have not Platforms.')
            return False

        platform_number = self.web_api.get_platform_number_by_name(api_data=api_data)

        if platform_number == -1:
            print_line("No such platform: {0}.".format(api_data['platform']))
            return False

        if len(api_data['organization']['platforms'][platform_number]['projects']) == 0:
            print_line('You have not Projects.')
            return False

        for project in api_data['organization']['platforms'][platform_number]['projects']:
            projects.append({'name': project['name'], 'description': 'default project'})

        if 'file' not in api_data:
            api_data['file'] = None

        print_projects(projects=projects, title=api_data['platform'], filename=api_data['file'])

        return True

    def action_show_set(self, api_data):
        # type: (dict) -> bool
        """
        Print current Component set for defined Platform/Project.
        :param api_data: api data set
        :return: result
        """
        my_set = self.components_helper.get_current_set_name(api_data=api_data)

        if my_set[0] is None:
            print_line('Get set name error.')
            return False

        print_line('Current component set: {0}.'.format(my_set[0]))

        components = self.components_helper.get_current_component_set(api_data=api_data)[0]['components']

        if components[0] is None:
            print_line('Get component set error.')
            return False

        if 'file' not in api_data:
            api_data['file'] = None

        print_components(components=components, title=api_data['platform'] + '/' + api_data['project'], filename=api_data['file'])

        return True

    def action_show_issues(self, api_data):
        # type: (dict) -> bool
        """
        Print current Issues tor defined Platform/Project.
        :param api_data: api data set
        :return: result
        """
        api_data['platform_number'] = self.web_api.get_platform_number_by_name(api_data=api_data)

        if api_data['platform_number'] == -1:
            print_line("No such platform: {0}.".format(api_data['platform']))
            return False

        api_data['project_number'] = self.web_api.get_project_number_by_name(api_data=api_data)

        if api_data['project_number'] == -1:
            print_line("No such project {0} in platform {1}.".format(api_data['project'], api_data['platform']))
            return False

        api_data['project_url'] = api_data['organization']['platforms'][api_data['platform_number']]['projects'][api_data['project_number']]['url']

        if not self.web_api.send_get_issues_request(api_data=api_data):
            print_line("Cant load issues for platform {0} and project {1}.".format(api_data['platform'], api_data['project']))
            return False

        issues = api_data['issues']

        printed_issues = []

        for issue in issues:
            printed_issues.append({'name': 'title', 'description': issue['title']})
            printed_issues.append({'name': 'component', 'description': issue['component']['name'] + ' - ' + issue['component']['version']})
            printed_issues.append({'name': 'description', 'description': issue['description']})
            printed_issues.append({'name': 'author', 'description': issue['author']})
            printed_issues.append({'name': 'status', 'description': issue['status']})
            printed_issues.append({'name': '\n', 'description': ''})

        if 'file' not in api_data:
            api_data['file'] = None

        print_issues(issues=printed_issues, title=api_data['platform'] + '/' + api_data['project'], filename=api_data['file'])

        return True

