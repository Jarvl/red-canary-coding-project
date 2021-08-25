import os
from subprocess import DEVNULL
import socket
import psutil
from activity_generator.helpers import (
  ACTIVITY_FILE,
  ACTIVITY_PROCESS,
  ACTIVITY_NETWORK,
  FILE_INTERACTION_CREATE,
  FILE_INTERACTION_MODIFY,
  FILE_INTERACTION_DELETE,
  PROTOCOL_TCP
)

class Generator:
  def __init__(self, current_process, logger_instance):
    self.current_process = current_process
    self.logger = logger_instance

  def create_file(self, full_file_path):
    with open(full_file_path, 'x') as _f:
      self.logger.log_activity(
        ACTIVITY_FILE,
        self.current_process,
        file_interaction=FILE_INTERACTION_CREATE,
        full_file_path=full_file_path)

  def modify_file(self, full_file_path):
    with open(full_file_path, 'w') as f:
      f.write("Modifying this file")
      self.logger.log_activity(
        ACTIVITY_FILE,
        self.current_process,
        file_interaction=FILE_INTERACTION_MODIFY,
        full_file_path=full_file_path)

  def delete_file(self, full_file_path):
    os.remove(full_file_path)
    self.logger.log_activity(
      ACTIVITY_FILE,
      self.current_process,
      file_interaction=FILE_INTERACTION_DELETE,
      full_file_path=full_file_path)

  def start_process(self, command):
    process_args = command.split()
    new_process = psutil.Popen(process_args, stdout=DEVNULL, stderr=DEVNULL)
    self.logger.log_activity(ACTIVITY_PROCESS, new_process, timestamp=new_process.create_time())

  def transmit_data(self, hostname, port):
    req_content = Generator.get_req_content(hostname)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
    s.connect((socket.gethostbyname(hostname), port))
    s.sendall(req_content)
    dest_ip, dest_port = s.getpeername()
    src_ip, src_port = s.getsockname()
    bytes_sent = len(req_content)
    self.logger.log_activity(
      ACTIVITY_NETWORK,
      self.current_process,
      dest_ip=dest_ip,
      dest_port=dest_port,
      src_ip=src_ip,
      src_port=src_port,
      bytes_sent=bytes_sent,
      protocol=PROTOCOL_TCP)
    s.close()

  @staticmethod
  def get_req_content(hostname):
    return "GET / HTTP/1.1\r\nHost:{}\r\n\r\n".format(hostname).encode()