"""
SafeAck Main Module
"""
# stdlib package imports
from argparse import ArgumentParser
from os.path import join as pjoin

# package imports
from offat.config_data_handler import validate_config_file_data
from offat.tester.tester_utils import generate_and_run_tests
from offat.parsers import create_parser
from offat.utils import headers_list_to_dict, read_yaml

# safeack package imports
from .utils import generate_result_filename


def banner():
    '''
    Prints SafeAck Banner
    '''
    print(r'''
 ,---.           ,---.         ,---.        ,--.     
'   .-'  ,--,--./  .-' ,---.  /  O  \  ,---.|  |,-.  
`.  `-. ' ,-.  ||  `-,| .-. :|  .-.  || .--'|     /  
.-'    |\ '-'  ||  .-'\   --.|  | |  |\ `--.|  \  \  
`-----'  `--`--'`--'   `----'`--' `--' `---'`--'`--'
                https://safeack.com
    ''')


def start():
    '''
    Starts cli tool
    '''
    banner()

    parser = ArgumentParser(prog='safeack')
    parser.add_argument('-f', '--file', dest='fpath', type=str,
                        help='path or url of openapi/swagger specification file', required=True)
    parser.add_argument('-rl', '--rate-limit', dest='rate_limit',
                        help='API requests rate limit per second', type=float, default=60, required=False)
    parser.add_argument('-pr', '--path-regex', dest='path_regex_pattern', type=str,
                        help='run tests for paths matching given regex pattern', required=False, default=None)
    parser.add_argument('-o', '--output', dest='output_file', type=str,
                        help='path to store test results in specified format. Default format is html', required=False, default=None)
    parser.add_argument('-of', '--format', dest='output_format', type=str, choices=[
                        'json', 'yaml', 'html', 'table'], help='Data format to save (json, yaml, html, table). Default: table', required=False, default='json')
    parser.add_argument('-H', '--headers', dest='headers', type=str,
                        help='HTTP requests headers that should be sent during testing eg: User-Agent: safeack', required=False, default=None, action='append', nargs='*')
    parser.add_argument('-tdc', '--test-data-config', dest='test_data_config',
                        help='YAML file containing user test data for tests', required=False, type=str)
    args = parser.parse_args()

    # convert req headers str to dict
    headers_dict: dict = headers_list_to_dict(args.headers)

    # handle rate limiting options
    rate_limit = args.rate_limit

    # handle test user data config file
    test_data_config = args.test_data_config
    if test_data_config:
        test_data_config = read_yaml(args.test_data_config)
        test_data_config = validate_config_file_data(test_data_config)

    file_name = pjoin('results', f'{generate_result_filename()}.json')

    # parse args and run tests
    api_parser = create_parser(args.fpath)
    generate_and_run_tests(
        api_parser=api_parser,
        regex_pattern=args.path_regex_pattern,
        output_file=file_name,
        output_file_format=args.output_format,
        req_headers=headers_dict,
        rate_limit=rate_limit,
        test_data_config=test_data_config,
    )


if __name__ == '__main__':
    start()
