import argparse
import os
import psutil
from subprocess import DEVNULL
import socket
from activity_logger import ActivityLogger

parser = argparse.ArgumentParser(description='Trigger activity for EDR agent testing.')
parser.add_argument('--test-file-path', metavar="/path/to/test_file.txt", required=True, type=str, dest='test_file_path')
parser.add_argument('--log-file-path', metavar="/path/to/log.yaml", required=True, type=str, dest='log_file_path')
parser.add_argument('--test-command', metavar="\"/path/to/executable --with-flags\"", required=True, type=str, dest='test_command')
parser.add_argument('--test-hostname', metavar="www.google.com", required=True, type=str, dest='test_hostname')
parser.add_argument('--test-port', metavar="80", required=True, type=int, dest='test_port')

args = parser.parse_args()

logger = ActivityLogger(args.log_file_path)
current_process = psutil.Process(os.getpid())
test_file_full_path = os.path.realpath(args.test_file_path)

print('Creating file...')
with open(test_file_full_path, 'x') as f:
  logger.log_activity('file', current_process, file_interaction='create', full_file_path=test_file_full_path)
print('Done.')

print('Modifying file...')
with open(test_file_full_path, 'w') as f:
  f.write("Modifying this file")
  logger.log_activity('file', current_process, file_interaction='modify', full_file_path=test_file_full_path)
print('Done.')

print('Deleting file...')
os.remove(test_file_full_path)
logger.log_activity('file', current_process, file_interaction='delete', full_file_path=test_file_full_path)
print('Done.')

print('Starting process...')
process_args = args.test_command.split()
p = psutil.Popen(process_args, stdout=DEVNULL, stderr=DEVNULL)
logger.log_activity('process', p, timestamp=p.create_time())
print('Done.')

print('Starting network connection and transmitting data...')

BUFFER_SIZE = 4096
req_content = "GET / HTTP/1.1\r\nHost:{}\r\n\r\n".format(args.test_hostname).encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP) as s:
  s.connect((socket.gethostbyname(args.test_hostname), args.test_port))
  s.sendall(req_content)
  dest_ip, dest_port = s.getpeername()
  src_ip, src_port = s.getsockname()
  bytes_sent = len(req_content)
  protocol= s.proto
  print(s.recv(1000))

  logger.log_activity(
    'network',
    current_process,
    dest_ip=dest_ip,
    dest_port=dest_port,
    src_ip=src_ip,
    src_port=src_port,
    bytes_sent=bytes_sent,
    protocol='TCP')

print('All done!')