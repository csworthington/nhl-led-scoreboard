from rgbmatrix import RGBMatrix, RGBMatrixOptions

class LEDMatrixWrapper():
  def __init__(self, options, *args, **kwargs):
    self.matrix = RGBMatrix(options=options)

    pass
  
  def _SwapOnVSync(self, canvas):
    ''' Wrapper for SwapOnVSync method '''
    return self.matrix.SwapOnVSync(canvas)
  
  def _CreateFrameCanvas(self):
    ''' Wrapper for CreateFrameCanvas method '''
    return self.matrix.CreateFrameCanvas()
  
  def _SetPixel(self, x_coord, y_coord, red_value, green_value, blue_value):
    return self.matrix.SetPixel(x_coord, y_coord, red_value, green_value, blue_value)
  
  def _getWidth(self):
    ''' Wrapper for width attribute of matrix class '''
    return self.matrix.width
  
  def _getHeight(self):
    ''' Wrapper for height attribute of matrix class '''
    return self.matrix.height