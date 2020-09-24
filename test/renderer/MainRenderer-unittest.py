import unittest
import sys
import os.path as path
  
sys.path.append(path.abspath(path.join(__file__, '../../../src')))

import time
import threading
from renderer.MatrixBuffer import MatrixBuffer
from data.data import Data
from data.scoreboard_config import ScoreboardConfig
from renderer.main import MainRenderer
from renderer.ZmqClient import ZMQClient

class TestMainRenderer(unittest.TestCase):

  def test_render_offday(self):
    zmq_client = ZMQClient(host_name='tcp://localhost:5555')
    matrix = MatrixBuffer(
      panel_offset=0,
      zmq_client=None
    )

    scoreboard_config = ScoreboardConfig(
      filename_base='config_0',
      args=None,
      size=(matrix.width, matrix.height)
    )

    data = Data(config=scoreboard_config)
    sleep_event = threading.Event()

    main_renderer = MainRenderer(
      matrix=matrix,
      data=data,
      sleepEvent=sleep_event
    )
    main_renderer.__render_offday()
  

  # def test_render(self):
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

  #   main_renderer = MainRenderer(
  #     matrix=matrix,
  #     data=data,
  #     sleepEvent=sleep_event
  #   )

  #   main_renderer.render()


if __name__ == '__main__':
  unittest.main()