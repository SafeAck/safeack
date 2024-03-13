"""
AWS utils
"""

from sys import exc_info

from boto3 import client
from botocore.exceptions import ClientError
from offat.logger import logger

from .utils import generate_result_filename


def upload_file(file_name, bucket, object_name=None) -> str:
    """Upload a file to an S3 bucket

    Args:
        file_name (str): File to upload on local machine
        bucket (str): Bucket to upload to
        object_name (str): S3 object name. If not specified then file_name is used

    Returns:
        str: s3 path of uploaded file (if str is empty then upload was failed)
    """
    s3_file_path = ''

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = f'results/{generate_result_filename()}.json'

    # Upload the file
    logger.info('Uploading result file to s3 bucket')
    try:
        client('s3').upload_file(file_name, bucket, object_name)
        logger.info(
            'File %s uploaded successfully to s3://%s/%s',
            file_name,
            bucket,
            object_name,
        )
    except ClientError as e:
        logger.error(
            'Failed to upload file %s to s3://%s/%s; Due to error: %s',
            file_name,
            bucket,
            object_name,
            e,
            exc_info=exc_info(),
        )

    return s3_file_path
