import unittest
import sys
import time
import os.path as path
  
sys.path.append(path.abspath(path.join(__file__, '../../../src')))

import threading
from renderer.MatrixBuffer import MatrixBuffer
from data.data import Data
from data.scoreboard_config import ScoreboardConfig
from renderer.main import MainRenderer

class TestMainRenderer(unittest.TestCase):

  def test_render_offday(self):
    matrix = MatrixBuffer(
      panel_offset=0,
      zmq_client=None
    )

    scoreboard_config = ScoreboardConfig(
      filename_base='config_0',
      args=None,
      size=(matrix.width, matrix.height)
    )

    data = Data(config=scoreboard_config),
    sleep_event = threading.Event()

    # time.sleep(10)

    # print('printing data status...')
    # print(data.status)



    main_renderer = MainRenderer(
      matrix=matrix,
      data=data,
      sleepEvent=sleep_event
    )


if __name__ == '__main__':
  unittest.main()