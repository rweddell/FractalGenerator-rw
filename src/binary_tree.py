from __future__ import division
 
import numpy as np
# from scipy import misc
import cv2
import matplotlib.pyplot as plt
 
m = 1920
n = 1080
 
s = int(m*0.65)  # Scale.
x = np.linspace(-m / s, m / s, num=m).reshape((1, m))
y = np.linspace(-n / s, n / s, num=n).reshape((n, 1))
Z = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
 
C = np.full((n, m), -0.4 + 0.6j)
M = np.full((n, m), True, dtype=bool)
N = np.zeros((n, m))
for i in range(256):
    Z[M] = Z[M] * Z[M] + C[M]
    M[np.abs(Z) > 2] = False
    N[M] = i
 
# misc.imsave('julia-m.png', np.flipud(1 - M))
# misc.imsave('julia.png', np.flipud(255 - N))
cv2.imwrite('julia.png', np.flipud(255-N))
# cv2.imwrite('julia-m.png', np.flipud(255-M))
 
# Save with Matplotlib using a colormap.
fig = plt.figure()
fig.set_size_inches(m / 100, n / 100)
ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1)
ax.set_xticks([])
ax.set_yticks([])
plt.imshow(np.flipud(N), cmap='nipy_spectral')
plt.savefig('julia-plt.png')

fig = plt.figure()
fig.set_size_inches(m / 100, n / 100)
ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1)
ax.set_xticks([])
ax.set_yticks([])
plt.imshow(np.flipud(N), cmap='gnuplot2')
plt.savefig('julia-m.png')

plt.close()

def draw_tree(order, theta, sz, posn, heading, color=(0,0,0), depth=0):
  
   # The relative ratio of the trunk to the whole tree  
   trunk_ratio = 0.29     
  
   # Length of the trunk  
   trunk = sz * trunk_ratio
   delta_x = trunk * math.cos(heading)
   delta_y = trunk * math.sin(heading)
   (u, v) = posn
   newpos = (u + delta_x, v + delta_y)
   pygame.draw.line(main_surface, color, posn, newpos)
  
   if order > 0:   # Draw another layer of subtrees
  
      # These next six lines are a simple hack to make 
      # the two major halves of the recursion different 
      # colors. Fiddle here to change colors at other 
      # depths, or when depth is even, or odd, etc.
      if depth == 0:
          color1 = (255, 0, 0)
          color2 = (0, 0, 255)
      else:
          color1 = color
          color2 = color
  
      # make the recursive calls to draw the two subtrees
      newsz = sz*(1 - trunk_ratio)
      draw_tree(order-1, theta, newsz, newpos, heading-theta, color1, depth+1)
      draw_tree(order-1, theta, newsz, newpos, heading+theta, color2, depth+1)
  
  
def main():
    theta = 0
  
    while True:
  
        # Update the angle
        theta += 0.01
  
        # This little part lets us draw the stuffs 
        # in the screen everything
        main_surface.fill((255, 255, 0))
        draw_tree(9, theta, surface_height*0.9, (surface_width//2, surface_width-50), -math.pi/2)
        pygame.display.flip()