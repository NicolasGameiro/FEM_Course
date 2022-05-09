# -*- coding: utf-8 -*-
"""
Created on Tue May  3 18:30:38 2022

@author: ngameiro
"""

import PySimpleGUI as sg
import numpy as np
from matplotlib.widgets import RectangleSelector
import matplotlib.figure as figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

import Code_FEM_v4 as fem

# instantiate matplotlib figure

# ------------------------------- This is to include a matplotlib figure in a Tkinter canvas
def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)

class Toolbar(NavigationToolbar2Tk):
     def __init__(self, *args, **kwargs):
         super(Toolbar, self).__init__(*args, **kwargs)


# ------------------------------- PySimpleGUI CODE

frame_node = [sg.Frame('Noeuds : ', [[sg.Text("X : "), sg.Input(s=10,default_text='0',enable_events=True, key="-X-")],
                       [sg.Text("Y : "), sg.Input(s=10,default_text='0',enable_events=True, key="-Y-")],
                       [sg.Text("Z : "), sg.Input(s=10,default_text='0',enable_events=True, key="-Z-")],
                            [sg.B('ajouter noeuds', key='add_node')]])]

frame_elem = [sg.Frame('elements : ', [[sg.Text("node 1 : "), sg.Input(s=10,default_text='1',enable_events=True, key="-n1-")],
                       [sg.Text("node 2 : "), sg.Input(s=10,default_text='2',enable_events=True, key="-n2-")],
                            [sg.B('ajouter elements', key='add_elem')]])]

frame_load = [sg.Frame('loads : ', [[sg.Text("node : "), sg.Input(s=10,default_text='1',enable_events=True, key="-n-")],
                       [sg.Text("Fx : "), sg.Input(s=10,default_text='2',enable_events=True, key="-Fx-")],
                       [sg.Text("Fy : "), sg.Input(s=10,default_text='0',enable_events=True, key="-Fy-")],
                       [sg.Text("Mz : "), sg.Input(s=10,default_text='0',enable_events=True, key="-Mz-")],
                            [sg.B('ajouter loads', key='add_load')]])]

layout_l = [
 [sg.B('start', key='plot')],
  frame_node ,
  frame_elem ,
  frame_load ,
]

layout_r = [ [sg.Canvas(key='controls_cv')],
            [sg.Canvas(key='fig_cv', size=(400 * 2, 200))],
    ]

layout = [[sg.MenubarCustom([['File', ['Exit']], ['Edit', ['Edit Me', ]]],  k='-CUST MENUBAR-',p=0)] ,
           [sg.T('Element finis 2D : ', font='_ 18', justification='c', expand_x=True)],
           [sg.Col(layout_l), sg.Col(layout_r)]]

window = sg.Window('Test', layout)
m = fem.Mesh(2,[[0,0], [1,0]],[[1,2]], debug = True)
f = fem.FEM_Model(m)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'add_node':
        X = float(values['-X-'])
        Y = float(values['-Y-'])
        Z = float(values['-Z-'])
        if [X,Y] not in m.node_list : 
            m.add_node([X,Y])
        else : 
            print('deja dans la liste des noeuds')
    elif event == 'add_elem' : 
        n1 = float(values['-n1-'])
        n2 = float(values['-n2-'])
        if [n1,n2] not in m.element_list : 
            m.add_element([n1,n2])
        else : 
            print('deja dans la liste des elements')
    elif event == 'add_load' : 
        n = float(values['-n-'])
        fx = float(values['-Fx-'])
        fy = float(values['-Fy-'])
        mz = float(values['-Mz-'])
        if [fx,fy,mz] not in f.load : 
            f.apply_load([fx,fy,mz],n)
        else :
            print('deja dans les charges')
    elif event == 'plot' :
        fig = m.geom()
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

    """
    x = np.linspace(0, 2 * np.pi,100)
    y = X*np.sin(x)
    line, = ax.plot(x, y)
    rs = RectangleSelector(ax, line_select_callback,
    drawtype='box', useblit=False, button=[1],
    minspanx=5, minspany=5, spancoords='pixels',
    interactive=True)
    draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)
    """

window.close()