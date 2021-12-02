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
from testt import *

continuePlotting = False
color_blue = '#4065A4'

def change_state():
    global continuePlotting
    if continuePlotting == True:
        continuePlotting = False
    else:
        continuePlotting = True


def data_points2(file1):
    data = pd.read_csv(file1).tail(10)
    print(data)
    return data


def app2(file1='data.txt'):
    # initialise a window.
  #  time.sleep(5)
    root = Tk()
    root.config(background='white')
    root.geometry("1080x700")
    mainframe=LabelFrame(root,text='Intermediate Values',fg='white',font=('Helvetica',20),
                         borderwidth=1,bg=color_blue)
    data_points2(file1)

    fig = plt.figure(figsize=(12,5))
    ax = fig.add_subplot(231)
    ax.set_title('Lambda 1 as function of time')
    ax.grid()

    ax2 = fig.add_subplot(232)
    ax2.set_title('Lambda 2 as function of time')
    ax2.grid()

    ax3 = fig.add_subplot(233)
    ax3.set_title('Lambda 3 as function of time')
    ax3.grid()

    ax4 = fig.add_subplot(234)
    ax4.set_title('Lambda 1 as function of time')
    ax4.grid()

    ax5 = fig.add_subplot(235)
    ax5.set_title('Lambda 2 as function of time')
    ax5.grid()

    ax6 = fig.add_subplot(236)
    ax6.set_title('Lambda 3 as function of time')
    ax6.grid()



    graph = FigureCanvasTkAgg(fig, master=mainframe)
    graph.get_tk_widget().grid(row=1,column = 1)

    def plotter():
        while continuePlotting:
            ax.cla()
            ax.grid()
            x = data_points2(file1)['DATETIME'].tail(10)
            y = data_points2(file1)['LAMBDA_1'].tail(10)
            ax.scatter( x,y, marker='o', color='red')
            ax.set_ylabel("Lambda 1")
            plt.tight_layout()
            ax.axes.get_xaxis().set_ticks([])
            ax.set_title('Lambda 1 as function of time')

         #  figure 2

            ax2.cla()
            ax2.grid()
            x = data_points2(file1)['DATETIME'].tail(10)
            y = data_points2(file1)['LAMBDA_2'].tail(10)
            ax2.set_ylabel("Lambda 2")
            plt.tight_layout()
            ax2.scatter( x,y, marker='o', color='red')
            ax2.set_title('Lambda 2 as function of time')
            ax2.axes.get_xaxis().set_ticks([])

         #  figure 2

            ax3.cla()
            ax3.grid()
            x = data_points2(file1)['DATETIME'].tail(10)
            y = data_points2(file1)['LAMBDA_3'].tail(10)
            ax3.set_ylabel("Lambda 3")
            plt.tight_layout()
            ax3.scatter( x,y, marker='o', color='red')
            ax3.set_title('Lambda 3 as function of time')
            ax3.axes.get_xaxis().set_ticks([])



            ax4.cla()
            ax4.grid()
            x = data_points2(file1)['DATETIME'].tail(10)
            y = data_points2(file1)['LAMBDA_3'].tail(10)
            ax4.set_xlabel("Time")
            ax4.set_ylabel("NH")
            plt.tight_layout()
            ax4.scatter( x,y, marker='o', color='red')
            ax4.set_title('NH as function of time')


            ax5.cla()
            ax5.grid()
            x = data_points2(file1)['DATETIME'].tail(10)
            y = data_points2(file1)['NL'].tail(10)
            ax5.set_xlabel("Time")
            ax5.set_ylabel("NL")
            plt.tight_layout()
            ax5.scatter( x,y, marker='o', color='red')
            ax5.set_title('NL as function of time')

            ax6.cla()
            ax6.grid()
            x = data_points2(file1)['DATETIME'].tail(10)
            y = data_points2(file1)['Nth'].tail(10)
            ax6.set_xlabel("Time")
            ax6.set_ylabel("Nth")
            plt.tight_layout()
            ax6.scatter( x,y, marker='o', color='red')
            ax6.set_title('Nth as function of time')

            for label in ax6.get_xticklabels():
                label.set_ha("right")
                label.set_rotation(35)

            for label in ax5.get_xticklabels():
                label.set_ha("right")
                label.set_rotation(35)

            for label in ax4.get_xticklabels():
                label.set_ha("right")
                label.set_rotation(35)


            graph.draw()
       #     time.sleep(5)



            x = data_points2(file1).tail(1)
            lab = Label(root, text=x,fg='white',
                        font=('Helvetica',11),
                        bg = color_blue ).place(relx = 0.5,rely = 0.1,anchor = 'n')


    def gui_handler():
        change_state()
        threading.Thread(target=plotter).start()

   # b = Button(mainframe, text="Start/Stop", command=gui_handler(), bg="red", fg="white")
   # b.grid()
    gui_handler()
    mainframe.pack(side='bottom',fill=BOTH)

    root.mainloop()

if __name__ == '__main__':
    import glob
    import os
    cwd = os.getcwd()
    list_of_files = glob.glob(cwd+'/RAW*.txt') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
    app2(latest_file)

