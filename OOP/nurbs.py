# -*- coding: utf-8 -*-
"""
Created on Fri May 13 00:05:13 2022

@author: ngameiro
"""

from geomdl import fitting
from geomdl.visualization import VisMPL as vis

# The NURBS Book Ex9.1
points = ((0, 0), (1, 0), (2, 1), (3, 0), (4, 0))
degree = 3  # cubic curve

# Do global curve interpolation
curve = fitting.interpolate_curve(points, degree)

# Plot the interpolated curve
curve.delta = 0.01
curve.vis = vis.VisCurve2D()
curve.render()