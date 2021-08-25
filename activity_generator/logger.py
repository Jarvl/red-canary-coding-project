import os
import json
from datetime import datetime
import time

class Logger:
  def __init__(self, log_file_path):
    self.log_file_path = log_file_path
    if not os.path.exists(self.log_file_path):
      with open(self.log_file_path, 'w') as f:
        f.write('logs:')

  def log_activity(self, activity_type, process, timestamp=None, **kwargs):
    if timestamp is None:
      timestamp = Logger.generate_timestamp()
    entries = {
      'activity_type': activity_type,
      'timestamp': int(timestamp), # Remove decimal places for consistency
      'pid': process.pid,
      'process_name': process.name(),
      'process_cmd_line': process.cmdline(),
      'initiated_by': process.username(),
      **kwargs
    }
    with open(self.log_file_path, 'a') as f:
      entries_formatted = '\n    '.join(['{}: {}'.format(k, json.dumps(v)) for k, v in entries.items()])
      log_text = '\n  - {}'.format(entries_formatted)
      f.write(log_text)

  @staticmethod
  def generate_timestamp():
    return time.mktime(datetime.utcnow().timetuple())
