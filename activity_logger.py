import os
import json
from datetime import datetime

class ActivityLogger:
  def __init__(self, log_file_path):
    self.log_file_path = log_file_path
    if not os.path.exists(self.log_file_path):
      with open(self.log_file_path, 'w') as f:
        f.write('logs:')

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
    entries = {'timestamp': self.generate_timestamp(), **kwargs}
    with open(self.log_file_path, 'a') as f:
      entries_formatted = '\n    '.join(['{}: "{}"'.format(k, v) for k, v in entries.items()])
      log_text = '\n  - {}'.format(entries_formatted)
      f.write(log_text)

  @staticmethod
  def generate_timestamp():
    return datetime.utcnow().isoformat()
