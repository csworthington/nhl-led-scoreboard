#!/usr/bin/env python
from testbase import TestBase
import time


class GrayscaleBlock(TestBase):
    def __init__(self, *args, **kwargs):
        super(GrayscaleBlock, self).__init__(*args, **kwargs)

    def run(self):
        sub_blocks = 16
        # width = self.matrix.width
        # height = self.matrix.height
        width = self.matrixWrapper._getPanelWidth()
        height = self.matrixWrapper._getPanelHeight()
        x_step = max(1, width / sub_blocks)
        y_step = max(1, height / sub_blocks)
        count = 0

        while True:
            for y in range(0, height):
                for x in range(0, width):
                    c = sub_blocks * int(y / y_step) + int(x / x_step)
                    if count % 4 == 0:
                        # self.matrix.SetPixel(x, y, c, c, c)
                        self.matrixWrapper._SetPixel(x, y, c, c, c)
                        # self.matrixWrapper._SetPixel(x, y, c, c, c, panel_offset=1)
                    elif count % 4 == 1:
                        self.matrixWrapper._SetPixel(x, y, c, 0, 0)
                        # self.matrixWrapper._SetPixel(x, y, c, 0, 0, panel_offset=1)
                    elif count % 4 == 2:
                        self.matrixWrapper._SetPixel(x, y, 0, c, 0)
                        # self.matrixWrapper._SetPixel(x, y, 0, c, 0, panel_offset=1)
                    elif count % 4 == 3:
                        self.matrixWrapper._SetPixel(x, y, 0, 0, c)
                        # self.matrixWrapper._SetPixel(x, y, 0, 0, c, panel_offset=1)

            count += 1
            time.sleep(2)


# Main function
if __name__ == "__main__":
    grayscale_block = GrayscaleBlock(num_panels=2)
    if (not grayscale_block.process()):
        grayscale_block.print_help()
