import unittest
import sys
import os.path as path
  
sys.path.append(path.abspath(path.join(__file__, '../../../src')))


import time
import threading
from renderer.MatrixBuffer import MatrixBuffer
from boards.boards import Boards
from data.data import Data
from data.scoreboard_config import ScoreboardConfig
from renderer.main import MainRenderer
from renderer.ZmqClient import ZMQClient

class TestBoards(unittest.TestCase):
  # def test_off_day(self):
  #   print('testing off day...')
  #   zmq_client = ZMQClient(host_name='tcp://localhost:5555')
  #   matrix = MatrixBuffer(
  #     panel_offset=0,
  #     zmq_client=zmq_client
  #   )

  #   scoreboard_config = ScoreboardConfig(
  #     filename_base='config_0',
  #     args=None,
  #     size=(matrix.width, matrix.height)
  #   )

  #   data = Data(config=scoreboard_config)
  #   sleep_event = threading.Event()

  #   board = Boards()

  #   board._off_day(
  #     data=data, 
  #     matrix=matrix,
  #     sleepEvent=sleep_event
  #   )
  
  def test_scheduled(self):
    print('testing scheduled day...')
    zmq_client = ZMQClient(host_name='tcp://localhost:5555')
    matrix = MatrixBuffer(
      panel_offset=0,
      zmq_client=zmq_client
    )

    scoreboard_config = ScoreboardConfig(
      filename_base='config_0',
      args=None,
      size=(matrix.width, matrix.height)
    )

    data = Data(config=scoreboard_config)
    sleep_event = threading.Event()

    board = Boards()

    board._scheduled(
      data=data, 
      matrix=matrix,
      sleepEvent=sleep_event
    )


if __name__ == '__main__':
  unittest.main()