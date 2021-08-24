import argparse
import os
import time
import subprocess
from activity_logger import ActivityLogger

parser = argparse.ArgumentParser(description='Trigger activity for EDR agent testing.')
parser.add_argument('--file-path', metavar="/path/to/file.txt", required=True, type=str, dest='file_path')
# parser.add_argument('--executable-path', metavar="/path/to/executable", required=True, type=str, dest='file_path')
args = parser.parse_args()

logger = ActivityLogger('logs/somelog.json')

print('Creating file...')
with open(args.file_path, 'x') as f:
  logger.log_file_activity(
    f.name,
    'create',
    initiated_by='???',
    process_name='???',
    process_cmd_line='???',
    pid='???')
time.sleep(.35)
print('Done.')

print('Modifying file...')
with open(args.file_path, 'w') as f:
  f.write("Modifying this file")
  logger.log_file_activity(
    f.name,
    'modify',
    initiated_by='???',
    process_name='???',
    process_cmd_line='???',
    pid='???')
time.sleep(.35)
print('Done.')

print('Deleting file...')
os.remove(args.file_path)
logger.log_file_activity(
  f.name,
  'delete',
  initiated_by='???',
  process_name='???',
  process_cmd_line='???',
  pid='???')
time.sleep(.35)
print('Done.')

print('Starting process...')
p = subprocess.Popen(['ls', '-al'])
logger.log_process_activity(
  initiated_by='???',
  process_name='???',
  process_cmd_line='???',
  pid='???')
time.sleep(.35)
print('Done.')

# print('Killing process...')

# TODO: network

print('All done!')