# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 19:28:56 2022

@author: ngameiro
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams["figure.figsize"] = (8,6)
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 12
from numpy.linalg import inv


#=== Usefull fonc ===
    
def Rot(c,s) : 
    Rotation_matrix =  np.array([[c, s , 0 , 0],
                               [-s, c, 0 , 0],
                                [0, 0 ,c,s ],
                                [0, 0, -s, c]])
    return Rotation_matrix

def K_elem(L_e,E,S) :
    K_elem = E*S/L_e*np.array([[1, 0 , -1, 0],
                         [0, 0 , 0, 0],
                        [-1, 0, 1, 0],
                        [0, 0 , 0 , 0]])
    return K_elem

def M_elem(L_e,rho,S) : 
    M_elem = 6*rho*S*L_e*np.array([[1,1,1]])
    return M_elem

def changement_base(P,M) : 
    return P.dot(M).dot(np.transpose(P))

def changement_coord(NL,EL) :
    BB = []
    for i in range(len(EL)) : # Une matrice de changement de coord par element
        #print("generation de la matrice de passage de l'element ", i + 1, ":")
        B = np.zeros([len(NL)*2,4])
        noeud1 = EL[i,0]
        noeud2 = EL[i,1]
        B[(noeud1 - 1)*2, 0] = 1
        B[(noeud1 - 1)*2 + 1 , 1] = 1
        B[(noeud2 - 1)*2 , 2] = 1
        B[(noeud2 - 1)*2 + 1, 3] = 1
        #print(B)
        BB.append(B)
    return BB

def assemblage_2D(BB,NL,EL,E,S) :
    M_global = np.zeros([len(NL)*2,len(NL)*2])
    for i in range(len(EL)) :
        noeud1 = EL[i,0]
        noeud2 = EL[i,1]
        x_1, x_2, y_1, y_2 = NL[noeud1-1,0],NL[noeud2-1,0],NL[noeud1-1,1],NL[noeud2-1,1]
        L_e = np.sqrt((x_2-x_1)**2 + (y_2-y_1)**2)
        c = (x_2-x_1)/L_e
        s = (y_2-y_1)/L_e
        rot = Rot(c,s)
        # rotation matrice elem
        K_rot = rot.dot(K_elem(L_e,E,S)).dot(np.transpose(rot))
        M_global = M_global + changement_base(BB[i],K_rot)
    return M_global

def solve(K_glob,F,BC) :
    K_glob_r = np.transpose(BC).dot(K_glob).dot(BC)
    print("k : ",K_glob_r)
    F_r = np.transpose(BC).dot(F)
    print(F_r)
    U_r = inv(K_glob_r).dot(F_r)
    #try :    
    #except : 
    #print("Attention Matrice singulière (contient un zéro dans ces termes diagonaux). Manque de condition limite")
    print(U_r)
    U = BC.dot(U_r)
    return U

def solver(NL,EL,F,BC,E,S) :
    matrices_de_passage = changement_coord(NL,EL)
    K_glob = assemblage_2D(matrices_de_passage,NL,EL,E,S)
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

def plot_disp(NL,U,scale=100) : 
    x = [x for x in NL[:,0]] #permet de passer np.array à liste
    y = [y for y in NL[:,1]] #permet de passer np.array à liste
    size = 1
    offset = size/4000000.
    plt.figure()
    plt.scatter(x, y, c='y', s=size, zorder=5)
    for i, location in enumerate(zip(x,y)):
        plt.annotate(i+1, (location[0]-offset, location[1]-offset), zorder=10)
    for i in range(len(EL)) :
        xi,xj = NL[EL[i,0]-1,0]+U[EL[i,0]-1]*scale,NL[EL[i,1]-1,0]+U[EL[i,1]-1]*scale
        yi,yj = NL[EL[i,0]-1,1]+U[EL[i,0]]*scale,NL[EL[i,1]-1,1]+U[EL[i,1]]*scale
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
        print(x_scatter,y_scatter)
    plt.figure()
    cmap = plt.get_cmap('jet')
    plt.scatter(x_scatter,y_scatter,c = color,cmap = cmap,s=10, edgecolor = 'none' )
    plt.colorbar(label='disp') #ScalarMappable(norm = norm_x, cmap = cmap ))
    return

def plot_stress(NL,U) :
    x_scatter = []
    y_scatter = []
    color = []
    for i in range(len(EL)) :
        x_scatter.append(np.linspace(NL[EL[i,0]-1,0],NL[EL[i,1]-1,0],100))
        y_scatter.append(np.linspace(NL[EL[i,0]-1,1],NL[EL[i,1]-1,1],100))
        color.append(np.linspace(sigma[EL[i,0]-1],sigma[EL[i,1]-1],100))
    plt.figure()
    cmap = plt.get_cmap('jet')
    plt.scatter(x_scatter,y_scatter,c = color,cmap = cmap,s=10, edgecolor = 'none' )
    plt.colorbar(label='Contrainte (en MPa)') #ScalarMappable(norm = norm_x, cmap = cmap ))
    return