import argparse
import os
import time
import psutil
from subprocess import DEVNULL
from activity_logger import ActivityLogger

parser = argparse.ArgumentParser(description='Trigger activity for EDR agent testing.')
parser.add_argument('--test-file-path', metavar="/path/to/test_file.txt", required=True, type=str, dest='test_file_path')
parser.add_argument('--log-file-path', metavar="/path/to/log.yaml", required=True, type=str, dest='log_file_path')
parser.add_argument('--executable', metavar="\"/path/to/executable --with-flags\"", required=True, type=str, dest='executable')
args = parser.parse_args()

logger = ActivityLogger(args.log_file_path)
current_process = psutil.Process(os.getpid())
test_file_full_path = os.path.realpath(args.test_file_path)

print('Creating file...')
with open(test_file_full_path, 'x') as f:
  logger.log_activity(current_process, 'file', file_interaction='create', full_file_path=test_file_full_path)
time.sleep(.35)
print('Done.')

print('Modifying file...')
with open(test_file_full_path, 'w') as f:
  f.write("Modifying this file")
  logger.log_activity(current_process, 'file', file_interaction='modify', full_file_path=test_file_full_path)
time.sleep(.35)
print('Done.')

print('Deleting file...')
os.remove(test_file_full_path)
logger.log_activity(current_process, 'file', file_interaction='delete', full_file_path=test_file_full_path)
time.sleep(.35)
print('Done.')

print('Starting process...')
process_args = args.executable.split()
p = psutil.Popen(process_args, stdout=DEVNULL, stderr=DEVNULL)
logger.log_activity(p, 'process', timestamp=p.create_time())
time.sleep(.35)
print('Done.')

# print('Killing process...')

# TODO: network

print('All done!')