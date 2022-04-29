# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 22:09:45 2022

@author: ngameiro
"""

from prettytable import PrettyTable as pt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams["figure.figsize"] = (8,6)
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 12

class Mesh : 
    def __init__(self, node_list = [], element_list = []) :
        self.node_list = np.array(node_list)
        self.element_list = np.array(element_list)
    
    def add_node(self,node) : 
        if len(node) != 2 : 
            print("Error : uncorrect node format")
        else :
            self.node_list = np.append(self.node_list,[node], axis=0)
            print("noeud added")
        print(self.node_list)
    
    def add_element(self, element) : 
        if len(element) != 2 : 
            print("Error : uncorrect element format")
        else :
            self.element_list = np.append(self.element_list,[element], axis=0)
            print("element added")
        print(self.element_list)
        
    def table(self):
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

class FEM_Model() : 
    def __init__(self, mesh) :
        self.mesh = mesh
    
    def test(self) :
        self.mesh.geom()
        
    def __str__(self):
        return "fem solver"
        
if __name__ == "__main__" :
    m1 = Mesh([[0,0],[1,1]],[[1,2]])
    
    m1.add_node([3]) #test erreur
    m1.add_node([2,2])
    m1.add_node([0,1])
    m1.add_element([2,3])
    m1.add_element([3,4])
    m1.table()   
    print(m1)
    #m1.geom()
        
    #FEM solver 
    fem = FEM_Model(m1)
    print(fem)
    fem.test()