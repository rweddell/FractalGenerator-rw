import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import numpy as np
from datetime import datetime
import cv2
import matplotlib.pyplot as plt
import os


def mandelbrot_set(x_dim, y_dim):

    max_iter = 120
    re_start = -2
    re_end = 1
    im_start = -1
    im_end = 1

    image = np.zeros((x_dim, y_dim))

    def mandelbrot_fractal(comp, max_iter):
        z = 0
        n = 0
        while abs(z) <= 2 and n < max_iter:
            z = z*z + comp
            n += 1
        return n
    
    for x in range(x_dim):
        for y in range(y_dim):
            c = complex(re_start+(x/x_dim)*(re_end - re_start),
                im_start+(y/y_dim)*(im_end-im_start))
            m = mandelbrot_fractal(c, max_iter)
            image[x][y] = 255 - int(m*255/max_iter)
            # image[x][y][1] = 127 - int(m*255/max_iter)
            # image[x][y][2] = 0 - int(m*255/max_iter)

    return image

m=1920
n=1080
image = mandelbrot_set(m, n)

# Save with Matplotlib using a colormap.
fig = plt.figure()
fig.set_size_inches(m / 100, n / 100)
ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1)
ax.set_xticks([])
ax.set_yticks([])
plt.imshow(np.flipud(image), cmap='nipy_spectral')
plt.savefig('mandelbrot-plt.png')

fig = plt.figure()
fig.set_size_inches(m / 100, n / 100)
ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1)
ax.set_xticks([])
ax.set_yticks([])
plt.imshow(np.flipud(image), cmap='gnuplot2')
plt.savefig('mandelbrot-m.png')

plt.close()