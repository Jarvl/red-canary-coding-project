import unittest
from unittest.mock import MagicMock, patch
import psutil
from activity_generator import Generator, Logger
from activity_generator.helpers import (
  get_current_process,
  patch_open,
  ACTIVITY_FILE,
  ACTIVITY_PROCESS,
  ACTIVITY_NETWORK,
  FILE_INTERACTION_CREATE,
  FILE_INTERACTION_MODIFY,
  FILE_INTERACTION_DELETE,
  PROTOCOL_TCP
)

current_process = get_current_process()
test_file_path = 'test.txt'

class TestGenerator(unittest.TestCase):
  @patch_open('activity_generator.generator.open')
  @patch('activity_generator.Logger')
  def test_create_file(self, open_mock, logger_mock):
    generator = Generator(current_process, logger_mock)
    generator.create_file(test_file_path)
    open_mock.assert_called_once_with(test_file_path, 'x')
    logger_mock.log_activity.assert_called_once_with(
      ACTIVITY_FILE,
      current_process,
      file_interaction=FILE_INTERACTION_CREATE,
      full_file_path=test_file_path)

  @patch_open('activity_generator.generator.open')
  @patch('activity_generator.Logger')
  def test_modify_file(self, open_mock, logger_mock):
    generator = Generator(current_process, logger_mock)
    generator.modify_file(test_file_path)
    open_mock.assert_called_once_with(test_file_path, 'w')
    logger_mock.log_activity.assert_called_once_with(
      ACTIVITY_FILE,
      current_process,
      file_interaction=FILE_INTERACTION_MODIFY,
      full_file_path=test_file_path)

  @patch('activity_generator.Logger')
  @patch('activity_generator.generator.os.remove')
  def test_delete_file(self, os_remove_mock, logger_mock):
    generator = Generator(current_process, logger_mock)
    generator.delete_file(test_file_path)
    os_remove_mock.assert_called_once_with(test_file_path)
    logger_mock.log_activity.assert_called_once_with(
      ACTIVITY_FILE,
      current_process,
      file_interaction=FILE_INTERACTION_DELETE,
      full_file_path=test_file_path)

  @patch('activity_generator.Logger')
  @patch('activity_generator.generator.psutil.Popen', autospec=True)
  def test_start_process(self, popen_mock, logger_mock):
    test_timestamp = 1629848608
    popen_mock_instance = popen_mock.return_value
    popen_mock_instance.create_time.return_value = test_timestamp

    generator = Generator(current_process, logger_mock)
    generator.start_process('echo test')
    popen_mock.assert_called_once()
    logger_mock.log_activity.assert_called_once_with(
      ACTIVITY_PROCESS,
      popen_mock_instance,
      timestamp=test_timestamp)

  @patch('activity_generator.Logger')
  @patch.object(Generator, 'get_req_content')
  @patch('activity_generator.generator.socket.socket', autospec=True)
  def test_transmit_data(self, socket_mock, get_req_content_mock, logger_mock):
    test_hostname = 'localhost'
    test_port = 80
    test_dest_ip = '127.0.0.1'
    test_dest_port = 80
    test_src_ip = '0.0.0.0'
    test_src_port = 34152
    test_req_content = 'some content'
    test_bytes_sent = len(test_req_content)

    get_req_content_mock.return_value = test_req_content
    socket_mock_instance = socket_mock.return_value
    print(socket_mock_instance)
    socket_mock_instance.getpeername.return_value = (test_dest_ip, test_dest_port)
    socket_mock_instance.getsockname.return_value = (test_src_ip, test_src_port)

    generator = Generator(current_process, logger_mock)
    generator.transmit_data(test_hostname, test_port)

    logger_mock.log_activity.assert_called_once_with(
      ACTIVITY_NETWORK,
      current_process,
      dest_ip=test_dest_ip,
      dest_port=test_dest_port,
      src_ip=test_src_ip,
      src_port=test_src_port,
      bytes_sent=test_bytes_sent,
      protocol=PROTOCOL_TCP)
