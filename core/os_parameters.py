"""Additional functions for OS info
"""

import sys
import platform

def get_os_platform():
    """
    Get OS platform type.
    :return: platform
    """

    if sys.platform == 'darwin' or platform.system() == 'Darwin':
        return OSs.MACOS
    if sys.platform == 'linux2' or sys.platform == 'linux':
        dist = platform.dist()[0]
        if 'debian' in dist:
            return OSs.DEBIAN
        if 'fedora' in dist:
            return OSs.FEDORA
        if 'Ubuntu' in dist or 'ubuntu' in dist:
            return OSs.UBUNTU
    if sys.platform == 'win32' or sys.platform == 'win64':
        return OSs.WINDOWS


def get_os_version(os_platform):
    """
    Get OS version.
    :param os_platform: os
    :return: result
    """
    if os_platform == 'windows':
        return platform.uname()[2]
    return ''


def get_os_sp(os_platform):
    """
    Get OS service pack (for Windows)
    :param os_platform: os
    :return: SP
    """

    if os_platform == 'windows':
        return platform.win32_ver()[2][2:]
    return ''


def get_os_release():
    """
    Get OS release.
    :return: release
    """

    return platform.release()


def get_os_machine():
    """
    Get OS machine code.
    :return: machine code
    """

    return platform.machine()

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