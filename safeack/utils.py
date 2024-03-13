"""
SafeAck CLI Utils
"""
from uuid import uuid4

from pkg_resources import get_distribution


def generate_result_filename():
    '''
    Generates and returns filename compatible with safeack backend

    Args:
        None

    Returns:
        str: randomly generated str compatible with safeack backend
    '''
    return uuid4().hex


def get_package_version():
    '''Returns package current version

    Args:
        None

    Returns:
        String: current package version
    '''
    return get_distribution('safeack').version
