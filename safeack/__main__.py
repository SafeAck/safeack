"""
SafeAck Main Module
"""

# stdlib package imports
from argparse import ArgumentParser
from datetime import datetime, UTC
from os.path import join as pjoin

# package imports
from offat.config_data_handler import validate_config_file_data
from offat.tester.tester_utils import generate_and_run_tests
from offat.parsers import create_parser
from offat.utils import read_yaml

# safeack package imports
from .aws import upload_file
from .logger import logger
from .utils import get_package_version


def banner():
    '''
    Prints SafeAck Banner
    '''
    print(
        r'''
 ,---.           ,---.         ,---.        ,--.
'   .-'  ,--,--./  .-' ,---.  /  O  \  ,---.|  |,-.
`.  `-. ' ,-.  ||  `-,| .-. :|  .-.  || .--'|     /
.-'    |\ '-'  ||  .-'\   --.|  | |  |\ `--.|  \  \
`-----'  `--`--'`--'   `----'`--' `--' `---'`--'`--'
                https://safeack.com
    '''
    )  # noqa: W291


def start():
    '''
    Starts cli tool
    '''
    banner()

    parser = ArgumentParser(prog='safeack')
    parser.add_argument(
        '-f',
        '--file',
        dest='fpath',
        type=str,
        help='path or url of openapi/swagger specification file',
        required=True,
    )
    parser.add_argument(
        '-v', '--version', action='version', version=f'%(prog)s {get_package_version()}'
    )
    parser.add_argument(
        '-rl',
        '--rate-limit',
        dest='rate_limit',
        help='API requests rate limit per second',
        type=float,
        default=60,
        required=False,
    )
    parser.add_argument(
        '-pr',
        '--path-regex',
        dest='path_regex_pattern',
        type=str,
        help='run tests for paths matching given regex pattern',
        required=False,
        default=None,
    )
    parser.add_argument(
        '-t',
        '--token',
        dest='token',
        type=str,
        help='HTTP requests headers that should be sent during testing eg: User-Agent: offat',
        required=True,
    )
    parser.add_argument(
        '-tdc',
        '--test-data-config',
        dest='test_data_config',
        help='YAML file containing user test data for tests',
        type=str,
        required=False,
    )
    parser.add_argument(
        '-b',
        '--bucket',
        dest='s3_bucket',
        type=str,
        help='AWS s3 bucket name',
        required=True,
    )
    parser.add_argument(
        '-h',
        '--host-url',
        dest='host',
        type=str,
        help='',
        required=True,
        default='http://localhost:8080',
    )

    args = parser.parse_args()

    # TODO: extract token and validate it
    token = args.token
    if not token:
        logger.error('token required to initiate scan!')
        exit(-1)

    # handle rate limiting options
    rate_limit = args.rate_limit

    # handle test user data config file
    test_data_config = args.test_data_config
    if test_data_config:
        test_data_config = read_yaml(args.test_data_config)
        test_data_config = validate_config_file_data(test_data_config)

    file_name = pjoin(
        'results', f'{datetime.now(UTC).strftime("%Y%m%d%H%M%S")}-safeack-result.json'
    )

    # parse args and run tests
    api_parser = create_parser(args.fpath)
    results = generate_and_run_tests(
        api_parser=api_parser,
        regex_pattern=args.path_regex_pattern,
        output_file=file_name,
        output_file_format='json',
        req_headers={'Authorization': f'Bearer {token}'},
        rate_limit=rate_limit,
        test_data_config=test_data_config,
        proxy=None,
    )
    if results:
        logger.info('Scan Completed: Results Found and Captured')
        s3_file_object = upload_file(
            file_name=file_name, bucket=args.s3_bucket, object_name=None
        )

        # TODO: push file object path to backend
    else:
        logger.error('Scan Completed: No Results Found')


if __name__ == '__main__':
    start()
