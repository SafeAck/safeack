"""
SafeAck Backend API client
"""
from requests import get as rget, post as rpost
from .logger import logger


class SafeAckClient:
    '''SafeAck Backend API Client'''

    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url
        self.timeout = 10
        self.__token = token

        self.is_valid = None
        self.__headers = {'Authorization': f"Bearer {self.__token}"}

    def is_token_valid(self) -> bool:
        '''
        Validates provided safeack backend token and
        sets `is_valid` value for further usage.
        Returns value of `is_valid` if its value
        already exists.

        Args:
            None

        Returns:
            bool: True if token is valid else False
        '''
        if self.is_valid is not None:
            return self.is_valid

        if not self.base_url or not self.__token:
            return False

        url = f'{self.base_url}/api/v1/scanner/auth-ping'
        res = rget(url=url, headers=self.__headers, timeout=self.timeout)
        res_json = res.json()

        self.is_valid = (
            res_json
            and res_json.get('msg') == 'Authentication successful'
            and res_json.get('status_code') == 200
        )

        return self.is_valid

    def push_s3_result_path_to_safeack_backend(self, s3_result_path: str) -> bool:
        '''
        Pushes AWS s3 result path to safeack backend

        Args:
            s3_result_path (str): s3 bucket object path where result is stored
                eg. s3://test/safeack-results/03ac6cafbea141e185570985c6316ad3.json

        Returns:
            bool: Returns True if path gets stored by backend else returns False.
        '''
        status = False

        if not self.is_valid:
            logger.error('Token is Invalid. Please provide new scanner token.')
        elif not s3_result_path:
            logger.error('s3_result_path is required')
        else:
            url = f"{self.base_url}/api/v1/scanner/results"
            body = {'s3_bucket_path': s3_result_path}
            res = rpost(
                url=url, headers=self.__headers, json=body, timeout=self.timeout
            )
            res_body = res.json()
            status = res_body.get('status_code', None) == 200
            logger.info('SafeAck Backend Result Upload Response: %s', res_body)

        return status
