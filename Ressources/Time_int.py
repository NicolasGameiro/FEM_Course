# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 23:36:54 2022

@author: ngameiro
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams["figure.figsize"] = (8,6)
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 12
from numpy.linalg import inv

#=== Parameters ===
E = 1e6 # Module D'Young [en Pa]
rho = 7850 # Masse volumique [en kg/m3]
I = 200 #Inertie
S = 0.1 # Section [en m^2]
L = 100 # Longueur d'un element [en m]

#=== Geometry ===
M_elem = rho*S*L/6*np.array([[2,1],
                             [1,2]])

K_elem = E*S/L*np.array([[1,-1],
                         [-1,1]])

def Newmark_scheme(b1,b2,M,K,dt,U,Ud,Udd,f) : 
    # accel
    Udd[:,2] = inv(M+1/2*dt^2*b2*K)*(-K)*(U[:,1]+Ud[:,1]*dt+1/2*dt^2*Udd[:,1]*(1-b2))+f[:,2]
    # vitesse
    Ud[:,2] = U[:,1] + Ud[:,1]*dt + 1/2*dt^2*(Udd[:,1]*(1-b2) + b2*Udd[:,2])
    # position
    U[:,2] = Ud[:,1] + dt*(Udd[:,1]*(1-b1) + b1*Udd[:,1])