# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 22:14:13 2022

@author: ngameiro

source : 
- https://www.youtube.com/watch?v=4YjcUXV_-tI&list=PLX36sAKtIxj0s5VJB6fVfmNe1Sm6-tNwz&index=28
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams["figure.figsize"] = (8,6)
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 12
from numpy.linalg import inv
from prettytable import PrettyTable as pt

def Rot(c,s) : 
    Rotation_matrix =  np.array([[c, s , 0, 0 , 0, 0],
                                 [-s, c, 0, 0 , 0, 0],
                                 [0, 0, 0, 1, 0 , 0],
                                 [0, 0 , 0 ,c ,s , 0 ],
                                 [0, 0, 0, -s, c, 0],
                                 [0, 0, 0, 0, 0 , 1]])
    return Rotation_matrix

def K_elem(L_e,E,S,I) :
    K_elem = E/L_e*np.array([[S, 0, 0 , -S, 0, 0],
                            [0, 12*I/L_e**2 , 6*I/L_e, 0, -12*I/L_e**2, 6*I/L_e],
                            [0, 6*I/L_e , 4*I, 0, -6*I/L_e, 2*I],
                            [-S, 0, 0 , S, 0, 0],
                            [0, -12*I/L_e**2 , -6*I/L_e, 0, 12*I/L_e**2, -6*I/L_e],
                            [0, 6*I/L_e , 2*I, 0, -6*I/L_e, 4*I]])
    return K_elem

def changement_base(P,M) : 
    return P.dot(M).dot(np.transpose(P))

def changement_coord(NL,EL) :
    BB = []
    for i in range(len(EL)) : # Une matrice de changement de coord par element
        #print("generation de la matrice de passage de l'element ", i + 1, ":")
        B = np.zeros([len(NL)*3,6])
        noeud1 = EL[i,0]
        noeud2 = EL[i,1]
        B[(noeud1 - 1)*3, 0] = 1
        B[(noeud1 - 1)*3 + 1 , 1] = 1
        B[(noeud1 - 1)*3 + 2, 2] = 1
        B[(noeud2 - 1)*3 , 3] = 1
        B[(noeud2 - 1)*3 + 1, 4] = 1
        B[(noeud2 - 1)*3 + 2, 5] = 1
        BB.append(B)
    return BB

def assemblage_2D(BB,NL,EL,E,S,I) :
    M_global = np.zeros([len(NL)*3,len(NL)*3])
    for i in range(len(EL)) :
        noeud1 = EL[i,0]
        noeud2 = EL[i,1]
        x_1, x_2, y_1, y_2 = NL[noeud1-1,0],NL[noeud2-1,0],NL[noeud1-1,1],NL[noeud2-1,1]
        L_e = np.sqrt((x_2-x_1)**2 + (y_2-y_1)**2)
        c = (x_2-x_1)/L_e
        s = (y_2-y_1)/L_e
        rot = Rot(c,s)
        # rotation matrice elem
        K_rot = rot.dot(K_elem(L_e,E,S, I)).dot(np.transpose(rot))
        M_global = M_global + changement_base(BB[i],K_rot)
    return M_global

def solver_frame(NL,EL,F,BC,E,S,I) :
    matrices_de_passage = changement_coord(NL,EL)
    K_glob = assemblage_2D(matrices_de_passage,NL,EL,E,S,I)
    K_glob_r = np.transpose(BC).dot(K_glob).dot(BC)
    ### en cas de matrice singuliaire 
    m = 0
    K_glob_r = K_glob_r + np.eye(K_glob_r.shape[1])*m
    ###
    F_r = np.transpose(BC).dot(F)
    U_r = inv(K_glob_r).dot(F_r)
    U = BC.dot(U_r)
    React = K_glob.dot(U) - F
    return U, React

def print_data(NL,EL,F,U,React) : 
    tu = pt()#Add headers
    tr = pt()
    tn = pt()
    te = pt()
    tf = pt()
    tu.field_names = ["Node","X", "Y", "phi"]#Add rows
    tr.field_names = ["Node","Rx", "Ry", "Mz"]
    tn.field_names = ["Node", "X", "Y"]
    te.field_names = ["Element", "Node 1", "Node 2"]
    tf.field_names = ["Node", "Fx", "Fy", "Mz"]
    for i in range(0, len(U), 3) :
        tu.add_row([int(i/3+1), U[i][0], U[i+1][0],U[i+2][0]])
        tr.add_row([int(i/3+1), React[i][0], React[i+1][0],React[i+2][0]])
        tf.add_row([int(i/3+1), F[i][0], F[i+1][0], F[i+2][0]])
    for i in range(len(NL)) : 
        tn.add_row([int(i+1), NL[i][0], NL[i][1]])
    for i in range(len(EL)) : 
        te.add_row([int(i+1), EL[i][0], EL[i][1]])
    print(tu)
    print(tr)
    print(tf)
    print(tn)
    print(te)
    

def gen_bc(NoN,lbc) :
    Nb_ddl = NoN*3
    BC = np.eye(Nb_ddl)
    BC = np.delete(BC,lbc,axis=1)
    return BC

#=== Plotting functions ===
def geom(NL,EL) : 
    x = [x for x in NL[:,0]]
    y = [y for y in NL[:,1]]
    size = 200
    offset = size/40000.
    plt.scatter(x, y, c='y', s=size, zorder=5)
    for i, location in enumerate(zip(x,y)):
        plt.annotate(i+1, (location[0]-offset, location[1]-offset), zorder=10)
    for i in range(len(EL)) :
        xi,xj = NL[EL[i,0]-1,0],NL[EL[i,1]-1,0]
        yi,yj = NL[EL[i,0]-1,1],NL[EL[i,1]-1,1]
        plt.plot([xi,xj],[yi,yj],color = 'k', lw = 1, linestyle = '--')
    plt.axis('equal')
    
def plot_disp_f(NL,EL,U,scale=100,r=100) :
    x_scatter = []
    y_scatter = []
    color = []
    for i in range(len(EL)) :
        x_scatter.append(np.linspace(NL[EL[i,0]-1,0],NL[EL[i,1]-1,0],r))
        y_scatter.append(np.linspace(NL[EL[i,0]-1,1]+U[(EL[i,0]-1)*2]*scale,NL[EL[i,1]-1,1]+U[(EL[i,1]-1)*2]*scale,r))
        color.append(np.linspace(U[(EL[i,0]-1)*2],U[(EL[i,1]-1)*2],r))
    plt.figure()
    cmap = plt.get_cmap('jet')
    plt.scatter(x_scatter,y_scatter,c = color,cmap = cmap,s=10, edgecolor = 'none' )
    plt.colorbar(label='disp') #ScalarMappable(norm = norm_x, cmap = cmap ))
    return