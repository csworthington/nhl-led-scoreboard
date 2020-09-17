from PIL import Image, ImageDraw
import math
from utils import round_normal

# libraries used for testing
from renderer.ZmqClient import ZMQClient
import time

DEBUG = False

class Matrix():
  def __init__(self, panel_number, zmq_client):
    self.panel_number = panel_number

    self.position_cache = {}
    
    self.width = 64
    self.height = 32

    # self.image = Image.new('RGBA', (self.width, self.height))
    self.image = Image.new('RGB', (self.width, self.height))
    self.draw = ImageDraw.Draw(self.image)

    self.pixels = self.image.load()

    # TODO figure out if this can be removed
    self.use_canvas = False

    self.zmq_client = zmq_client
  

  def parse_location(self, value, dimension):
    ''' 
    Check if the number is a percentage and calculate pixels
    '''
    # Check if number is percentage and calculate pixels
    if (isinstance(value, str) and value.endswith('%')):
      return round_normal((float(value[:-1]) / 100.0) * (dimension - 1))

    return value
  
  def align_position(self, align, position, size):
    align = align.split("-")
    x, y = position

    # Handle percentages by converting to pixels
    x = self.parse_location(x, self.width)
    y = self.parse_location(y, self.height)

    if (align[0] == "center"):
      x -= size[0] / 2
    elif (align[0] == "right"):
      x -= size[0]

    if (len(align) > 1):
      if (align[1] == "center"):
        y -= size[1] / 2 + 1
      elif (align[1] == "bottom"):
        y -= size[1]

    if x % 2 == 0:
      x = math.ceil(x)
    else:
      x = math.floor(x)

    return (round_normal(x), round_normal(y))
  

  def draw_rectangle(self, position, size, color):
    self.draw.rectangle(
      [
        position[0], 
        position[1], 
        position[0] + size[0], 
        position[1] + size[1]
      ], 
      fill=color
    )

    return {
      "position": position,
      "size": size
    }
  

  def cache_position(self, id, position):
    self.position_cache[id] = position

  def render(self):
    if (DEBUG):
      for x in range(self.height):
        self.draw_pixel(
          (self.width / 2 - 1, x),
          (0, 255, 0)
        )
        self.draw_pixel(
          (self.width / 2, x),
          (0, 255, 0)
        )

      for x in range(self.width):
        self.draw_pixel(
          (x, self.height / 2 - 1),
          (0, 255, 0)
        )
        self.draw_pixel(
          (x, self.height / 2),
          (0, 255, 0)
        )

    if (self.use_canvas):
      # self.canvas.SetImage(self.image.convert('RGB'), 0, 0)
      # self.canvas = self.matrix.SwapOnVSync(self.canvas)
      self.send_to_matrix()
      
    else:
      # self.matrix.SetImage(self.image.convert('RGB'))
      self.send_to_matrix()

  def clear(self):
    self.image.paste(0, (0, 0, self.width, self.height))
  

  def send_to_matrix(self):
    
    self.zmq_client.send_image(self.image)

  def network_issue_indicator(self):
    '''
    If there is a network issue, draw something on the screen
    '''
    red = self.graphics.Color(255, 0, 0)
    self.graphics.DrawLine(self.matrix, 0, self.matrix.height - 1, self.matrix.width, self.matrix.height - 1, red)


if __name__ == '__main__':
  zmq_client = ZMQClient(host_name='tcp://localhost:5555')
  image_matrix = Matrix(panel_number=1, zmq_client=zmq_client)

  print('testing drawing rectangle...')
  image_matrix.draw_rectangle(position=[2,2], size=[20, 20], color=(0,255,0))
  time.sleep(3)

  print('finishing...')
  zmq_client.close_socket()