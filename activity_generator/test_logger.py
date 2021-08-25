import os
import unittest
import json
from functools import wraps
from unittest.mock import MagicMock, patch, mock_open
from activity_generator import Logger
from activity_generator.helpers import get_current_process, patch_open, ACTIVITY_FILE

current_process = get_current_process()
log_file_path = 'testing.yml'
test_timestamp = 1629848608
test_log_text = '- somekey: somevalue'

class TestLogger(unittest.TestCase):
  @patch('os.path.exists', MagicMock(return_value=False))
  @patch_open('activity_generator.logger.open')
  def test_non_existent_log_file(self, open_mock):
    Logger(log_file_path)
    open_mock.assert_called_once_with(log_file_path, 'w')
    open_mock.return_value.write.assert_called_once_with('logs:')

  @patch('os.path.exists', MagicMock(return_value=True))
  @patch_open('activity_generator.logger.open')
  def test_existing_log_file(self, open_mock):
    Logger(log_file_path)
    open_mock.assert_not_called()

  @patch('os.path.exists', MagicMock(return_value=True))
  @patch('activity_generator.Logger.format_log_entries', MagicMock(return_value=test_log_text))
  @patch_open('activity_generator.logger.open')
  def test_log_activity_file_write(self, open_mock):
    logger = Logger(log_file_path)
    logger.log_activity(ACTIVITY_FILE, current_process)
    open_mock.assert_called_once_with(logger.log_file_path, 'a')
    open_mock.return_value.write.assert_called_once_with(test_log_text)

  @patch('os.path.exists', MagicMock(return_value=True))
  @patch('activity_generator.Logger.generate_timestamp', MagicMock(return_value=test_timestamp))
  @patch_open('activity_generator.logger.open')
  def test_log_activity_default_values(self, open_mock):
    logger = Logger(log_file_path)
    logger.log_activity(ACTIVITY_FILE, current_process)
    open_mock.return_value.write.assert_called_once()
    log_text = str(open_mock.return_value.write.call_args_list[0][0])

    assert 'activity_type: "{}"'.format(ACTIVITY_FILE) in log_text
    assert 'timestamp: {}'.format(test_timestamp) in log_text
    assert 'pid: {}'.format(current_process.pid) in log_text
    assert 'process_name: "{}"'.format(current_process.name()) in log_text
    # Convert cmdline array to format used for the log
    assert 'process_cmd_line: {}'.format(json.dumps(current_process.cmdline())) in log_text
    assert 'initiated_by: "{}"'.format(current_process.username()) in log_text

  @patch('os.path.exists', MagicMock(return_value=True))
  @patch_open('activity_generator.logger.open')
  def test_log_activity_passed_timestamp(self, open_mock):
    logger = Logger(log_file_path)
    logger.log_activity(ACTIVITY_FILE, current_process, timestamp=test_timestamp)
    open_mock.return_value.write.assert_called_once()
    log_text = str(open_mock.return_value.write.call_args_list[0][0])
    assert 'timestamp: {}'.format(test_timestamp) in log_text

  @patch('os.path.exists', MagicMock(return_value=True))
  @patch_open('activity_generator.logger.open')
  def test_log_activity_extra_values(self, open_mock):
    logger = Logger(log_file_path)
    logger.log_activity(ACTIVITY_FILE, current_process, timestamp=test_timestamp, extra_key='extra_val')
    open_mock.return_value.write.assert_called_once()
    log_text = str(open_mock.return_value.write.call_args_list[0][0])
    assert 'extra_key: "extra_val"' in log_text