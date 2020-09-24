import unittest
import sys
import os.path as path
  
sys.path.append(path.abspath(path.join(__file__, '../../../src')))

from data.status import Status


class TestData(unittest.TestCase):
  
  def test_create_status(self):
    test_status = Status()
  
  def test_is_scheduled(self):
    test_status = Status()


if __name__ == '__main__':
  unittest.main()