from renderer.ZmqClient import ZMQClient
from renderer.ImageMatrix import Matrix
import time

if __name__ == '__main__':
  zmq_client = ZMQClient(host_name='tcp://localhost:5555')
  image_matrix = Matrix(panel_number=1, zmq_client=zmq_client)

  print('testing drawing rectangle...')
  image_matrix.draw_rectangle(position=[2,2], size=[20, 20], color=(0,255,0))
  image_matrix.render()
  time.sleep(3)

  print('finishing...')
  zmq_client.close_socket()