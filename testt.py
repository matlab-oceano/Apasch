#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 22:26:56 2021
@author: spi-2017-12
"""
import matplotlib.dates as mdates
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
color_blue = '#4065A4'

def change_state():
    global continuePlotting
    if continuePlotting == True:
        continuePlotting = False
    else:
        continuePlotting = True


def data_points():
    data = pd.read_csv('data.txt').tail(50)
    print(data)
    return data

def app():
    # initialise a window.
  #  time.sleep(5)
    root2 = Tk()
    root2.config(background='white')
    root2.geometry("1000x700")
    mainframe=LabelFrame(root2,text='PLOT',fg='white',font=('Helvetica',20),
                         height = 720,width=1080,
                         borderwidth=1,bg=color_blue)
    frame_text =LabelFrame(root2,text='Values',fg='white',font=('Helvetica',20),
                           width = 300 ,height = 720,
                           borderwidth=1,bg=color_blue)

    frame_text.grid(row=1,column=1)
    mainframe.grid(row=1,column=2)

 #   lab = Label(root, text="Temperature as function of time",font=('Helvetica',20), bg = 'white').pack()
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(211)
  #  ax.set_xlabel("Time")
  #  ax.set_ylabel("Temp")
    ax.set_title('pH as function of time')
    ax.grid()

    ax2 = fig.add_subplot(212)
    ax2.set_xlabel("Time")
    ax2.set_ylabel("pH")
    ax2.set_title('Temperature as function of time')
    ax2.grid()


    for label in ax.get_xticklabels():
        label.set_ha("right")
        label.set_rotation(45)
    graph = FigureCanvasTkAgg(fig, master=mainframe)
    graph.get_tk_widget().grid()

    def plotter():
        while continuePlotting:
            ax.cla()
            ax.grid()
            x = data_points()['Datetime'].tail(20)
            x=pd.to_datetime(x)
            y = data_points()['pH'].tail(20)
            print( ' ------------------- ')
            print(x)
            print(y)
            print(' ------------------------ ')
            ax.scatter( x,y, marker='o', color='red')
            ax.set_ylabel("pH")
            plt.tight_layout()
            ax.axes.get_xaxis().set_ticks([])
         #   graph.draw()
            ax2.cla()
            ax2.grid()
            x = data_points()['Datetime'].tail(20)
            x=pd.to_datetime(x)
            y = data_points()['Temp'].tail(20)
            ax2.set_xlabel("Time")
            ax2.set_ylabel("Temperature")
            plt.tight_layout()
            myFmt = mdates.DateFormatter('%X')
            ax2.scatter( x,y, marker='o', color='red')
            ax2.xaxis.set_major_formatter(myFmt)

            for label in ax2.get_xticklabels():
                label.set_ha("right")
                label.set_rotation(45)
            ax.set_title('pH as function of time')
            ax2.set_title('Temperature as function of time')


            graph.draw()
       #     time.sleep(5)
            x = data_points().tail(1)

            lab = Label(frame_text, text=x,
                        font=('Helvetica',12),
                        bg = 'white').place(relx = 0.5,rely = 0.2,anchor = 'n')

    def gui_handler():
        change_state()
        threading.Thread(target=plotter).start()

   # b = Button(mainframe, text="Start/Stop", command=gui_handler(), bg="red", fg="white")
   # b.grid()
    gui_handler()
    root2.mainloop()


if __name__ == '__main__':
    k=threading.Thread(target=app)
    k.start()

