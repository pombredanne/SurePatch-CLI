#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main surepatch module
"""

# -------------------------------------------------------------------------
# Inputs
# -------------------------------------------------------------------------

import sys
import argparse

from core.api import API
from core.api import OSs
from core.api import Methods
from core.api import Formats
from core.interface import print_line
from core.interface import print_logo
from core.os_parameters import get_os_platform
from core.os_parameters import get_os_version
from core.os_parameters import get_os_sp
from core.os_parameters import get_os_release
from core.os_parameters import get_os_machine

# -------------------------------------------------------------------------
# Define main API
# -------------------------------------------------------------------------
surepatch_api = API()

# -------------------------------------------------------------------------
# Create command line parser
# -------------------------------------------------------------------------

def create_parser():
    """
    Create argument parser.
    :return: parser
    """

    parser = argparse.ArgumentParser(
        description="SurePatch Argument Parser")

    parser.add_argument(
        '--action',
        type=str,
        required=False,
        help='Define action: '
             'save_config, '
             'create_platform, '
             'create_project, '
             'create_set, '
             'show_platforms, '
             'show_projects, '
             'show_set, '
             'show_issues')

    parser.add_argument(
        '--file',
        type=str,
        required=False,
        help="Define file name")

    parser.add_argument(
        '--target',
        type=str,
        required=False,
        help="Define SurePatch target (os/pip/requirements/npm/"
             "packages_json/gem/gemlist/gemfile...)")

    parser.add_argument(
        '--method',
        type=str,
        required=False,
        help="Define packages collection mode (auto/manual/file)")

    parser.add_argument(
        '--format',
        type=str,
        required=False,
        help='Define file format (system/user)')

    parser.add_argument(
        '--team',
        type=str,
        required=False,
        help="Define your team")

    parser.add_argument(
        '--user',
        type=str,
        required=False,
        help="Define Username/email")

    parser.add_argument(
        '--password',
        type=str,
        required=False,
        help="Define Password")

    parser.add_argument(
        '--platform',
        type=str,
        required=False,
        help="Define Platform name")

    parser.add_argument(
        '--description',
        type=str,
        required=False,
        nargs='?',
        help="Define Project description")

    parser.add_argument(
        '--project',
        type=str,
        required=False,
        help="Define Project name")

    parser.add_argument(
        '--set',
        type=str,
        required=False,
        help='Define Set name. If is set None - \
            set name will be incremented automatically')

    parser.add_argument(
        '--auth_token',
        type=str,
        required=False,
        help='Define token from your web dashboard \
        to login without password')

    parser.add_argument(
        '--logo',
        type=str,
        required=False,
        help='Print logo or not (on/off)'
    )

    parser.add_argument(
        '--logging',
        type=str,
        required=False,
        help='Use log file or not (on/off)'
    )

    return parser.parse_args()


def main():
    """
    Application main function.
    :return: exit code
    """

    arguments = create_parser()

    # Collect app command line parameters into data set

    api_data = dict(
        action=arguments.action,
        team=arguments.team,
        user=arguments.user,
        password=arguments.password,
        file=arguments.file,
        target=arguments.target,
        method=arguments.method,
        format=arguments.format,
        platform=arguments.platform,
        description=arguments.description,
        project=arguments.project,
        set=arguments.set,
        os_type=get_os_platform(),
        os_version=get_os_version(get_os_platform()),
        os_sp=get_os_sp(get_os_platform()),
        os_release=get_os_release(),
        os_machine=get_os_machine(),
        components=[],
        auth_token=arguments.auth_token,
        logo=arguments.logo,
        logging=arguments.logging
    )

    if arguments.logo is not None:
        if arguments.logo == 'on':
            print_logo()

    # Run application with data set

    if surepatch_api.run_action(api_data=api_data):
        print_line('Complete successfully.')
        return 0
    else:
        print_line('Complete with errors.')
        return 1


if __name__ == '__main__':
    """
    Entry point
    """

    sys.exit(main())
