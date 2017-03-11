"""Displays output from the fractal module within a notebook or hydrogen using jupyter."""

import IPython.display
from fractal import Fractal

def display(f):
    """Render and displays the fractal into jupyter (ipython) for jupyter notebooks or hydrogen."""
    buf = io.BytesIO()
    f.render().save(buf, 'PNG')
    img = IPython.display.Image(data = buf.getvalue())
    IPython.display.display(img)

f = Fractal()
display(f)
