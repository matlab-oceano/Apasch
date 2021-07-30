
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import glob


class plot_ph() :
    def __init__(self,file = ['data.txt']):
        self.file = file
        self.x_vals = []
        self.y_vals = []

    def graphe(self) :
        plt.style.use('fivethirtyeight')
        index = count()

    def animate(self,i):

        print(self.file[-1])
        data = pd.read_csv(self.file[-1])
        x = data['Datetime']
        y1 = data['Temp']
        y2 = data['pH']
        plt.cla()
        plt.plot(x, y1, label='Temp')
        plt.plot(x, y2, label='pH')
        plt.legend(loc='upper left')
        plt.tight_layout()
        #plt.xticks(rotation=30)
    def lancer_plot(self):
        ani = FuncAnimation(plt.gcf(), self.animate, interval=1000)
        plt.tight_layout()
        plt.show()




if __name__ == '__main__':
    k=plot_ph()
    k.lancer_plot()
