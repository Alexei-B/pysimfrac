import numpy as np
import math
import io
import PIL.Image
import IPython.display

class Fractal:

    ln2 = abs(math.log(2))

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

    def __init__(self, width = 320, height = 240, iterations = 100):
        self.width = width
        self.height = height
        self.ratio = height / width
        self.max_iterations = iterations
        self.pos = [0.0, 0.0]
        self.scale = 1
        self.paspread = 2

    def move(self, x, y):
        self.pos[0] += x * self.scale
        self.pos[1] -= y * self.scale

    def zoom(self, factor):
        self.scale /= factor

    def interpolate_number(self, i, x, y):
        return i * (y - x) + x

    def interpolate_pallet(self, i, x, y):
        cx = self.pallet[x % len(self.pallet)]
        cy = self.pallet[y % len(self.pallet)]
        return [int(self.interpolate_number(i, cx[n], cy[n])) for n in range(3)]

    def map_coords(self, a, b):
        return (a / self.width  - 1/2) * self.scale              * 4 + self.pos[0], \
               (b / self.height - 1/2) * self.scale * self.ratio * 4 + self.pos[1]

    def linearize(self, zn):
        return abs(math.log(abs(math.log(abs(zn)) / self.ln2)) / self.ln2)

    def mandelbrot_fn(self, x, y, mi):
        c = z = complex(x, y)
        it = mi

        for n in range(mi):
            z = z*z + c

            if z.real * z.real + z.imag * z.imag > (1 << 16):
                it = (n + 1 - self.linearize(z)) / self.paspread
                break

        return self.interpolate_pallet(it % 1, int(it), int(it + 1))

    def mandelbrot(self):
        return [self.mandelbrot_fn(*self.map_coords(x, y), self.max_iterations) for y in range(self.height) for x in range(self.width)]

    def render(self):
        raw = self.mandelbrot()
        pixels = [raw[l:l + self.width] for l in range(0, len(raw), self.width)];
        return PIL.Image.fromarray(np.uint8(pixels))

    def display(self):
        buf = io.BytesIO()
        self.render().save(buf, 'PNG')
        img = IPython.display.Image(data = buf.getvalue())
        IPython.display.display(img)

if __name__ == '__main__':
    f = Fractal(320, 260)
    f.display()
