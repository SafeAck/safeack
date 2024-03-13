"""
SafeAck CLI Utils
"""
from hashlib import blake2b
from uuid import uuid4

def generate_result_filename():
    '''
    Generates and returns filename compatible with safeack backend

    Args:
        None

    Returns:
        str: randomly generated str compatible with safeack backend
    '''
    return blake2b(uuid4().bytes, digest_size=32).hexdigest()
