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
    data = pd.read_csv('data.txt').tail(25)
    print(data)
    return data['Datetime'], data['Temp']


def app():
    # initialise a window.
    root = Tk()
    root.config(background='white')
    root.geometry("1000x700")

    lab = Label(root, text="Figure 1", bg='white').pack()
    fig = plt.figure()
    ax = plt.gca()
    plt.xticks(rotation=30)
    plt.ylabel('Temperature (°c)')
    plt.xlabel('Time')
    plt.grid()
    plt.tight_layout()
    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().pack(side="top", fill='both', expand=True)

    def plotter():
        while continuePlotting:
            plt.cla()
            plt.grid()
            x = data_points()[0]
            y = data_points()[1]
            plt.scatter(x, y, label='Temp')
            plt.title('Temperature as function of time')
            plt.xticks(rotation=30)
            plt.ylabel('Temperature (°c)')
            plt.xlabel('Time')
            plt.grid()
            graph.draw()
            time.sleep(1)
            plt.tight_layout()

    def gui_handler():
        change_state()
        threading.Thread(target=plotter).start()

    b = Button(root, text="Start/Stop", command=gui_handler, bg="red", fg="white")
    b.pack()

    root.mainloop()


if __name__ == '__main__':
    app()