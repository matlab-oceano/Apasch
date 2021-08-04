#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 22:26:56 2021

@author: spi-2017-12
"""

from tkinter import * 
from random import randint 
import pandas as pd
# these two imports are important
from matplotlib import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.figure import Figure 
import time
import matplotlib.pyplot as plt
import threading

continuePlotting = False 
 
def change_state(): 
    global continuePlotting 
    if continuePlotting == True: 
        continuePlotting = False 
    else: 
        continuePlotting = True 
     
 
def data_points():
    data = pd.read_csv('data.txt').tail(50)
<<<<<<< HEAD

    print(data)
    return data

def app():
    # initialise a window.
  #  time.sleep(5)
    root = Tk() 
    root.config(background='white') 
    root.geometry("1000x700")
    lab = Label(root, text="Temperature as function of time",font=('Helvetica',20), bg = 'white').pack()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel("Time")
    ax.set_ylabel("Temp")
    ax.set_title('Temperature as function of time')
=======
    print(data)
    return data['Datetime'],data['Temp']

def app(): 
    # initialise a window. 
    root = Tk() 
    root.config(background='white') 
    root.geometry("1000x700") 
     
    lab = Label(root, text="pH as function of time", bg = 'white').pack()

    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.set_xlabel("Time")
    ax.set_ylabel("pH")
    ax.set_title('pH as function of time')
>>>>>>> 4df6cf04824cd63f1653c951c476d78d8e810ebc
    ax.grid()

    for label in ax.get_xticklabels():
        label.set_ha("right")
        label.set_rotation(45)
    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().pack(side="top",fill='both',expand=True) 
 
<<<<<<< HEAD
    def plotter():
        while continuePlotting: 
            ax.cla()
            ax.grid()
            x = data_points()['Datetime'].tail(20)
            y = data_points()['Temp'].tail(20)
            ax.plot( x,y, marker='o', color='orange')
            ax.set_xlabel("Time")
            ax.set_ylabel("Temperature")
=======
    def plotter(): 
        while continuePlotting: 
            ax.cla()
            ax.grid()
            x = data_points()[0]
            y = data_points()[1]
            ax.plot( x,y, marker='o', color='orange')
            ax.set_xlabel("Time")
            ax.set_ylabel("pH")
>>>>>>> 4df6cf04824cd63f1653c951c476d78d8e810ebc
            plt.tight_layout()
            for label in ax.get_xticklabels():
                label.set_ha("right")
                label.set_rotation(45)
            graph.draw()
<<<<<<< HEAD
            time.sleep(5)
            lab = Label(root, text=data_points().tail(1),font=('Helvetica',20), bg = 'white').place(relx = 0.5,rely = 0.9,anchor = 'n')
 
    def gui_handler():
        change_state() 
        threading.Thread(target=plotter).start()
 
    b = Button(root, text="Start/Stop", command=gui_handler, bg="red", fg="white")
    b.pack()

    root.mainloop() 
 
if __name__ == '__main__':
    app()
=======
            time.sleep(1)
 
    def gui_handler(): 
        change_state() 
        threading.Thread(target=plotter).start() 
 
    b = Button(root, text="Start/Stop", command=gui_handler, bg="red", fg="white") 
    b.pack() 
     
    root.mainloop() 
 
if __name__ == '__main__': 
    app() 
>>>>>>> 4df6cf04824cd63f1653c951c476d78d8e810ebc
