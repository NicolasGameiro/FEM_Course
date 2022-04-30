# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 23:38:15 2022

@author: ngameiro
"""

from fcn_frame import *
#import seaborn as sns;sns.set_style("whitegrid")

#=== Parameters ===
E = 1e6 # Module D'Young [en Pa]
rho = 7850 # Masse volumique [en kg/m3]
I = 200 #Inertie
S = 0.1 # Section [en m^2]
L = 100 # Longueur d'un element [en m]

#=== Geometry ===
cas = 4

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
elif cas == 3 :
    NL = np.array([[0,0],
              [.5,0],
              [1,0]])
    EL = np.array([[1,2],
              [2,3]])
elif cas == 4 : 
    portee = 4.5
    h_archi = 8
    h_mur = 4.5
    h_ferme = h_archi - h_mur
    NL = np.array([[0,0],
                   [portee,0],
                   [portee/2,h_ferme],
                   [portee/2,0]])
    EL = np.array([[1,4],
                   [4,2],
                   [2,3],
                   [3,4],
                   [3,1]])

NoN = len(NL) # Nombre de noeuds
NoE = len(EL) # Nombre d'elements
print("Nombre de noeuds :", NoN)
print("Nombre de elements :", NoE)
geom(NL,EL)

#=== BCs ===
if cas == 2 : 
    F = np.array([[0, 0, 0],
                  [0, 0, 0],
                  [100,0,0]])
elif cas == 3 :
    F = np.array([[0, 0, 0],
                  [0, 0, 0],
                  [100,100,0]])
elif cas == 4 : 
    F = np.array([[0, 0, 0],
                  [0, 0, 0],
                  [100,0,0],
                  [0, 0, 0]])

F = np.vstack(F.flatten())

BC2 = gen_bc(NoN, lbc = [0,1,2,3,4,5])

BC3 = np.array([[0,0],
               [0,0],
               [0,0],
               [0,0],
               [0,0],
               [0,0],
               [1,0],
               [0,1],
               [0,0]])

BC4 = np.array([[0,0,0,0,0,0],
               [0,0,0,0,0,0],
               [0,0,0,0,0,0],
               [1,0,0,0,0,0],
               [0,1,0,0,0,0],
               [0,0,1,0,0,0],
               [0,0,0,1,0,0],
               [0,0,0,0,1,0],
               [0,0,0,0,0,1]])

BC5 = gen_bc(NoN, [0,1,2,4])

#=== Solver ===
U, React = solver_frame(NL,EL,F,BC5,E,S,I)
print_data(NL,EL,F,U,React)

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

