import unittest

from src.renderer.MatrixBuffer import MatrixBuffer
from src.renderer.scoreboard import ScoreboardRenderer

class TestScoreboardRenderer(unittest.TestCase):

  def test_draw_scheduled(self):

    matrix = MatrixBuffer(
      panel_offset=0,
      zmq_client=None
    )

    sr = ScoreboardRenderer(
      data=data,
      matrix=matrix,
      scoreboard=scoreboard
      shot_on_goal=False
    )