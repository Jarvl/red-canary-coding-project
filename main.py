import os
import argparse
from activity_generator.helpers import get_current_process
from activity_generator import Generator, Logger

parser = argparse.ArgumentParser(description='Trigger activity for EDR agent testing.')
parser.add_argument('--log-file-path', metavar="/path/to/log.yaml", required=True, type=str, dest='log_file_path')
parser.add_argument('--test-file-path', metavar="/path/to/test_file.txt", required=True, type=str, dest='test_file_path')
parser.add_argument('--test-command', metavar="\"/path/to/executable --with-flags\"", required=True, type=str, dest='test_command')
parser.add_argument('--test-hostname', metavar="www.google.com", required=True, type=str, dest='test_hostname')
parser.add_argument('--test-port', metavar="80", required=True, type=int, dest='test_port')
args = parser.parse_args()

current_process = get_current_process()

full_log_file_path = os.path.realpath(args.log_file_path)
logger = Logger(full_log_file_path)
generator = Generator(current_process, logger)

test_file_full_path = os.path.realpath(args.test_file_path)

print('Creating file...')
generator.create_file(test_file_full_path)

print('Modifying file...')
generator.modify_file(test_file_full_path)

print('Deleting file...')
generator.delete_file(test_file_full_path)

print('Starting process...')
generator.start_process(args.test_command)

print('Starting network connection and transmitting data...')
generator.transmit_data(args.test_hostname, args.test_port)

print('All done!')
