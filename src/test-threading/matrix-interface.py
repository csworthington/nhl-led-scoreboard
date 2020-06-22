# Interface to allow multiple led matrixes to be controlled simultaneously by different programs

import argparse
from rgbmatrix import RGBMatrix, RGBMatrixOptions


class MatrixInterface():

  def __init__(self, *args, **kwargs):
    self.parser = argparse.ArgumentParser()
    self.parser.add_argument("--led-panels", action="store", help="Number of panels to be controlled independently. Default 1", default=1, type=int)
    
  def process(self):
    self.args = self.parser.parse_args()

    options = RGBMatrixOptions()

    if self.args.led-panels != None:
      # something here
  
  # receive a command from a thread and draw the panel
  def command(self, panel, command):