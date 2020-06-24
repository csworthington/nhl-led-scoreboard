import rpyc

class LEDMatrixService(rpyc.Service):

  def __init__(self, *args, **kwargs):
    pass

  def on_connect(self, conn):
    # code that runs when a connection is created
    print('connection created!')
  
  def on_disconnect(self, conn):
    # code that runs after the connection has already closed
    print('connection closed!')
  
  # to connect to a method, it must have the exposed prefix!
  def exposed_get_answer(self): # this is an exposed method
    return 42
  
  exposed_the_real_answer = 43

  def get_question(self): #while this method is not exposed
    return 'what is the airspped velocity of an unladen swallow?'

if __name__ == '__main__':
  from rpyc.utils.server import ThreadedServer
  t = ThreadedServer(LEDMatrixService(), port=18861)
  t.start()