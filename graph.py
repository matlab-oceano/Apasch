
import time
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

    def animate(self,i):
        print('Lecture du fichier : ' , self.file[-1])
        data = pd.read_csv(self.file[-1])
        if len(data)>0 :
            x = data['Datetime'].tail(100)
            y1 = data['Temp'].tail(100)
            y2 = data['pH'].tail(100)
            plt.subplot(2, 1, 1)
            plt.cla()
           # plt.tight_layout()
            plt.title('pH as function of time')
            plt.scatter(x, y2, label='pH')
            plt.ylabel('pH')
            plt.legend(loc='upper right')
            plt.grid()
            ax = plt.gca()
            ax.axes.xaxis.set_visible(False)
            plt.subplot(2,1,2)
            plt.cla()
            plt.title('Temperature as function of time')
            plt.scatter(x, y1, label='Temp')
            plt.legend(loc='upper right')
            plt.xticks(rotation=30)
            plt.ylabel('Temperature (°c)')
            plt.xlabel('Time')
            plt.grid()
            plt.tight_layout()



    def lancer_plot(self):
        ani = FuncAnimation(plt.gcf(), self.animate, interval=1000)
        plt.tight_layout()
        plt.show()




if __name__ == '__main__':
    k=plot_ph()
    k.lancer_plot()
