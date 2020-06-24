import rpyc

class LEDMatrixClient():
  def __init__(self, *args, **kwargs):
    self.serviceIp = 'localhost'
    self.port = 18861

    self.connectToService(self.serviceIp, self.port)
    pass
  
  def connectToService(self, ip, port):
    self.connection = rpyc.connect(ip, port)
    print(self.connection.root.get_answer())


if __name__ == '__main__':
  client = LEDMatrixClient()