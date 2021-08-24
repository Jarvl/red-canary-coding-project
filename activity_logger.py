import os
import json
from datetime import datetime

class ActivityLogger:
  def __init__(self, log_file_path):
    self.logs = {'data': []}
    self.log_file_path = log_file_path

  def write_entries(self):
    with open(self.log_file_path, 'w') as f:
      f.seek(0)
      f.write(json.dumps(self.logs, indent=2))
      f.truncate()

  def log_process_activity(self, **kwargs):
    self.log_activity(activity_type='process', **kwargs)

  def log_file_activity(self, file_name, interaction, **kwargs):
    full_file_path = os.path.realpath(file_name)
    self.log_activity(
      activity_type='file',
      interaction=interaction,
      full_file_path=full_file_path,
      **kwargs)

  # def log_network_activity(self, dest_host, dest_port, src_host, src_port, bytes_tx, protocol, interaction, **kwargs):
  #   self.log_activity(
  #     activity_type='network',
  #     destination=dest_host,
  #     full_file_path=full_file_path,
  #     **kwargs)

  def log_activity(self, **kwargs):
    self.logs['data'].append({'timestamp': self.generate_timestamp(), **kwargs})
    self.write_entries()

  @staticmethod
  def generate_timestamp():
    return datetime.utcnow().isoformat()
