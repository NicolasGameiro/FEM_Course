# -*- coding: utf-8 -*-
"""
Created on Mon May  2 19:35:06 2022

@author: ngameiro
"""

from numpy.linalg import inv
import numpy as np
import matplotlib.pyplot as plt

X = [0, 1]
Y = [1, 1]
Yp = [-0.1, 0.1]

node1 = [0, 1, 0.1]
node2 = [1, 1, -2]

def interpol(node1,node2) : 
    x1 = node1[0]
    x2 = node2[0]
    x3 = x1
    x4 = x2
    y1 = node1[1]
    y2 = node2[1]
    y3 = node1[2]
    y4 = node2[2]
    V = np.array([[1, x1, x1**2, x1**3],
                  [1, x2, x2**2, x2**3],
                  [0,1, 2*x3, 3*x3**2],
                  [0,1, 2*x4, 3*x4**2]])
    R = np.array([y1,y2,y3,y4])
    R = np.vstack(R)
    P = np.hstack(inv(V).dot(R))
    P = P[::-1]
    p = np.poly1d([x for x in P])
    x = np.linspace(X[0],X[1],100)
    y = p(x)
    return x,y


x,y = interpol(node1,node2)


plt.figure()
size = 10
plt.scatter(x, y, c='b', s=size, zorder=5)
plt.axis('equal')
plt.grid()