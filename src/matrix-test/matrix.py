from rgbmatrix import RGBMatrix, RGBMatrixOptions

class LEDMatrixWrapper():
  def __init__(self, options, num_panels=1, *args, **kwargs):
    self.matrix = RGBMatrix(options=options)


    # set up the fake panel to store info
    singlePanelOptions = RGBMatrixOptions()

    singlePanelOptions.hardware_mapping = "regular"
    singlePanelOptions.rows = 32
    singlePanelOptions.cols = 64
    singlePanelOptions.chain_length = 1
    singlePanelOptions.parallel = 1
    singlePanelOptions.row_address_type = 0 # default row address type
    singlePanelOptions.multiplexing = 0 # default multiplexint
    singlePanelOptions.pwm_bits = 11 # default led pwm bits
    singlePanelOptions.brightness = 100 # default brightness 100
    singlePanelOptions.pwm_lsb_nanoseconds = 130 # default pwm nanoseconds
    singlePanelOptions.led_rgb_sequence = "RGB" # default sequence
    singlePanelOptions.pixel_mapper_config = "" # default pixel mapper
    singlePanelOptions.panel_type = ""

    self.singlePanel = RGBMatrix(options=singlePanelOptions)

    self.numPanels = num_panels

    pass
  
  def getOffsetPanel(self):
    return self.singlePanel.CreateFrameCanvas()
  
  def setOffsetCanvas(self, canvas, offset):
    x_offset = 64 * offset

    for x in range(0, 64):
      for y in range(0, 32):
        pass
    pass
  
  def _SwapOnVSync(self, canvas):
    ''' Wrapper for SwapOnVSync method '''
    return self.matrix.SwapOnVSync(canvas)
  
  def _CreateFrameCanvas(self):
    ''' Wrapper for CreateFrameCanvas method '''
    return self.matrix.CreateFrameCanvas()
  
  def _SetPixel(self, x_coord, y_coord, red_value, green_value, blue_value, panel_offset=0):
    # return self.matrix.SetPixel((x_coord + (panel_offset * 64)), (y_coord + (panel_offset * 64)), red_value, green_value, blue_value)
    return self.matrix.SetPixel(x_coord, y_coord, red_value, green_value, blue_value)

  def _getPanelWidth(self):
    ''' Return width of individual panel '''
    # return int(self.matrix.width / self.numPanels)
    # return int(self.matrix.width)
    return self.singlePanel.width
  
  def _getPanelHeight(self):
    ''' Return height of individual panel '''
    # return self._getHeight()
    return self.singlePanel.height
  
  def _getWidth(self):
    ''' Wrapper for width attribute of matrix class '''
    return self.matrix.width
  
  def _getHeight(self):
    ''' Wrapper for height attribute of matrix class '''
    return self.matrix.height