# -*- coding: utf-8 -*-

"""
Created : 17/09/2021

@author: Nicolas GAMEIRO

to do :
pip freeze > requirements.txt
"""
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

"""
NL = Node List
EL = Element List
PD = Problem dimension
ENL = Extend Node List
NoN = Number of nodes
"""

import sys

sys.path.append('./src')
from functions import *
from plotting import *

NL = np.array([[0, 0],
               [1, 0],
               [0.5, 1]])

NL = np.array([[0, 0],
               [1, 0],
               [1, 0.5],
               [0, 0.5],
               [1, 3],
               [2,0.5],
               [2,1],
               [3,0.5],
               [3,0],
               [2,0]])

EL = np.array([[1, 2],
               [2, 3],
               [3, 1]])

EL = np.array([[1, 2],
               [2, 3],
               [3, 1],
               [1,4],
               [3,4],
               [4,5],
               [5,3],
               [3,6],
               [6,7],
               [6,10],
               [7,8],
               [8,9],
               [9,10],
               [10,2],
               [3,6],
               [6,9],
               [6,8],
               [3,10]])

filename = "Mesh.txt"
#NL1 = Read_Node_List(filename)

# TODO : creer un generateur de condition limites
DorN = np.array([[-1, -1],
                 [-1, -1],
                 [1, 1]])

E = 10 * 10 ** 9  # Module d'Young (Pa)
l = 0.05  # Largueur (m)
L = 0.05  # longueur (m)
A = L * l  # Section (m^2)
I = 40 # Inertie (m^4)

PD = np.size(NL, 1)
NoN = np.size(NL, 0)
DorN = 1*np.ones([NoN, PD])
print('Dimension of the problem : ', PD)
print('Number of nodes : ', NoN)

U_u = np.zeros([NoN, PD])
Fu = np.zeros([NoN, PD])

Fu = add_force(Fu, node=8, Fx=200, Fy=0)
DorN = add_DorN(DorN, node=1, x=-1, y=-1)
DorN = add_DorN(DorN, node=2, x=-1, y=-1)

fig, axs = plt.subplots(1, 2)
fig.suptitle('Results plot')

# Plot nodes
for i in range(NoN):
    axs[0].scatter(NL[i][0], NL[i][1])
    axs[0].text(NL[i][0], NL[i][1], str(i + 1))
    axs[0].plot([NL[EL[i][0] - 1][0], NL[EL[i][1] - 1][0]], [NL[EL[i][0] - 1][1], NL[EL[i][1] - 1][1]])
# plt.grid()
# plt.savefig('mesh.png')
# plt.show()

plot_forces(axs[0], NL, Fu)

ENL = np.zeros([NoN, 6 * PD])
print("Init Extended Node List :\n", ENL)

ENL[:, 0:PD] = NL[:, :]
ENL[:, PD:2 * PD] = DorN[:, :]

(ENL, DOFs, DOCs) = assign_BCs(NL, ENL)
print("Update Extended Node List :\n", ENL)
print('row : ', np.size(ENL, 0), 'column : ', np.size(ENL, 1))

K = assemble_stiffness(ENL, EL, NL, E, A)

ENL[:, 4 * PD:5 * PD] = U_u[:, :]
ENL[:, 5 * PD:6 * PD] = Fu[:, :]
print("Update Extended Node List :\n", ENL)

U_u = U_u.flatten()
Fu = Fu.flatten()

print('DOFs : ', DOFs, 'DOCs : ', DOCs)
Fp = assemble_force(ENL, NL)
Up = assemble_displacement(ENL, NL)

K_UU = K[0:DOFs, 0:DOFs]
K_UP = K[DOFs, DOFs:DOFs + DOCs]
K_PU = K[DOFs:DOFs + DOCs, 0:DOFs]
K_PP = K[DOFs:DOFs + DOCs, DOFs:DOFs + DOCs]

F = Fp - np.matmul(K_UP, Up)
U_u = np.matmul(np.linalg.inv(K_UU), F)
Fu = np.matmul(K_PU, U_u) + np.matmul(K_PP, Up)

ENL = update_nodes(ENL, U_u, NL, Fu)
print("Final Extended Node List :\n", ENL, np.size(ENL, 1), np.size(ENL, 0))

############################
### Post Processing
############################

scale = 100  # Exaggeration
resolution = 100
coor = []
dispx_array = []
strain_x_array = []
stress_x_array = []

for i in range(np.size(NL, 0)):
    dispx = ENL[i, 8]
    dispy = ENL[i, 9]
    print('U_x = ', dispx, 'U_y = ', dispy)

    # TODO : Calcul de la deformation puis contrainte
    # sigma = E * epsilon avec epsilon = (disp_x - L)/L

    # Calcul de la deformation
    print("traitement de l'element defini par le noeud %s et %s" % (EL[i, 0], EL[i, 1]))
    X1 = ENL[EL[i, 0] - 1, 0]
    X2 = ENL[EL[i, 1] - 1, 0]
    Y1 = ENL[EL[i, 0] - 1, 1]
    Y2 = ENL[EL[i, 1] - 1, 1]
    L = math.sqrt((X2 - X1) ** 2 + (Y1 - Y2) ** 2)
    print('L = ', L)
    strain_x = (dispx - L) / L
    stress_x = E*strain_x
    x = ENL[i, 0] + dispx * scale
    y = ENL[i, 1] + dispy * scale

    strain_x_array.append(strain_x)
    stress_x_array.append(float(stress_x)/10**6)
    dispx_array.append(dispx)
    coor.append(np.array([x, y]))

coor = np.vstack(coor)
dispx_array = np.vstack(dispx_array)
print(dispx_array)
print("Stress (MPa) = \n", stress_x_array)
x_scatter = []
y_scatter = []
color_x = []

for i in range(0, np.size(EL, 0)):
    x1 = coor[EL[i, 0] - 1, 0]
    x2 = coor[EL[i, 1] - 1, 0]
    y1 = coor[EL[i, 0] - 1, 1]
    y2 = coor[EL[i, 1] - 1, 1]

    dispx_EL = np.array([dispx_array[EL[i, 0] - 1], dispx_array[EL[i, 1] - 1]])

    if x1 == x2:
        x = np.linspace(x1, x2, resolution)
        y = np.linspace(y1, y2, resolution)
    else:
        m = (y2 - y1) / (x2 - x1)
        x = np.linspace(x1, x2, resolution)
        y = m * (x - x1) + y1

    x_scatter.append(x)
    y_scatter.append(y)
    print('dispx_El = ', dispx_EL[0], dispx_EL[1])
    color_x.append(np.linspace(np.abs(dispx_EL[0]), np.abs(dispx_EL[1]), resolution))
    # print('color_x = \n', color_x)

x_scatter = np.vstack([x_scatter]).flatten()
y_scatter = np.vstack([y_scatter]).flatten()
color_x = np.vstack([color_x]).flatten()

cmap = plt.get_cmap('jet')
axs[1].scatter(x_scatter, y_scatter, c=color_x, cmap=cmap, s=10, edgecolor='none')

norm_x = Normalize(np.abs(dispx_array.min()), np.abs(dispx_array.max()))
clb = plt.colorbar(ScalarMappable(norm=norm_x, cmap=cmap), orientation="horizontal")
clb.ax.tick_params(labelsize=10)
clb.ax.set_title('displacement', fontsize=12)
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('test/res.png')
plt.show()
