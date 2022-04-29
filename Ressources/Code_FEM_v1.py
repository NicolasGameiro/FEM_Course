# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 23:38:15 2022

@author: ngameiro
"""

from fcn import *
#import seaborn as sns;sns.set_style("whitegrid")



#=== Parameters ===
E = 1e6 # Module D'Young [en Pa]
rho = 7850 # Masse volumique [en kg/m3]
S = 0.1 # Section [en m^2]
L = 100 # Longueur d'un element [en m]

#=== Geometry ===
cas = 2

if cas == 1 : 
    NL = np.array([[0,0],
              [.5,0],
              [1,0]])
    EL = np.array([[1,2],
              [2,3]])
elif cas == 2 :
    a = 100
    NL = np.array([[0,0],
              [a,0],
              [a/2,a*np.sqrt(3)/2]])
    EL = np.array([[1,2],
              [2,3],
                [1,3]])

NoN = len(NL) # Nombre de noeuds
NoE = len(EL) # Nombre d'elements
print("Nombre de noeuds :", NoN)
print("Nombre de elements :", NoE)
geom(NL,EL)

#=== BCs ===
F = np.array([[0,0],
             [0,0],
             [100,0]])

F = np.vstack(F.flatten())

BC1 = np.array([[0,0,0,0],
               [0,0,0,0],
               [1,0,0,0],
               [0,1,0,0],
               [0,0,1,0],
               [0,0,0,1]])

BC2 = np.array([[0,0],
               [0,0],
               [0,0],
               [0,0],
               [1,0],
               [0,1]])

BC3 = np.array([[0,0,0],
               [0,0,0],
               [0,0,0],
               [1,0,0],
               [0,1,0],
               [0,0,1]])

#=== Solver ===
U, React = solver(NL,EL,F,BC2,E,S)
print(U)

# plt.figure()
# plt.spy(K_glob_r,marker=None,markersize=4)
# plt.show()

# ax = sns.heatmap(K_glob_r, annot=True, cbar=None, xticklabels=False, yticklabels=False)
# plt.title("Matrice de raideur réduite : ",fontsize=12)
# plt.show()


### Etape 9 : Calcul des contraintes
# On recalcule les déplacements locaux
#u = R(0).dot(U[0:4])
#f = K_elem.dot(u)

plot_disp_f(NL,EL,U)

affiche = 0
if affiche == 1 : 
    print("K_glob \n :",K_glob_r)
    print("F \n :",F_r)
    print("Deplacement : \n", U_r)
    print("Deplacement : \n", U)
    print("Reaction : \n", React)
    plot_disp(NL,U,scale=100)
    plot_disp_f(NL,U)