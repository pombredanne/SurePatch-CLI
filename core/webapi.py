# -*- coding: utf-8 -*-
"""
Module for server access via web requests.
"""

import json
import datetime
import requests

from core.interface import print_line


class WebAPI(object):
    """
    Web API for Surepatch CLI Application.
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) \
        Gecko/20100101 Firefox/45.0',
        'token': ''
    }

    # This route for Production server

    base_url_prod = "https://surepatch.com"

    # This route for Testing Beta server

    base_url_dev = "https://beta.surepatch.net"

    api_url = '/api'

    # URL block

    login_url = api_url + "/auth/login"
    login_token_url = api_url + "/auth/token/login"
    organization_url = api_url + "/organization"
    platform_url = api_url + "/platforms"
    project_url = api_url + "/projects"
    issues_url = api_url + "/projects/partial"
    components_url = api_url + "/components"

    # Payload templates block

    login_payload = dict(
        username=None,
        password=None,
        referalToken=None,
        organization=None)

    platform_payload = dict(
        name='',
        description='')

    project_payload = dict(
        platform_id='',
        parent=None,
        project_url=None,
        project_id=None,
        required_right='manage_projects',
        name='',
        denied_if_unpaid=True,
        logo=None,
        components=[])

    components_payload = dict(
        set_name='0.0.0',
        components=[],
        project_url=None)

    issues_payload = dict()

    def get_request_url(self, server, url):
        # type: (str, str) -> str
        """
        Get request url, depends from server type: dev or prod
        :param server: dev or prod server string
        :param url: url to join
        :return: joined url
        """
        print_line('Send request to "{}" server...'.format(server))
        if server == 'prod':
            return self.base_url_prod + url
        else:
            return self.base_url_dev + url


    def send_login_token_request(self, api_data):
        # type: (dict) -> bool
        """
        Send login request with auth token to Surepatch server
        :param api_data: api data set
        :return: result
        """

        # Complete payload

        self.login_payload['authToken'] = api_data['auth_token']
        self.login_payload['org_domain'] = api_data['team']

        # Send request for login with auth token

        try:
            response = requests.post(
                url=self.get_request_url(api_data['server'], self.login_token_url),
                headers=self.headers,
                json=self.login_payload)

            if response.status_code == 200:
                # Login success - response code 200
                try:
                    text = response.text
                    login_response_text = json.loads(text)
                    api_data['token'] = login_response_text['token']
                    api_data['user_id'] = login_response_text['userID']
                    api_data['org_id'] = login_response_text['orgID']
                    api_data['organization'] = None
                    print_line('Login success.')
                    return True

                except ValueError as json_value_exception:
                    print_line('Response JSON parsing exception: '
                               '{0}'.format(json_value_exception))
                    return False

            # Otherwise

            print_line('Login failed. Status code: {0}'.format(response.status_code))
            return False

        except requests.exceptions.HTTPError as http_exception:
            print_line('HTTP Error: {0}'.format(http_exception))
            return False

        except requests.exceptions.ConnectionError as connection_exception:
            print_line('Connection error: {0}'.format(connection_exception))
            return False

        except requests.exceptions.Timeout as timeout_exception:
            print_line('Connection timeout: {0}'.format(timeout_exception))
            return False

        except requests.exceptions.RequestException as request_exception:
            print_line('Request exception: {0}'.format(request_exception))
            return False

    def send_login_user_password_request(self, api_data):
        # type: (dict) -> bool
        """
        Send login request with username and password to Surepatch server.
        :param api_data: api data set
        :return: result
        """

        # Complete payload

        self.login_payload['username'] = api_data['user']
        self.login_payload['password'] = api_data['password']
        self.login_payload['referalToken'] = None
        self.login_payload['organization'] = api_data['team']

        # Send request for login with auth team/user/password

        try:
            response = requests.post(
                url=self.get_request_url(api_data['server'], self.login_url),
                headers=self.headers,
                json=self.login_payload)

            if response.status_code == 200:
                # Login success - response code 200
                try:
                    text = response.text
                    login_response_text = json.loads(text)

                    # Get session token from response

                    if 'token' in login_response_text:
                        api_data['token'] = login_response_text['token']
                    else:
                        api_data['token'] = None
                        print_line('It seems that you have enabled two-factor authentication.')
                        print_line('CLI App does not support login/password with enabled MFA.')
                        print_line('To obtain auth token, please visit surepatch.com, '
                                   'login, go to Profile page.')
                        print_line('For successfull login in this case, use auth token '
                                   'in parameters or config file.')
                        return False

                    # Get user ID from response

                    if 'userID' in login_response_text:
                        api_data['user_id'] = login_response_text['userID']
                    else:
                        api_data['user_id'] = None

                    # Get organization ID from response

                    if 'orgID' in login_response_text:
                        api_data['org_id'] = login_response_text['orgID']
                    else:
                        api_data['org_id'] = None

                    api_data['organization'] = None
                    print_line('Login success.')
                    return True

                except ValueError as json_value_exception:
                    print_line('Response JSON parsing exception: '
                               '{0}'.format(json_value_exception))
                    return False

            # Otherwise

            print_line('Login failed. Status code: {0}'.format(response.status_code))
            return False

        except requests.exceptions.HTTPError as http_exception:
            print_line('HTTP Error: {0}'.format(http_exception))
            return False

        except requests.exceptions.ConnectionError as connection_exception:
            print_line('Connection error: {0}'.format(connection_exception))
            return False

        except requests.exceptions.Timeout as timeout_exception:
            print_line('Connection timeout: {0}'.format(timeout_exception))
            return False

        except requests.exceptions.RequestException as request_exception:
            print_line('Request exception: {0}'.format(request_exception))
            return False

    def send_get_organization_parameters_request(self, api_data):
        # type: (dict) -> bool
        """
        Send special request to Surepatch server to get Organization information.
        :param api_data: api data set
        :return: result
        """

        # Complete payload

        self.headers['token'] = api_data['token']

        # Send request to get the organization parameters

        try:
            response = requests.get(
                url=self.get_request_url(api_data['server'], self.organization_url),
                headers=self.headers)

            if response.status_code == 200:
                # Request success - response code 200
                try:
                    text = response.text
                    organization_data = json.loads(text)[0]

                    # Complete organization structure in data set

                    api_data['organization'] = dict()
                    api_data['organization']['_id'] = organization_data.get('_id', '')
                    api_data['organization']['name'] = organization_data.get('name', '')
                    api_data['organization']['token'] = organization_data.get('token', '')
                    api_data['organization']['url'] = organization_data.get('url', '')
                    api_data['organization']['stripe_id'] = organization_data.get('stripe_id', '')
                    api_data['organization']['team_plan_id'] = organization_data.get('team_plan_id', '')
                    api_data['organization']['all_projects'] = organization_data.get('allProjects', '')

                    owner_id = dict()
                    owner_id = organization_data.get('owner_id', {})
                    api_data['organization']['ownerID'] = owner_id.get('_id', '')
                    api_data['organization']['username'] = owner_id.get('username', '')
                    api_data['organization']['first_name'] = owner_id.get('firstname', '')
                    api_data['organization']['last_name'] = owner_id.get('lastname', '')
                    api_data['organization']['token_expires'] = owner_id.get('tokenExpires', '')
                    api_data['organization']['password_expires'] = owner_id.get('passwordExpires', '')
                    api_data['organization']['private_key'] = owner_id.get('privateKey', '')
                    api_data['organization']['connection_id'] = owner_id.get('connectionID', '')
                    api_data['organization']['version'] = owner_id.get('__v', '')
                    api_data['organization']['password'] = owner_id.get('password', '')
                    api_data['organization']['github'] = owner_id.get('github', '')
                    api_data['organization']['notifications'] = owner_id.get('notifications', '')
                    api_data['organization']['TFA'] = owner_id.get('TFA', '')
                    api_data['organization']['open_key'] = owner_id.get('openKey', '')
                    api_data['organization']['blocked_till'] = owner_id.get('blockedTill', '')
                    api_data['organization']['failed_attempts'] = owner_id.get('failedAttempts', '')
                    api_data['organization']['updated'] = owner_id.get('updated', '')
                    api_data['organization']['super'] = owner_id.get('super', '')
                    api_data['organization']['last_passwords'] = owner_id.get('lastPasswords', '')

                    api_data['organization']['platforms'] = list()
                    platforms = list()
                    platforms = organization_data.get('platforms', [])

                    for platform_data in platforms:
                        platform = dict()
                        platform['id'] = platform_data.get('_id', '')
                        platform['name'] = platform_data.get('name', '')
                        platform['description'] = platform_data.get('description', '')
                        platform['url'] = platform_data.get('url', '')
                        platform['version'] = platform_data.get('__v', '')
                        platform['projects'] = list()


                        for project_data in platform_data['projects']:
                            project = dict()
                            project['id'] = project_data.get('_id', '')
                            project['name'] = project_data.get('name', '')
                            project['logo'] = project_data.get('logo', '')
                            project['organization_id'] = project_data.get('organization_id', '')
                            project['platform_id'] = project_data.get('platform_id', '')
                            project['current_component_set'] = project_data.get('current_component_set', list())
                            project['token'] = project_data.get('token', '')
                            project['url'] = project_data.get('url', '')
                            project['version'] = project_data.get('__v', '')
                            project['updated'] = project_data.get('updated', '')
                            project['created'] = project_data.get('created', '')
                            project['issues'] = project_data.get('issues', list())
                            project['component_set_history'] = project_data.get('component_set_history', list())
                            project['child_projects'] = project_data.get('child_projects', list())
                            project['parent_projects'] = project_data.get('parent_projects', list())

                            platform['projects'].append(project)

                        api_data['organization']['platforms'].append(platform)


                    return True

                except ValueError as json_value_exception:
                    print_line('Response JSON parsing exception: '
                               '{0}'.format(json_value_exception))
                    return False

            # Otherwise

            print_line('Get organization parameters failed. Status code: '
                       '{0}'.format(response.status_code))
            return False

        except requests.exceptions.HTTPError as http_exception:
            print_line('HTTP Error: {0}'.format(http_exception))
            return False

        except requests.exceptions.ConnectionError as connection_exception:
            print_line('Connection error: {0}'.format(connection_exception))
            return False

        except requests.exceptions.Timeout as timeout_exception:
            print_line('Connection timeout: {0}'.format(timeout_exception))
            return False

        except requests.exceptions.RequestException as request_exception:
            print_line('Request exception: {0}'.format(request_exception))
            return False

    def send_create_new_platform_request(self, api_data):
        # type: (dict) -> bool
        """
        Send request to Surepatch server to create new Platform.
        :param api_data: api data set
        :return: result
        """

        # Complete payload

        self.headers['token'] = api_data['token']
        self.platform_payload['name'] = api_data['platform']
        self.platform_payload['description'] = api_data['description']

        try:
            response = requests.post(
                url=self.get_request_url(api_data['server'], self.platform_url),
                headers=self.headers,
                json=self.platform_payload)

            if response.status_code == 200:
                # Request success - response code 200
                print_line('Platform {0} was created successfully.'.format(api_data['platform']))
                return True

            # Otherwise

            print_line('Create platform failed. Status code: '
                       '{0}'.format(response.status_code))
            return False

        except requests.exceptions.HTTPError as http_exception:
            print_line('HTTP Error: {0}'.format(http_exception))
            return False

        except requests.exceptions.ConnectionError as connection_exception:
            print_line('Connection error: {0}'.format(connection_exception))
            return False

        except requests.exceptions.Timeout as timeout_exception:
            print_line('Connection timeout: {0}'.format(timeout_exception))
            return False

        except requests.exceptions.RequestException as request_exception:
            print_line('Request exception: {0}'.format(request_exception))
            return False

    def send_create_new_project_request(self, api_data):
        # type: (dict) -> bool
        """
        Send request to Surepatch server to create new Project.
        :param api_data: api data set
        :return: result
        """

        # Complete payload

        self.headers['token'] = api_data['token']
        self.project_payload['name'] = api_data['project']
        self.project_payload['platform_id'] = self.get_platform_id_by_name(api_data=api_data)
        self.project_payload['components'] = api_data['components']

        try:
            response = requests.post(
                url=self.get_request_url(api_data['server'], self.project_url),
                headers=self.headers,
                json=self.project_payload)

            if response.status_code == 200:
                # Request success - response code 200
                print_line('Project {0} was created successfully.'.format(api_data['project']))
                return True

            # Otherwise

            print_line('Create project failed. Status code: '
                       '{0}'.format(response.status_code))
            return False

        except requests.exceptions.HTTPError as http_exception:
            print_line('HTTP Error: {0}'.format(http_exception))
            return False

        except requests.exceptions.ConnectionError as connection_exception:
            print_line('Connection error: {0}'.format(connection_exception))
            return False

        except requests.exceptions.Timeout as timeout_exception:
            print_line('Connection timeout: {0}'.format(timeout_exception))
            return False

        except requests.exceptions.RequestException as request_exception:
            print_line('Request exception: {0}'.format(request_exception))
            return False

    def send_create_new_component_set_request(self, api_data):
        # type: (dict) -> bool
        """
        Send request to Surepatch server to create new Component Set.
        :param api_data: api data set
        :return:
        """

        # Complete payload

        self.headers['token'] = api_data['token']
        self.components_payload['set_name'] = api_data['set']
        self.components_payload['project_url'] = api_data['project_url']
        self.components_payload['components'] = api_data['components']

        try:
            response = requests.post(
                url=self.get_request_url(api_data['server'], self.components_url),
                headers=self.headers,
                json=self.components_payload)

            if response.status_code == 200:
                # Request success - response code 200
                print_line('Component set {0} was created successfully.'.format(api_data['set']))
                return True

            # Otherwise

            print_line('Create component set failed. Status code: '
                       '{0}'.format(response.status_code))
            return False

        except requests.exceptions.HTTPError as http_exception:
            print_line('HTTP Error: {0}'.format(http_exception))
            return False

        except requests.exceptions.ConnectionError as connection_exception:
            print_line('Connection error: {0}'.format(connection_exception))
            return False

        except requests.exceptions.Timeout as timeout_exception:
            print_line('Connection timeout: {0}'.format(timeout_exception))
            return False

        except requests.exceptions.RequestException as request_exception:
            print_line('Request exception: {0}'.format(request_exception))
            return False

    def send_delete_platform_request(self, api_data):
        # type: (dict) -> bool
        """
        Send request to delete Platform.
        :param api_data: api data set
        :return: result
        """

        # Complete payload
        self.headers['token'] = api_data['token']

        try:
            response = requests.delete(
                url=self.get_request_url(api_data['server'], self.platform_url + '/' + str(api_data['platform_id'])),
                headers=self.headers,
                json=self.platform_payload)

            if response.status_code == 200:
                # Request success - response code 200
                print_line('Platform {0} was deleted successfully.'.format(api_data['platform']))
                return True

            # Otherwise

            print_line('Delete Platform failed. Status code: '
                       '{0}'.format(response.status_code))
            return False

        except requests.exceptions.HTTPError as http_exception:
            print_line('HTTP Error: {0}'.format(http_exception))
            return False

        except requests.exceptions.ConnectionError as connection_exception:
            print_line('Connection error: {0}'.format(connection_exception))
            return False

        except requests.exceptions.Timeout as timeout_exception:
            print_line('Connection timeout: {0}'.format(timeout_exception))
            return False

        except requests.exceptions.RequestException as request_exception:
            print_line('Request exception: {0}'.format(request_exception))
            return False

    def send_delete_project_request(self, api_data):
        # type: (dict) -> bool
        """
        Send request to delete Project.
        :param api_data: api data set
        :return: result
        """

        # Complete payload

        self.headers['token'] = api_data['token']

        try:
            response = requests.delete(
                url=self.get_request_url(api_data['server'], self.project_url + '/' + str(api_data['project_id'])),
                headers=self.headers,
                json=self.project_payload)

            if response.status_code == 200:
                # Request success - response code 200
                print_line('Project {0} was deleted successfully.'.format(api_data['project']))
                return True

            # Otherwise

            print_line('Delete Project failed. Status code: '
                       '{0}'.format(response.status_code))
            return False

        except requests.exceptions.HTTPError as http_exception:
            print_line('HTTP Error: {0}'.format(http_exception))
            return False

        except requests.exceptions.ConnectionError as connection_exception:
            print_line('Connection error: {0}'.format(connection_exception))
            return False

        except requests.exceptions.Timeout as timeout_exception:
            print_line('Connection timeout: {0}'.format(timeout_exception))
            return False

        except requests.exceptions.RequestException as request_exception:
            print_line('Request exception: {0}'.format(request_exception))
            return False

    def send_archive_platform_request(self, api_data):
        # type: (dict) -> bool
        """
        Send request to archive Platform.
        :param api_data: api data set
        :return: result
        """

        # Complete payload

        self.headers['token'] = api_data['token']
        self.platform_payload = dict(
            newPlatform=dict(
                id=api_data['platform_id'],
                url=api_data['platform_url'],
                options=dict(
                    updated=datetime.datetime.now().isoformat() + 'Z',
                    state='archive',
                    archivedBy=api_data['user'])))

        try:
            response = requests.put(
                url=self.get_request_url(api_data['server'], self.platform_url),
                headers=self.headers,
                json=self.platform_payload)

            if response.status_code == 200:
                # Request success - response code 200
                print_line('Platform {0} was archived successfully.'.format(api_data['platform']))
                return True

            # Otherwise

            print_line('Archive Platform failed. Status code: '
                       '{0}'.format(response.status_code))
            return False

        except requests.exceptions.HTTPError as http_exception:
            print_line('HTTP Error: {0}'.format(http_exception))
            return False

        except requests.exceptions.ConnectionError as connection_exception:
            print_line('Connection error: {0}'.format(connection_exception))
            return False

        except requests.exceptions.Timeout as timeout_exception:
            print_line('Connection timeout: {0}'.format(timeout_exception))
            return False

        except requests.exceptions.RequestException as request_exception:
            print_line('Request exception: {0}'.format(request_exception))
            return False

    def send_archive_project_request(self, api_data):
        # type: (dict) -> bool
        """
        Send request to archive Project.
        :param api_data: api data set
        :return: result
        """

        # Complete payload
        self.headers['token'] = api_data['token']
        self.project_payload['options'] = dict(
            newProject=dict(
                id=api_data['project_id'],
                url=api_data['project_url'],
                options=dict(
                    updated=datetime.datetime.now().isoformat() + 'Z',
                    state='archive',
                    archivedBy=api_data['user'])))

        try:
            response = requests.put(
                url=self.get_request_url(api_data['server'], self.project_url),
                headers=self.headers,
                json=self.project_payload)

            if response.status_code == 200:
                # Request success - response code 200
                print_line('Project {0} was archived successfully.'.format(api_data['project']))
                return True

            print_line('Archive Project failed. Status code: '
                       '{0}'.format(response.status_code))
            return False

        except requests.exceptions.HTTPError as http_exception:
            print_line('HTTP Error: {0}'.format(http_exception))
            return False

        except requests.exceptions.ConnectionError as connection_exception:
            print_line('Connection error: {0}'.format(connection_exception))
            return False

        except requests.exceptions.Timeout as timeout_exception:
            print_line('Connection timeout: {0}'.format(timeout_exception))
            return False

        except requests.exceptions.RequestException as request_exception:
            print_line('Request exception: {0}'.format(request_exception))
            return False

    def send_restore_platform_request(self, api_data):
        # type: (dict) -> bool
        """
        Send request to restore defined Platform from archive.
        :param api_data:
        :return:
        """

        # Complete payload

        self.headers['token'] = api_data['token']
        self.platform_payload = dict(
            newPlatform=dict(
                id=api_data['platform_id'],
                url=api_data['platform_url'],
                options=dict(
                    updated=datetime.datetime.now().isoformat() + 'Z',
                    state='open',
                    archived=None)))

        try:
            response = requests.put(
                url=self.get_request_url(api_data['server'], self.platform_url),
                headers=self.headers,
                json=self.platform_payload)

            if response.status_code == 200:
                # Request success - response code 200
                print_line('Platform {0} was restored successfully.'.format(api_data['platform']))
                return True

            # Otherwise

            print_line('Restore Platform failed. Status code: '
                       '{0}'.format(response.status_code))
            return False

        except requests.exceptions.HTTPError as http_exception:
            print_line('HTTP Error: {0}'.format(http_exception))
            return False

        except requests.exceptions.ConnectionError as connection_exception:
            print_line('Connection error: {0}'.format(connection_exception))
            return False

        except requests.exceptions.Timeout as timeout_exception:
            print_line('Connection timeout: {0}'.format(timeout_exception))
            return False

        except requests.exceptions.RequestException as request_exception:
            print_line('Request exception: {0}'.format(request_exception))
            return False

    def send_restore_project_request(self, api_data):
        # type: (dict) -> bool
        """
        Send request to restore defined Project from archive.
        :param api_data: api data set
        :return: result
        """

        # Complete payload

        self.headers['token'] = api_data['token']
        self.project_payload = dict(
            newProject=dict(
                id=api_data['project_id'],
                url=api_data['project_url'],
                options=dict(
                    updated=datetime.datetime.now().isoformat() + 'Z',
                    state='open',
                    archived=None)))

        try:
            response = requests.put(
                url=self.get_request_url(api_data['server'], self.project_url),
                headers=self.headers,
                json=self.project_payload)

            if response.status_code == 200:
                # Request success - response code 200
                print_line('Project {0} was restored successfully.'.format(api_data['project']))
                return True

            print_line('Restore Project failed. Status code: '
                       '{0}'.format(response.status_code))
            return False

        except requests.exceptions.HTTPError as http_exception:
            print_line('HTTP Error: {0}'.format(http_exception))
            return False

        except requests.exceptions.ConnectionError as connection_exception:
            print_line('Connection error: {0}'.format(connection_exception))
            return False

        except requests.exceptions.Timeout as timeout_exception:
            print_line('Connection timeout: {0}'.format(timeout_exception))
            return False

        except requests.exceptions.RequestException as request_exception:
            print_line('Request exception: {0}'.format(request_exception))
            return False

    def send_get_archived_platforms_request(self, api_data):
        # type: (dict) -> bool
        """
        Send request to get all archived platforms.
        :param api_data: api data set
        :return: result
        """

        # Complete payload

        self.headers['token'] = api_data['token']

        try:
            response = requests.get(
                url=self.get_request_url(api_data['server'],
                                         self.platform_url + '/archive/' + api_data['organization']['_id']),
                headers=self.headers,
                json=self.platform_payload)

            api_data['archive_platforms'] = None

            if response.status_code == 200:
                # Request success - response code 200
                try:
                    text = response.text
                    api_data['archive_platforms'] = json.loads(text)
                    return True

                except json.JSONDecodeError as json_decode_error:
                    print_line('An exception occured with json decoder: '
                               '{0}.'.format(json_decode_error))
                    return False

            # Otherwise

            print_line('Archive Platform get information failed. '
                       'Status code: {0}'.format(response.status_code))
            return False

        except requests.exceptions.HTTPError as http_exception:
            print_line('HTTP Error: {0}'.format(http_exception))
            return False

        except requests.exceptions.ConnectionError as connection_exception:
            print_line('Connection error: {0}'.format(connection_exception))
            return False

        except requests.exceptions.Timeout as timeout_exception:
            print_line('Connection timeout: {0}'.format(timeout_exception))
            return False

        except requests.exceptions.RequestException as request_exception:
            print_line('Request exception: {0}'.format(request_exception))
            return False

    def send_get_archived_projects_request(self, api_data):
        # type: (dict) -> bool
        """
        Send request to get all archived projects.
        :param api_data: api data set
        :return: result, modify api_data
        """

        # Complete payload

        self.headers['token'] = api_data['token']

        try:
            response = requests.get(
                url=self.get_request_url(api_data['server'],
                                         self.project_url + '/archive/' + api_data['organization']['id']),
                headers=self.headers,
                json=self.project_payload)

            api_data['archive_projects'] = None

            if response.status_code == 200:
                # Request success - response code 200
                try:
                    text = response.text
                    api_data['archive_projects'] = json.loads(text)
                    return True

                except json.JSONDecodeError as json_decode_error:
                    print_line('An exception occured with json decoder: '
                               '{0}.'.format(json_decode_error))
                    return False

            # Otherwise

            print_line('Archive Project get information failed. '
                       'Status code: {0}'.format(response.status_code))
            return False

        except requests.exceptions.HTTPError as http_exception:
            print_line('HTTP Error: {0}'.format(http_exception))
            return False

        except requests.exceptions.ConnectionError as connection_exception:
            print_line('Connection error: {0}'.format(connection_exception))
            return False

        except requests.exceptions.Timeout as timeout_exception:
            print_line('Connection timeout: {0}'.format(timeout_exception))
            return False

        except requests.exceptions.RequestException as request_exception:
            print_line('Request exception: {0}'.format(request_exception))
            return False

    def send_get_issues_request(self, api_data):
        # type: (dict) -> bool
        """
        Send request to get Issues.
        :param api_data:
        :return:
        """

        # Complete payload

        self.headers['token'] = api_data['token']

        try:
            response = requests.post(
                url=self.get_request_url(api_data['server'], self.issues_url + '/' + api_data['project_url']),
                headers=self.headers,
                json=self.issues_payload)

            api_data['archive_projects'] = None

            if response.status_code == 200:
                # Request success - response code 200
                try:
                    content = response.content.decode("utf-8")
                    api_data['issues'] = json.loads(content)['project']['issues']
                    return True

                except json.JSONDecodeError as json_decode_error:
                    print_line('An exception occured with json decoder: '
                               '{0}.'.format(json_decode_error))
                    return False

            # Otherwise

            print_line('Archive Project get information failed. Status code: '
                       '{0}'.format(response.status_code))
            return False

        except requests.exceptions.HTTPError as http_exception:
            print_line('HTTP Error: {0}'.format(http_exception))
            return False

        except requests.exceptions.ConnectionError as connection_exception:
            print_line('Connection error: {0}'.format(connection_exception))
            return False

        except requests.exceptions.Timeout as timeout_exception:
            print_line('Connection timeout: {0}'.format(timeout_exception))
            return False

        except requests.exceptions.RequestException as request_exception:
            print_line('Request exception: {0}'.format(request_exception))
            return False

    @staticmethod
    def get_platform_id_by_name(api_data):
        # type: (dict) -> int
        """
        Get platform ID by its name.
        :param api_data: api data set
        :return: result
        """
        platform_name = api_data['platform']
        for platform in api_data['organization']['platforms']:
            if platform['name'] == platform_name:
                return platform['id']
        return -1

    @staticmethod
    def get_platform_number_by_name(api_data):
        # type: (dict) -> int
        """
        Get Platform number in list by its name.
        :param api_data: api data set
        :return:result
        """

        platform_name = api_data['platform']
        for index, platform in enumerate(api_data['organization']['platforms']):
            if platform['name'] == platform_name:
                return index
        return -1

    def get_project_number_by_name(self, api_data):
        # type: (dict) -> int
        """
        Get project number (index) by its name.
        :param api_data: api data set
        :return: result
        """

        project_name = api_data['project']
        platform_number = self.get_platform_number_by_name(api_data=api_data)
        for index, project in enumerate(api_data['organization']['platforms'][platform_number]['projects']):
            if project['name'] == project_name:
                return index
        return -1
