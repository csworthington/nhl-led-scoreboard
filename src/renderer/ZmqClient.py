import zmq

class ZMQImageMessage():
  def __init__(self, image, panel_offset):
    self.image = image
    self.panel_offset = panel_offset
  
  def __str__(self):
    return ''


def ZMQMessage():
  def __init__(self, panel_offset):
    self.panel_offset = panel_offset


def ZMQHornMessage(ZMQMessage):
  def __init__(self, panel_offset):
    super().__init__(panel_offset)

class ZMQChangeTeamMessage():
  def __init__(self, panel_number, team):
    self.team = team
    self.panel_number = panel_number


class ZMQClient():
  def __init__(self, host_name, panel_offset=0):
    # initialize socket
    self.context = zmq.Context()

    self.socket = self.context.socket(zmq.REQ)
    self.socket.connect(host_name)

    self.panel_offset = panel_offset
  

  def send_image(self, image):
    # message = (self.panel_number, image)
    message = ZMQImageMessage(image=image, panel_offset=self.panel_offset)
    # self.socket.send_pyobj(image)
    self.socket.send_pyobj(message)
    # TODO: possibly do not wait for reply?
    message = self.socket.recv()
  

  def close_socket(self):
    self.socket.close()
