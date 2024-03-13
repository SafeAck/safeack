"""
SafeAck CLI Utils
"""

from hashlib import blake2b
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
    return blake2b(uuid4().bytes, digest_size=32).hexdigest()


def get_package_version():
    '''Returns package current version

    Args:
        None

    Returns:
        String: current package version
    '''
    return get_distribution('safeack').version
