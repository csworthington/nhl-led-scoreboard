import zmq

class ZMQClient():
  def __init__(self, host_name, panel_number=1):
    # initialize socket
    self.context = zmq.Context()

    self.socket = self.context.socket(zmq.REQ)
    self.socket.connect(host_name)

    self.panel_number = panel_number
  

  def send_image(self, image):
    self.socket.send_pyobj(image)
    # TODO: possibly do not wait for reply?
    message = self.socket.recv()
  

  def close_socket(self):
    self.socket.close()
