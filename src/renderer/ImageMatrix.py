from PIL import Image, ImageDraw
import math
from utils import round_normal

DEBUG = False

class Matrix():
  def __init__(self, panel_number, zmq_client):
    self.panel_number = panel_number

    self.position_cache = {}
    
    self.width = 64
    self.height = 32

    # self.image = Image.new('RGBA', (self.width, self.height))
    self.image = Image.new('RGB', (self.width, self.height))
    self.draw = ImageDraw.Draw(self.image)

    self.pixels = self.image.load()

    # TODO figure out if this can be removed
    self.use_canvas = False

    self.zmq_client = zmq_client
  

  def parse_location(self, value, dimension):
    """ 
    Check if the number is a percentage and calculate pixels
    """
    # Check if number is percentage and calculate pixels
    if (isinstance(value, str) and value.endswith('%')):
      return round_normal((float(value[:-1]) / 100.0) * (dimension - 1))

    return value
  
  def align_position(self, align, position, size):
    align = align.split("-")
    x, y = position

    # Handle percentages by converting to pixels
    x = self.parse_location(x, self.width)
    y = self.parse_location(y, self.height)

    if (align[0] == "center"):
      x -= size[0] / 2
    elif (align[0] == "right"):
      x -= size[0]

    if (len(align) > 1):
      if (align[1] == "center"):
        y -= size[1] / 2 + 1
      elif (align[1] == "bottom"):
        y -= size[1]

    if x % 2 == 0:
      x = math.ceil(x)
    else:
      x = math.floor(x)

    return (round_normal(x), round_normal(y))


  def draw_text(self, position, text, font, fill=None, align="left", 
                backgroundColor=None, backgroundOffset=[1, 1, 1, 1]):
    """
    Draw text on the pillow canvas.

    Args:
      position: The coordinates of the top left corner of the text in format (x,y)
      text: The text to be drawn on the Pillow canvas
      font: a Pillow ImageFont object for drawing the text
      fill: the colour of the text in RGB format (R,G,B)
      align:
      backgroundColor: the background colour of the text in RGB format (R,G,B)
      backgroundOffset:
    
    Returns:
      A python object with parameters for position and size
    """
    width = 0
    height = 0

    text_chars = text.split("\n")
    offsets = []

    for index, chars in enumerate(text_chars):
      spacing = 0 if index == 0 else 1

      offset = font.getoffset(chars)
      offset_x = offset[0]
      offset_y = offset[1] - height - spacing

      offsets.append((offset_x, offset_y))

      bounding_box = font.getmask(chars).getbbox()
      if bounding_box is not None:
        width = bounding_box[2] if bounding_box[2] > width else width
        height += bounding_box[3] + spacing

    width -= 1
    height -= 1
    size = (width, height)

    x, y = self.align_position(align, position, size)
    
    if (backgroundColor != None):
      self.draw_rectangle(
        (x - backgroundOffset[0], y - backgroundOffset[1]),
        (width + backgroundOffset[0] + backgroundOffset[2], height + backgroundOffset[1] + backgroundOffset[3]),
        backgroundColor
      )

    if (backgroundColor != None):
      self.draw_rectangle(
        (x - backgroundOffset[0], y - backgroundOffset[1]),
        (width + backgroundOffset[0] + backgroundOffset[2], height + backgroundOffset[1] + backgroundOffset[3]),
        backgroundColor
      )

    for index, chars in enumerate(text_chars):
      offset = offsets[index]
      chars_position = (x - offset[0], y - offset[1])

      self.draw.text(
        chars_position,
        chars,
        fill=fill,
        font=font
      )

    if (DEBUG):
      self.draw_pixel(
        (x, y),
        (0, 255, 0)
      )
      self.draw_pixel(
        (x, y + height),
        (0, 255, 0)
      )
      self.draw_pixel(
        (x + width, y + height),
        (0, 255, 0)
      )
      self.draw_pixel(
        (x + width, y),
        (0, 255, 0)
      )

    return {
      "position": (x, y),
      "size": size
    }

  def draw_image(self, position, image, align="left"):
    """
    Draw an image on the canvas at the specified position.

    Args:
      position: the coordinates for where to draw the top left corner of the image in format (x,y)
      image: the pillow image to be drawn
    
    Returns:
      A python object with parameters for the image's position and size
    """
    position = self.align_position(align, position, image.size)

    try:
      self.image.paste(image, position, image)
    except:
      self.image.paste(image, position)

    return {
      "position": position,
      "size": image.size
    }

  def draw_rectangle(self, position, size, color):
    """
    Draw a rectangle on the pillow canvas.

    Args:
      position: the coordinates of the top left corner of the rectangle in format (x,y)
      size: the size of the sides of the rectangle in format (width, height)
      color: the colour of the rectangle in format (R,G,B)
    
    Returns:
      A python object with the position and size of the rectangle
    """
    self.draw.rectangle(
      [
        position[0], 
        position[1], 
        position[0] + size[0], 
        position[1] + size[1]
      ], 
      fill=color
    )

    return {
      "position": position,
      "size": size
    }
  

  def draw_pixel(self, position, color):
    """
    Fill a pixel on the pillow canvas with a specific colour.

    Args:
      position: the coordinates for the pixel to be filled in format (x,y)
      color: An RGB tuple representing the colour to be filled
    """
    try:
      self.pixels[position] = color
    except:
      print(position, "out of range!")


  def draw_pixels(self, position, pixels, size, align="left"):
    """
    Draw multiple pixels on the pillow canvas

    Args:
      position:
      pixels:
      size:
      align:
    """
    x, y = self.align_position(align, position, size)

    for pixel in pixels:
      self.draw_pixel(
        (
            pixel.position[0] + x,
            pixel.position[1] + y,
        ),
        pixel.color
      )
  

  def draw_text_layout(self, layout, text, align="left", backgroundColor=None):
    self.cache_position(
      layout.id,
      self.draw_text(
        self.layout_position(layout),
        text,
        fill=layout.color,
        font=layout.font,
        backgroundColor=backgroundColor, #layout.backgroundColor if hasattr(layout, 'backgroundColor') else None,
        align=layout.align
      )
    )

  def draw_image_layout(self, layout, image, offset=(0, 0)):
    self.cache_position(
      layout.id,
      self.draw_image(
        self.layout_position(layout, offset),
        image,
        layout.align
      )
    )


  def draw_pixels_layout(self, layout, pixels, size):
    self.cache_position(
      layout.id,
      self.draw_pixels(
        self.layout_position(layout),
        pixels,
        size,
        layout.align
      )
    )


  def layout_position(self, layout, offset=(0, 0)):
    x = layout.position[0] + offset[0]
    y = layout.position[1] + offset[1]

    if (hasattr(layout, 'relative') and layout.relative.to in self.position_cache):
      cached_position = self.position_cache[layout.relative.to]
      position = self.align_position(
        layout.relative.align,
        cached_position["position"],
        (
          -cached_position["size"][0],
          -cached_position["size"][1]
        )
      )

      x += position[0]
      y += position[1]

    return (x, y)

  def cache_position(self, id, position):
    self.position_cache[id] = position

  def render(self):
    if (DEBUG):
      for x in range(self.height):
        self.draw_pixel(
          (self.width / 2 - 1, x),
          (0, 255, 0)
        )
        self.draw_pixel(
          (self.width / 2, x),
          (0, 255, 0)
        )

      for x in range(self.width):
        self.draw_pixel(
          (x, self.height / 2 - 1),
          (0, 255, 0)
        )
        self.draw_pixel(
          (x, self.height / 2),
          (0, 255, 0)
        )

    if (self.use_canvas):
      # self.canvas.SetImage(self.image.convert('RGB'), 0, 0)
      # self.canvas = self.matrix.SwapOnVSync(self.canvas)
      self.send_to_matrix()
      
    else:
      # self.matrix.SetImage(self.image.convert('RGB'))
      self.send_to_matrix()

  def clear(self):
    self.image.paste(0, (0, 0, self.width, self.height))
  

  def send_to_matrix(self):
    
    self.zmq_client.send_image(self.image)

  def network_issue_indicator(self):
    """
    If there is a network issue, draw something on the screen
    """
    # red = self.graphics.Color(255, 0, 0)
    red = (255, 0, 0)
    # self.graphics.DrawLine(self.matrix, 0, self.matrix.height - 1, self.matrix.width, self.matrix.height - 1, red)
    self.draw.line(((0, self.height-1), (self.width, self.height-1)), fill=red)


class MatrixPixels:
    def __init__(self, position, color):
        self.position = position
        self.color = color