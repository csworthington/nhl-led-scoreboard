import sys
from datetime import datetime, timedelta
from data.scoreboard_config import ScoreboardConfig
from renderer.main import MainRenderer
# from rgbmatrix import RGBMatrix, RGBMatrixOptions
# from utils import args, led_matrix_options
from utils import args
from data.data import Data
import threading
from sbio.dimmer import Dimmer
from sbio.pushbutton import PushButton
# from renderer.matrix import Matrix
import debug

from renderer.MatrixBuffer import MatrixBuffer
from renderer.ZmqClient import ZMQClient

SCRIPT_NAME = "NHL-LED-SCOREBOARD"

SCRIPT_VERSION = "1.1.5"


def run():
    # Get supplied command line arguments
    commandArgs = args()

    # Check for led configuration arguments
    # matrixOptions = led_matrix_options(commandArgs)
    # matrixOptions.drop_privileges = False

    print('panel offset = ' + str(commandArgs.panel_offset))

    # Initialize the matrix
    matrix = MatrixBuffer(
        panel_offset=commandArgs.panel_offset, 
        zmq_client=ZMQClient(host_name='tcp://localhost:5555', panel_offset=commandArgs.panel_offset)
    )

    # Set panel number for debug
    debug.set_panel_number(commandArgs.panel_offset)

    # Print some basic info on startup
    debug.info("{} - v{} ({}x{})".format(SCRIPT_NAME, SCRIPT_VERSION, matrix.width, matrix.height))

    # Get config file name by adding panel offset number to end of string
    config_file_name = 'config_{0}'.format(commandArgs.panel_offset)

    # Read scoreboard options from config.json if it exists
    config = ScoreboardConfig(config_file_name, commandArgs, (matrix.width, matrix.height))

    # Set up debug
    debug.set_debug_status(config)
    
    data = Data(config)

    # Event used to sleep when rendering
    # Allows Web API (coming in V2) and pushbutton to cancel the sleep
    sleepEvent = threading.Event()

    if data.config.dimmer_enabled:
        dimmer = Dimmer(data, matrix)
        dimmerThread = threading.Thread(target=dimmer.run, args=())
        dimmerThread.daemon = True
        dimmerThread.start()

    if data.config.pushbutton_enabled:
        pushbutton = PushButton(data,matrix,sleepEvent)
        pushbuttonThread = threading.Thread(target=pushbutton.run, args=())
        pushbuttonThread.daemon = True
        pushbuttonThread.start()

    MainRenderer(matrix, data, sleepEvent).render()

if __name__ == "__main__":
    try:
        run()

    except KeyboardInterrupt:
        print("Exiting NHL-LED-SCOREBOARD\n")
        sys.exit(0)
