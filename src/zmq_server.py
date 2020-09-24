from rgbmatrix import RGBMatrix, RGBMatrixOptions
from utils import args, led_matrix_options
import zmq
import os, sys, time
import subprocess
from PIL import Image

from renderer.ZmqClient import ZMQMessage

def start_subprocess(panel_offset=0):
  p = subprocess.Popen(['python3', './src/main.py', '--panel-offset={0}'.format(panel_offset)])
  print('started subprocess with pid=' + str(p.pid))
  return p

def run():
  # Get supplied command line arguments
  command_args = args()

  # Check for led configuration arguments
  matrixOptions = led_matrix_options(command_args)
  matrixOptions.drop_privileges = False

  # Initialize the matrix
  matrix = RGBMatrix(options = matrixOptions)

  # Initialize the offscreen canvas
  offscreen_canvas = matrix.CreateFrameCanvas()

  # Initialize ZMQ server
  socket_address = command_args.socket_addr
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind(socket_address)

  print('Server started at ' + socket_address)

  if (command_args.test_mode is False):
    print('Starting subprocesses...')

    # Declare list to contain each subprocess
    processes = list()
    num_processes = command_args.led_chain
    print('spawning {0} subprocesses...'.format(num_processes))

    for i in range(num_processes):
      processes.append(start_subprocess(panel_offset=i))
      


  print('Waiting for input...')

  offscreen_canvas.Fill(255,255,255)
  matrix.SwapOnVSync(offscreen_canvas)

  # create empty image
  empty_image = Image.new('RGB', (64,32))

  continue_loop = True

  while (continue_loop):
    message = socket.recv_pyobj()
    # print('received request')
    
    if (isinstance(message, ZMQMessage)):
      x_image_location = 64 * message.panel_offset
      offscreen_canvas.SetImage(empty_image, x_image_location, 0)
      offscreen_canvas.SetImage(message.image, x_image_location, 0)
      matrix.SwapOnVSync(offscreen_canvas)
    else:
      print('type mismatch')

    socket.send(b'done')
  
  socket.close()
  


if __name__ == "__main__":
  try:
    run()

  except KeyboardInterrupt:
    print("Exiting ZMQ_SERVER.py\n")
    sys.exit(0)
