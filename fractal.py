"""
Renders images of fractals from the complex plain.

Currently Supports: Mandelbrot
The images are rendered as PIL images.
"""
import numpy as np
import math
import io
import PIL.Image

class Fractal:
    """Renders Pillow images of fractals."""

    # Simple pallet based on solarized.
    pallet = [
        [0x00, 0x2b, 0x36],
        [0x07, 0x36, 0x42],
        [0x58, 0x6e, 0x75],
        [0x65, 0x7b, 0x83],
        [0x83, 0x94, 0x96],
        [0x93, 0xa1, 0xa1],
        [0xee, 0xe8, 0xd5],
        [0xfd, 0xf6, 0xe3],
        [0xee, 0xe8, 0xd5],
        [0x93, 0xa1, 0xa1],
        [0x83, 0x94, 0x96],
        [0x65, 0x7b, 0x83],
        [0x58, 0x6e, 0x75],
        [0x07, 0x36, 0x42],
        [0x00, 0x2b, 0x36]
    ]

    def __init__(self, width = 320, height = 260, iterations = 80):
        """Construct a Fractal renderer with a default image size of 320x260 at 80 max iterations."""
        self.width = width
        self.height = height
        self.ratio = height / width
        self.max_iterations = iterations
        self.pos = [0.0, 0.0]
        self.scale = 1
        self.paspread = 2

    def move(self, x, y):
        """Move the render view relative to the current scale."""
        self.pos[0] += x * self.scale
        self.pos[1] -= y * self.scale

    def zoom(self, factor):
        """Scale the render view relative to the current scale."""
        if factor <= 0:
            return

        self.scale /= factor

    def interpolate_number(self, i, x, y):
        """Calculate a linear interpolation from x to y by i where i is between 0 and 1."""
        return i * (y - x) + x

    def interpolate_pallet(self, i, x, y):
        """Interpolate pallet colours based on i."""
        cx = self.pallet[x % len(self.pallet)]
        cy = self.pallet[y % len(self.pallet)]
        return [int(self.interpolate_number(i, cx[n], cy[n])) for n in range(3)]

    def map_coords(self, a, b):
        """Map image space coordinates to complex space coordinates, accounting for image ratio."""
        return (a / self.width  - 1/2) * self.scale              * 4 + self.pos[0], \
               (b / self.height - 1/2) * self.scale * self.ratio * 4 + self.pos[1]

    def normalize(self, zn):
        """Smooth the output of the Mandelbrot function for colour selection."""
        return abs(math.log(abs(math.log(abs(zn))), 2))

    def mandelbrot_fn(self, x, y, mi):
        """Calculate the Mandelbrot set member for the complex number x + yi, to maximum iterations mi."""
        c = z = complex(x, y)
        it = mi

        for n in range(mi):
            z = z*z + c

            if z.real * z.real + z.imag * z.imag > (1 << 16):
                it = (n + 1 - self.normalize(z)) / self.paspread
                break

        return self.interpolate_pallet(it % 1, int(it), int(it + 1))

    def mandelbrot(self):
        """Calculate the Mandelbrot set for the current render view."""
        return [self.mandelbrot_fn(*self.map_coords(x, y), self.max_iterations) for y in range(self.height) for x in range(self.width)]

    def render(self):
        """Render the fractal for the current render view."""
        raw = self.mandelbrot()
        pixels = [raw[l:l + self.width] for l in range(0, len(raw), self.width)];
        return PIL.Image.fromarray(np.uint8(pixels))
