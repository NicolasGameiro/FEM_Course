# -*- coding: utf-8 -*-
"""
Created on Wed May 11 18:23:33 2022

@author: ngameiro
"""

import bpy
import csv
import numpy as np
from numpy import genfromtxt
import mathutils
import math
from mathutils import Matrix

def importdata(v_path, e_path, c_path) : 
    vertices = genfromtxt(v_path, delimiter = ',')
    edges = genfromtxt(e_path, delimiter = ',')
    color = genfromtxt(c_path, delimiter = ',')
    return vertices, edges, color

def calculateRatationMatrix(posI,posJ) : 
    R = np.identity(4)
    ix = posI[0]
    iy = posI[1]
    iz = posI[2]
    jx = posJ[0]
    jy = posJ[1]
    jz = posJ[2]
    
    dx = jx - ix
    dy = jy - iy
    dz = jz - iz
    length = math.sqrt(dx**2 + dy**2 + dz**2)
    
    if (abs(dx)<0.001 and abs(dy)<0.001) : 
        #Element is vertical - offset in positive global x to define a local z-x plane
        i_offset = np.array([ix+1,iy,iz])
        j_offset = np.array([jx+1,jy,jz])
    else : 
        #Member is not vertical 
        i_offset = np.array([ix,iy,iz+1])
        j_offset = np.array([jx,jy,jz+1])
    node_k = i_offset + 0.5*(j_offset - i_offset)
    
    local_z_vector = np.array(posI) - np.array(posJ)
    local_z_unit = local_z_vector/length
    
    vector_in_plane = node_k - posI
    local_x_vector = vector_in_plane - np.dot(vector_in_plane,local_z_unit)*local_z_unit
    magX = math.sqrt(local_x_vector[0]**2 + local_x_vector[1]**2 + local_x_vector[2]**2)
    local_x_unit = local_x_vector/magX
    
    local_y_unit = np.cross(local_z_unit,local_x_unit)
    
    rotationMatrix = np.array([local_x_unit, local_y_unit, local_z_unit]).T
    
    R[0:3,0:3] = rotationMatrix
    return Matrix(R), length

def calculateTransformationMatrix(posI,posJ) : 
    offset = posI  + 0.5*(posJ - posI).T
    transMatrix = Matrix.Translation(offset)
    return transMatrix

def generateElement(scale , length , num , forceMag) : 
    bpy.ops.mesh.primitive_cylinder_add(
         vertices = 4 ,
         radius = scale ,
         depth = length ,
         enter_editmode = False ,
         align = "WORLD" ,
         location = (v[0], v[1], v[2]) ,
         scale = (1 , 1 ,1)
         )
    bpy.ops.object.shade_smooth()
    ico = bpy.context..object
    ico.name = 'Node ' + str(num)
    return ico

def 