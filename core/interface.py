# -*- coding: utf-8 -*-
"""
Interface module.
"""
from __future__ import print_function

import os
import sys
import yaml
from textwrap import wrap
from terminaltables import AsciiTable

import logging

logger = logging.getLogger('surepatch')
logger.setLevel(logging.DEBUG)

log_file_name = '.surepatch.log'
log_file_path = os.path.expanduser('~')
log_full_path = os.path.join(log_file_path, log_file_name)

fh = logging.FileHandler(log_full_path)
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)

logging_enabled = False

config_file_name = '.surepatch.yaml'
config_file_path = os.path.expanduser('~')
config_full_path = os.path.join(config_file_path, config_file_name)

if os.path.isfile(config_full_path):
    with open(config_full_path, 'r') as yaml_config_file:
        try:
            config = yaml.load(yaml_config_file)
        except:
            config = dict()
            logging_enabled = False

        if 'logging' in config:
            if config['logging'] == 'on':
                logging_enabled = True
            else:
                logging_enabled = False
        else:
            logging_enabled = False

def print_logo():
    """
    Print SurePatch logo on the screen.
    """
    print('\n')
    print('+------------------------------------------------------------------------------------------------+')
    text = """
                     #####                       ######
                    #     # #    # #####  ###### #     #   ##   #####  ####  #    #
                    #       #    # #    # #      #     #  #  #    #   #    # #    #
                     #####  #    # #    # #####  ######  #    #   #   #      ######
                          # #    # #####  #      #       ######   #   #      #    #
                    #     # #    # #   #  #      #       #    #   #   #    # #    #
                     #####   ####  #    # ###### #       #    #   #    ####  #    #
                    (c) BrainBankers, 2018
     """
    print(text)
    print('+------------------------------------------------------------------------------------------------+')


def print_line(message):
    # type: (str) -> None
    """
    Print message on the screen.
    :param message: string message to print
    :return: None
    """
    print(message)
    if logging_enabled:
        logger.debug(message)


def print_table(elements, title=None, filename=None):
    # type: (list, str, str) -> None
    """
    Print information as ASCII Table.
    :param elements: list of printing elements
                     {'name': element_name, 'version': element_version}
                     or
                     {'name': element_name, 'description': element_description}
    :param title: title of Table
    :param filename: path to text file export
    :return: None
    """

    # If list of printing elements is not empty

    if len(elements) > 0:
        # For elements with 'version' field
        if 'version' in elements[0].keys():
            table_data = [
                ['Name', 'Version']]

            table = AsciiTable(table_data)
            table.padding_left = 1
            table.padding_right = 1

            max_width = 80

            if title is not None:
                table.title = title

            for element in elements:
                table_data.append(
                    [element['name'],
                     '\n'.join(wrap(element['version'], max_width))])

            print(table.table)

            if isinstance(filename, list):
                filename = filename[0]

            if filename is not None:
                try:
                    with open(filename, 'w') as fp:
                        fp.write(table.table)

                except IOError as ioerror_exception:
                    print_line("Exception {0} occured while write file {1}.".format(ioerror_exception, filename))

        # For elements with 'description' field
        elif 'description' in elements[0].keys():
            table_data = [
                ['Name', 'Description']]

            table = AsciiTable(table_data)
            table.padding_left = 1
            table.padding_right = 1

            max_width = 80

            if title is not None:
                table.title = title

            for element in elements:
                table_data.append(
                    [element['name'],
                     '\n'.join(wrap(element['description'], max_width))])

            print(table.table)

            if isinstance(filename, list):
                filename = filename[0]

            if filename is not None:
                try:
                    with open(filename, 'w') as fp:
                        fp.write(table.table)

                except IOError as ioerror_exception:
                    print_line("Exception {0} occured while write file {1}.".format(ioerror_exception, filename))

def print_components(components, title=None, filename=None):
    # type: (list, str, str) -> None
    """
    Print Component Set as ASCII Table
    :param components: list of components
    :param title: Table title
    :param filename: path to file
    :return: None
    """

    
    print_table(elements=components, title=title, filename=filename)


def print_platforms(platforms, title=None, filename=None):
    # type: (list, str, str) -> None
    """
    Print Platforms as ASCII Table
    :param platforms: list of platforms
    :param title: Table title
    :param filename: path to file
    :return: None
    """
    
    print_table(elements=platforms, title=title, filename=filename)


def print_projects(projects, title=None, filename=None):
    # type: (list, str, str) -> None
    """
    Print Projects as ASCII Table
    :param projects: list of projects
    :param title: Table title
    :param filename: path to file
    :return: None
    """

    print_table(elements=projects, title=title, filename=filename)


def print_issues(issues, title=None, filename=None):
    # type: (list, str, str) -> None
    """
    Print Issues as ASCII Table
    :param issues: list of issues
    :param title: Table title
    :param filename: path to file
    :return: None
    """

    print_table(elements=issues, title=title, filename=filename)


def ask(message):
    # type: (str) -> str
    """
    Ask user with unput. For python2 and python3 implementations
    :param message: message to show when ask
    :return: user input as str
    """
    if sys.version_info > (3, 0):
        # For Python 3
        return input(message)

    else:
        # For Python 2
        return raw_input(message)
