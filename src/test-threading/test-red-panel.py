#!/usr/bin/env python
from testrenderer import TestRenderer


class PulsingColors(TestRenderer):
    def __init__(self, *args, **kwargs):
        super(PulsingColors, self).__init__(*args, **kwargs)

    def run(self):
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        continuum = 0

        red = 255
        green = 0
        blue = 0

        while True:
          self.usleep(50 * 1000)

          if (red == 255):
            red = 0
            green = 255
          elif (green == 255):
            green = 0
            blue = 255
          elif (blue == 255):
            blue = 0
            red = 255

          

          self.offscreen_canvas.Fill(red, green, blue)
          self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

        # while True:
        #     self.usleep(5 * 1000)
        #     continuum += 1
        #     continuum %= 3 * 255

        #     red = 0
        #     green = 0
        #     blue = 0

        #     if continuum <= 255:
        #         c = continuum
        #         blue = 255 - c
        #         red = c
        #     elif continuum > 255 and continuum <= 511:
        #         c = continuum - 256
        #         red = 255 - c
        #         green = c
        #     else:
        #         c = continuum - 512
        #         green = 255 - c
        #         blue = c

        #     self.offscreen_canvas.Fill(red, green, blue)
        #     self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

# Main function
if __name__ == "__main__":
    pulsing_colors = PulsingColors()
    if (not pulsing_colors.process()):
        pulsing_colors.print_help()
