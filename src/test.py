from renderer.ZmqClient import ZMQClient
from renderer.MatrixBuffer import MatrixBuffer
from utils import get_file

import time
import os
from PIL import ImageFont

if __name__ == '__main__':
  zmq_client = ZMQClient(host_name='tcp://localhost:5555')
  image_matrix = MatrixBuffer(panel_number=1, zmq_client=zmq_client)

  # load font
  font = ImageFont.truetype(get_file("assets/fonts/04B_24__.TTF"), 8)
  font_large = ImageFont.truetype(get_file("assets/fonts/score_large.otf"), 16)
  font_pb = ImageFont.truetype(get_file("assets/fonts/score_large.otf"), 22)
  font_large_2 = ImageFont.truetype(get_file("assets/fonts/04B_24__.TTF"), 24)

  print('testing drawing text...')
  image_matrix.draw_text(
    position=(1,1),
    text='Hi',
    font=font,
    fill=(0,0,0),
    align='left',
    backgroundColor=(255,0,0)
  )
  image_matrix.render()
  time.sleep(2)


  # print('testing drawing rectangle...')
  # image_matrix.draw_rectangle(position=(10, 5), size=(25, 10), color=(0,0,255))
  # # image_matrix.draw_rectangle(position=[2,2], size=[20, 20], color=(255,255,0))
  # image_matrix.render()
  # time.sleep(2)

  print('clearing...')
  image_matrix.clear()
  image_matrix.render()
  # time.sleep(1)

  print('drawing single pixel..')
  image_matrix.draw_pixel((63,31), (255,255,255))
  image_matrix.render()

  # print('drawing multiple pixels...')
  # image_matrix.draw_pixels(
  #   position=(10,10), 
  #   pixels=[(255,255,255), (0,0,255), (0,255,0)],
  #   size=3,
  #   align='left'  
  # )

  # print('showing no network connection..')
  # image_matrix.network_issue_indicator()
  # image_matrix.render()
  # time.sleep(2)

  print('finishing...')
  zmq_client.close_socket()