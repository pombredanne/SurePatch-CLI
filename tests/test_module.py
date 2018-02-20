#!/usr/bin/env python3
"""
Example launch CLI App as python module.
"""

import sys
import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from surepatch import surepatch_api

# Demo for surepatch execution as python module

login_data = dict()
if not surepatch_api.load_config_from_file(api_data=login_data):
    print('You have not config file ~/.surepatch.yaml. Create it, or fill parameters'
          'myteam, myname and mypassword directly in test_module.py code and comment sys.exit(0).')
    sys.exit(0)

myteam = login_data['team']
myname = login_data['user']
mypassword = login_data['password']

# myteam = 'team'
# myname = 'e-mail'
# mypassword = 'password'

myplatform = 'moduletest2'

demo_set = [
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_platform',
        platform=myplatform,
        description='Test for module'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='os_none',
        target='os',
        file='no'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='os_path',
        target='os',
        file='/Users/admin/packages_examples/mac_rep.txt'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='pip_none',
        target='pip',
        file='no'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='pip3_none',
        target='pip3',
        file='no'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='req_path',
        target='req',
        file='/Users/admin/packages_examples/requirements.txt'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='npm_none',
        target='npm',
        file='no'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='npm_local',
        target='npm_local',
        file='/Users/admin/packages_examples/'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='package_json',
        target='package_json',
        file='/Users/admin/packages_examples/package.json'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='package_lock',
        target='package_lock_json',
        file='/Users/admin/packages_examples/package-lock.json'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='gem_none',
        target='gem',
        file='no'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='gemfile',
        target='gemfile',
        file='/Users/admin/packages_examples/Gemfile'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='gemfile_lock',
        target='gemfile_lock',
        file='/Users/admin/packages_examples/Gemfile.lock'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='composer_json',
        target='php_composer_json',
        file='/Users/admin/packages_examples/composer1.json'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='composer_lock',
        target='php_composer_lock',
        file='/Users/admin/packages_examples/composer1.lock'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='pom',
        target='pom',
        file='/Users/admin/packages_examples/pom.xml'),
    dict(
        team=myteam,
        user=myname,
        password=mypassword,
        login_method='username_and_password',
        action='create_project',
        platform=myplatform,
        project='yarn',
        target='yarn',
        file='/Users/admin/packages_examples/yarn.lock')
]

for data in demo_set:
    if surepatch_api.run_action(api_data=data):
        print('OK')
    else:
        print('Error')
