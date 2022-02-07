import turtle as t
import numpy as np
import matplotlib.pyplot as plt
from random import randint


def koch_fract(turtle, divis, size):
   if(divis == 0):
      turtle.forward(size)
   else:
      for angle in [60, -120, 60, 0]:
         koch_fract(turtle, divis - 1, size / 3)               
         turtle.left(angle)

def binary_tree(t, branch_length, shorten_by, angle, min_branch_len=5):
  if branch_length > min_branch_len:
    t.forward(branch_length)
    new_length = branch_length - shorten_by
    t.left(angle)
    binary_tree(t, new_length, shorten_by, angle)
    t.right(angle * 2)
    binary_tree(t, new_length, shorten_by, angle)
    t.left(angle)
    t.backward(branch_length)

def barnsely_fern():

    x = [0]
    y = [0]
    for i in range(0, 50000): 
    
        p = randint(1, 100) 
        
        if p == 1: 
            x.append(0) 
            y.append(0.16*(y[i])) 
            
        if p >= 2 and p <= 86: 
            x.append(0.85*(x[i]) + 0.04*(y[i])) 
            y.append(-0.04*(x[i]) + 0.85*(y[i])+1.6) 
        
        if p >= 87 and p <= 93: 
            x.append(0.2*(x[i]) - 0.26*(y[i])) 
            y.append(0.23*(x[i]) + 0.22*(y[i])+1.6) 
            
        if p >= 94 and p <= 100: 
            x.append(-0.15*(x[i]) + 0.28*(y[i])) 
            y.append(0.26*(x[i]) + 0.24*(y[i])+0.44)




def mandelbrot_set(x, y):

    def mandelbrot(c, z, iterations=4):
        count_m = 0
        for a in range(iterations):
            z = z**2 + c
            count_m += 1        
            if(abs(z) > 4):
                break
        return count_m

    m = np.zeros((len(x), len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            c = complex(x[i], y[j])
            z = complex(0, 0)
            count = mandelbrot(c, z)
            m[i, j] = count    
            
    return m