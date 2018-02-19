#!/usr/bin/env python3
"""
Example launch CLI App as python module.
"""

import sys
import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from surepatch import surepatch_api


data = dict(
    team='dima',
    user='ws.bespalov@gmail.com',
    password='Test123!',
    login_method='username_and_password',
    action='create_project',
    platform='module',
    project='npm_none',
    description='Tests of module imports',
    target='npm'
)

if surepatch_api.run_action(api_data=data):
    print('OK')
else:
    print('Error')
