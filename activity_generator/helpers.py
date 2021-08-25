import os
import psutil
from functools import wraps
from unittest.mock import MagicMock, patch, mock_open

ACTIVITY_FILE = 'file'
ACTIVITY_PROCESS = 'process'
ACTIVITY_NETWORK = 'network'
FILE_INTERACTION_CREATE = 'create'
FILE_INTERACTION_MODIFY = 'modify'
FILE_INTERACTION_DELETE = 'delete'
PROTOCOL_TCP = 'tcp'

def get_current_process():
  return psutil.Process(os.getpid())

def patch_open(location):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      open_mock = mock_open()
      with patch(location, open_mock):
        return func(*args, open_mock, **kwargs)
    return wrapper
  return decorator

class MockProcess:
  @property
  def pid(self):
    return 1000