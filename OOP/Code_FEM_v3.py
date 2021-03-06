# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 22:09:45 2022

@author: ngameiro
"""

from prettytable import PrettyTable as pt
import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams["figure.figsize"] = (8,6)
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 12

class Mesh : 
    def __init__(self, node_list = [], element_list = [], h = 0.22, b = 0.10) :
        self.node_list = np.array(node_list)
        self.element_list = np.array(element_list)
        self.S = h*b
        self.Iy = b*h**3/12
        self.Iz = h*b**3/12
    
    def add_node(self,node) : 
        if len(node) != 2 : 
            print("Error : uncorrect node format")
        else :
            self.node_list = np.append(self.node_list,[node], axis=0)
            print("noeud added")
    
    def add_element(self, element) : 
        if len(element) != 2 : 
            print("Error : uncorrect element format")
        else :
            self.element_list = np.append(self.element_list,[element], axis=0)
            print("element added")
        
    def node_table(self):
        tab = pt()
        tab.field_names = ["Node","X", "Y"]#Add rows
        for i in range(len(self.node_list)) : 
            tab.add_row([int(i+1), self.node_list[i,0], self.node_list[i,1]])
        print(tab)
    
    def __str__(self):
        return f""" Information sur le maillage : \n
    - Nombre de noeuds : {len(self.node_list)}\n 
    - Nombre d'éléments : {len(self.element_list)}
    """
    #=== Plotting functions ===
    def geom(self) : 
        x = [x for x in self.node_list[:,0]]
        y = [y for y in self.node_list[:,1]]
        size = 200
        offset = size/40000.
        plt.scatter(x, y, c='y', s=size, zorder=5)
        for i, location in enumerate(zip(x,y)):
            plt.annotate(i+1, (location[0]-offset, location[1]-offset), zorder=10)
        for i in range(len(self.element_list)) :
            xi,xj = self.node_list[self.element_list[i,0]-1,0],self.node_list[self.element_list[i,1]-1,0]
            yi,yj = self.node_list[self.element_list[i,0]-1,1],self.node_list[self.element_list[i,1]-1,1]
            plt.plot([xi,xj],[yi,yj],color = 'k', lw = 1, linestyle = '--')
        plt.axis('equal')
        plt.grid()

class FEM_Model() : 
    def __init__(self, mesh, E = 2.1E11) :
        self.mesh = mesh
        self.E = E
        self.load = np.zeros([len(self.mesh.node_list),3])
        self.bc = np.eye(len(self.mesh.node_list)*3)
        self.U = np.zeros(len(self.mesh.node_list)*3)
        self.React = np.zeros(len(self.mesh.node_list)*3)
        self.lbc = []
    
    def test(self) :
        self.mesh.geom()
        
    def apply_load(self,node_load,node):
        if len(node_load) != 3 : 
            print("Error : uncorrect load format (must be 3 elements Fx, Fy and Mz)")
        elif node > len(self.mesh.node_list) :
            print("Error : node specified not in the mesh")
        else :
            self.load[node-1,:] = node_load
            print("nodal load applied")
            print(self.load)
            print("==============")
    
    def apply_bc(self,node_bc,node):
        if len(node_bc) != 3 : 
            print("Error : uncorrect bc format (must be 3 elements Fx, Fy and Mz)")
        elif node > len(self.mesh.node_list) :
            print("Error : node specified not in the mesh")
        else :
            for i in range(len(node_bc)) : 
                if node_bc[i] == 1 : 
                    self.lbc.append(i+3*(node-1))
            print("boundary condition applied")
            print(self.lbc)
            print("==============")
    
    def Rot(self,c,s) : 
        Rotation_matrix =  np.array([[c, s , 0, 0 , 0, 0],
                                     [-s, c, 0, 0 , 0, 0],
                                     [0, 0, 1, 0, 0 , 0],
                                     [0, 0 , 0 ,c ,s , 0 ],
                                     [0, 0, 0, -s, c, 0],
                                     [0, 0, 0, 0, 0 , 1]])
        return Rotation_matrix
    
    def K_elem(self,L_e) :
        S = self.mesh.S
        I = self.mesh.Iy
        K_elem = self.E/L_e*np.array([[S, 0, 0 , -S, 0, 0],
                                    [0, 12*I/L_e**2 , 6*I/L_e, 0, -12*I/L_e**2, 6*I/L_e],
                                    [0, 6*I/L_e , 4*I, 0, -6*I/L_e, 2*I],
                                    [-S, 0, 0 , S, 0, 0],
                                    [0, -12*I/L_e**2 , -6*I/L_e, 0, 12*I/L_e**2, -6*I/L_e],
                                    [0, 6*I/L_e , 2*I, 0, -6*I/L_e, 4*I]])
        return K_elem
    
    def changement_base(self,P,M) : 
        return P.dot(M).dot(np.transpose(P))

    def changement_coord(self) :
        BB = []
        for i in range(len(self.mesh.element_list)) : # Une matrice de changement de coord par element
            #print("generation de la matrice de passage de l'element ", i + 1, ":")
            B = np.zeros([len(self.mesh.node_list)*3,6])
            noeud1 = self.mesh.element_list[i,0]
            noeud2 = self.mesh.element_list[i,1]
            B[(noeud1 - 1)*3, 0] = 1
            B[(noeud1 - 1)*3 + 1 , 1] = 1
            B[(noeud1 - 1)*3 + 2, 2] = 1
            B[(noeud2 - 1)*3 , 3] = 1
            B[(noeud2 - 1)*3 + 1, 4] = 1
            B[(noeud2 - 1)*3 + 2, 5] = 1
            BB.append(B)
        return BB

    def assemblage_2D(self) :
        BB = self.changement_coord()
        NL = self.mesh.node_list
        EL = self.mesh.element_list
        M_global = np.zeros([len(NL)*3,len(NL)*3])
        for i in range(len(EL)) :
            noeud1 = EL[i,0]
            noeud2 = EL[i,1]
            x_1, x_2, y_1, y_2 = NL[noeud1-1,0],NL[noeud2-1,0],NL[noeud1-1,1],NL[noeud2-1,1]
            L_e = np.sqrt((x_2-x_1)**2 + (y_2-y_1)**2)
            c = (x_2-x_1)/L_e
            s = (y_2-y_1)/L_e
            rot = self.Rot(c,s)
            # rotation matrice elem
            K_rot = rot.dot(self.K_elem(L_e)).dot(np.transpose(rot))
            M_global = M_global + self.changement_base(BB[i],K_rot)
        return M_global

    def solver_frame(self) :
        self.bc = np.delete(self.bc,self.lbc,axis=1)
        K_glob = self.assemblage_2D()
        K_glob_r = np.transpose(self.bc).dot(K_glob).dot(self.bc)
        ### en cas de matrice singuliaire 
        m = 0
        K_glob_r = K_glob_r + np.eye(K_glob_r.shape[1])*m
        ###
        F = np.vstack(self.load.flatten())
        F_r = np.transpose(self.bc).dot(F)
        U_r = inv(K_glob_r).dot(F_r)
        self.U = self.bc.dot(U_r)
        self.React = K_glob.dot(self.U) - F
    
    def get_res(self):
        return self.U, self.React
    
    def plot_disp_f(self,scale=1e6,r=150,dir='x') :
        NL = self.mesh.node_list
        EL = self.mesh.element_list
        U = self.U
        x_scatter = []
        y_scatter = []
        color = []
        for i in range(len(EL)) :
            xi,xj = NL[EL[i,0]-1,0],NL[EL[i,1]-1,0]
            yi,yj = NL[EL[i,0]-1,1],NL[EL[i,1]-1,1]
            plt.plot([xi,xj],[yi,yj],color = 'k', lw = 1, linestyle = '--')
        for i in range(len(EL)) :
            if dir == 'y' : 
                x_scatter.append(np.linspace(NL[EL[i,0]-1,0],NL[EL[i,1]-1,0],r))
                y_scatter.append(np.linspace(NL[EL[i,0]-1,1]+U[(EL[i,0]-1)*3+1]*scale,NL[EL[i,1]-1,1]+U[(EL[i,1]-1)*3+1]*scale,r))
                color.append(np.linspace(U[(EL[i,0]-1)*3+1],U[(EL[i,1]-1)*3+1],r))
            elif dir == "x" : 
                x_scatter.append(np.linspace(NL[EL[i,0]-1,0]+U[(EL[i,0]-1)*3]*scale,NL[EL[i,1]-1,0]+U[(EL[i,1]-1)*3]*scale,r))
                y_scatter.append(np.linspace(NL[EL[i,0]-1,1],NL[EL[i,1]-1,1],r))
                color.append(np.linspace(U[(EL[i,0]-1)*3],U[(EL[i,1]-1)*3],r))
            elif dir == "sum" : 
                x_scatter.append(np.linspace(NL[EL[i,0]-1,0]+U[(EL[i,0]-1)*3]*scale,NL[EL[i,1]-1,0]+U[(EL[i,1]-1)*3]*scale,r))
                y_scatter.append(np.linspace(NL[EL[i,0]-1,1]+U[(EL[i,0]-1)*3+1]*scale,NL[EL[i,1]-1,1]+U[(EL[i,1]-1)*3+1]*scale,r))
                color.append(np.linspace(U[(EL[i,0]-1)*3]+U[(EL[i,0]-1)*3+1],U[(EL[i,1]-1)*3]+U[(EL[i,1]-1)*3+1],r))
        plt.figure()
        #Permet de reverse la barre de couleur si max negatif 
        if min(U) > 0 :
            cmap = plt.get_cmap('jet')
        elif min(U) <= 0 : 
            cmap = plt.get_cmap('jet_r')
        plt.scatter(x_scatter,y_scatter,c = color,cmap = cmap,s=10, edgecolor = 'none' )
        plt.colorbar(label='disp') #ScalarMappable(norm = norm_x, cmap = cmap ))
        plt.axis('equal')
        return
        
    def __str__(self):
        return "fem solver"
    
def test_simpe() : 
    mesh = Mesh([[0,0],[2,0]],[[1,2]])
    mesh.add_node([4,0])
    mesh.add_node([2,3])
    mesh.add_element([2,3])
    mesh.add_element([3,4])
    mesh.add_element([4,1])
    mesh.add_element([4,2])
    mesh.geom()
    mesh.node_table()
    
    f = FEM_Model(mesh)
    f.apply_load([0,-100,0],4)
    f.apply_bc([1,1,1],1)
    f.apply_bc([0,1,0],3)
    #TODO : attention comme la matrice de bc change les noeuds changent de position !
    f.solver_frame()
    U, React = f.get_res()
    print(U)
    f.plot_disp_f(dir='x')
    f.plot_disp_f(dir='y')
    f.plot_disp_f(dir='sum')
    return 

def test_ferme_tradi() : 
    mesh = Mesh([[0,0],[2,0]],[[1,2]])
    mesh.add_node([4,0])
    mesh.add_node([2,3])
    mesh.add_node([2,1])
    mesh.add_node([3,1.5])
    mesh.add_node([1,1.5])
    mesh.add_element([2,3])
    mesh.add_element([3,4])
    mesh.add_element([4,1])
    mesh.add_element([4,5])
    mesh.add_element([5,2])
    mesh.add_element([5,6])
    mesh.add_element([5,7])
    mesh.geom()
    mesh.node_table()
    
    f = FEM_Model(mesh)
    f.apply_load([0,-100,0],4)
    f.apply_bc([1,1,1],1)
    f.apply_bc([0,1,0],3)
    #TODO : attention comme la matrice de bc change les noeuds changent de position !
    f.solver_frame()
    U, React = f.get_res()
    print(U)
    f.plot_disp_f(dir='x')
    f.plot_disp_f(dir='y')
    f.plot_disp_f(dir='sum')
    return 
        
        
if __name__ == "__main__" :
    test_ferme_tradi() 