#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 13:54:51 2021

@author: spi-2017-12
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 00:55:54 2021

@author: spi-2017-12
"""
import matplotlib.pyplot as plt
import matplotlib
from read_file import *

class Apasch(object):
    def __init__(self,data=[],salinity=38,DATA_DIR='',apasch_files=[''],campagne='campagne',CTE_APASCH={},head=['']):
        self.head=head
        self.data=data
        self.salinity=salinity
        self.apasc_file=apasch_files
        cwd = os.getcwd()
        DATA_DIR = os.path.join(cwd)
        self.DATA_DIR=DATA_DIR
        self.data_calule=[]
        self.campagne=campagne
        self.CTE_APASCH = CTE_APASCH
    def __str__(self):
        msg = 'Class APASCH, Data_Dir : ' + self.DATA_DIR
        return msg
    def __repr__(self):
        return self.__str__()
    
    def list_apasch_files(self,extension='TXT',dossier_apasch=''):
        FID = ReadFile()
        cwd = os.getcwd()
        CACHE_DIR = os.path.join(cwd,'cache')
        os.makedirs(CACHE_DIR, exist_ok=True)
        apasch_files = [x for x in os.listdir(self.DATA_DIR+'/'+dossier_apasch) if x.endswith('.'+extension)]
        print('Fichiers Apasch :' , apasch_files)
        self.apasch_files=apasch_files

    def file2dataframe(self,index=0):
        FID = ReadFile()
        data_pd = FID.readFid(['apasch_files/'+self.apasch_files[index]], self.CTE_APASCH)
        if self.CTE_APASCH["header"]==None :
            data_pd.columns = self.head
        self.data=data_pd
        data_pd
                


    def calcul_pH(self,index=0) :
        
        # Initialisation 
        # Salinité
        print('Traitement du fichier : ', self.apasch_files[index])
        self.file2dataframe(index)       
        S=self.salinity;
        data_pd=self.data ; 
        size_data=(len(data_pd))-len(data_pd)%15
        print(size_data)
        if(len(data_pd))%15 != 0 :
            print("le nombre de lignes de :",self.apasch_files[index],"n'est pas un multiple de 15" )
        Abs_LED1 = np.zeros((size_data//15,4))
        Abs_LED2 = np.zeros((size_data//15,4))
        Abs_LED3 = np.zeros((size_data//15,4))
        R_indic  = np.zeros((size_data//15,4))
        pHj  = []
        temp=[]
        datef=[]
        
        zl=0
        for z in range (0,(size_data),15) : #1 measurement=15 lines
            zl+=1;
        # date of the sample
            date_sample=data_pd['DATE'][z]+' '+data_pd['TIME'][z];
        # sample temperature= average of temperature during all the measurements of the sample    
            T=np.mean(data_pd['T_cel'][z:z+14])
            il=0 
            Ti=[]
            Avg_LED1=[]    
            Avg_LED2=[]
            Avg_LED3=[]
            Avg_Ref_LED1=[]    
            Avg_Ref_LED2=[]
            Avg_Ref_LED3=[]
            
            for i in range(z,z+14,3) :#average the triplicate data:
                il=il+1;
                Ti.append(data_pd['T_cel'][i]/100);
                Avg_LED1.append(np.nanmean(data_pd['LAMBDA_1'][i:i+3]));
                Avg_LED2.append(np.nanmean(data_pd['LAMBDA_2'][i:i+3]));
                Avg_LED3.append(np.nanmean(data_pd['LAMBDA_3'][i:i+3]));
                Avg_Ref_LED1.append(np.nanmean(data_pd['NL'][i:i+3]));
                Avg_Ref_LED2.append(np.nanmean(data_pd['Nthph'][i:i+3]));
                Avg_Ref_LED3.append(np.nanmean(data_pd['100_T_cel'][i:i+3]));
                
        
           #calcul des absorbances pour chaque addition de colorant :
            for j in range (0,4) : 
              #  print(zl)
                Abs_LED1[zl-1][j]=np.log10(Avg_LED1[0]/Avg_LED1[j+1]);
                Abs_LED2[zl-1][j]=np.log10(Avg_LED2[0]/Avg_LED2[j+1])-Abs_LED1[zl-1][j];
                Abs_LED3[zl-1][j]=np.log10(Avg_LED3[0]/Avg_LED3[j+1])-Abs_LED1[zl-1][j];
                R_indic[zl-1][j]=Abs_LED2[zl-1][j]/Abs_LED3[zl-1][j]                     #rapport des absorbances
            #Calibration d'Apasch pour 4°C<T<31°C et 20<S<40
                Tki=273.15+Ti[4]; 
                e1=0.0170595;
                e4=1.560023*10**3+4.811158*10**(-1)*Tki+1.146155*10**(-1)*S-1.933045*10**(-3)*S*S-3.958658*10**4/Tki-2.75658*10**2*np.log(Tki)-2.026206*10**(-2)*np.log(Tki)*S+3.418927*10**(-4)*np.log(Tki)*S*S;       
            #Equation en utilisant la relation de Dickson pour le tris:
               # pK2e2=1.262784*10**2-4.640924*S+3.34405*10**(-3)*S*S-(4.154957*10**3)/Tki-(1.834135*10**1)*np.log(Tki)+(1.947547*10**2*S)/Tki+6.987689*10**(-1)*S*np.log(Tki)-5.741784*10**(-4)*S*S*np.log(Tki);
                pK2e2=1.17901*10**2-4.358595*S+4.262097*10**(-3)*S*S-(3.755133*10**3)/Tki-(1.71209*10**1)*np.log(Tki)+(1.800733*10**2*S)/Tki+6.585909*10**(-1)*S*np.log(Tki)-7.443867*10**(-4)*S*S*np.log(Tki)
            #Equation en utilisant la deuxième relation pour le tris:
            pHj.append(pK2e2+np.log10((R_indic[zl-1][0]-e1)/(1-R_indic[zl-1][0]*e4)));
            temp.append(Ti[4])
            datef.append(date_sample)
        # On arrange dans un dataframe
        temp=np.array(temp)
        temp.reshape(-1,1)
        df = pd.DataFrame({'Date': datef,'Temp':temp,'pH':pHj,'Abs_LED3':Abs_LED3[:,-1],'Abs_LED2':Abs_LED2[:,-1],'Abs_LED1':Abs_LED1[:,-1],'R_indic' :R_indic[:,-1]} )
        self.data_calcule = df.round(4)
        self.export_pH(index=index)
        return True
  
    def export_pH(self,filename='',sep='\t',index=0):
        data_file=self.apasch_files[index]
        filename='ph_calcule/'+data_file[0:len(data_file)-4]+'_calcule.txt'
        self.data_calcule.to_csv(filename, sep = sep)         
    
    def plot_data(self,xdata='Temp',ydata='pH',index=0):
        SMALL_SIZE = 20
        MEDIUM_SIZE = 22
        BIGGER_SIZE=23
        plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
        plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
        plt.figure(figsize=(12,8))
        plt.scatter(self.data_calcule[xdata],self.data_calcule[ydata],label='pH_Apasch')
        plt.legend()
        plt.ylabel(ydata)
        plt.xlabel(xdata)
        name=self.campagne+': '+ydata+' fct de '+xdata+self.data_calcule['Date'][0][0:10]
        namefig=self.campagne+'_'+ydata+'_fct_de_'+xdata+self.data_calcule['Date'][0].split('/')[1]+self.data_calcule['Date'][0].split('/')[2][0:2]
        plt.savefig(namefig+'.png',bbox_inches='tight')
        plt.title(name)
        plt.grid()
        plt.savefig(namefig+'.png')

    def plot_data_time(self,ydata='pH',index=0):
        SMALL_SIZE = 20
        MEDIUM_SIZE = 22
        BIGGER_SIZE=23
        plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
        plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
        
        xv = [datetime.strptime(d,"%Y/%m/%d %H:%M:%S") for d in self.data_calcule['Date']]
        dates = matplotlib.dates.date2num(xv)
        
        fig=plt.figure(figsize=(10,5))
        plt.plot_date(dates, self.data_calcule[ydata],label=ydata)
        plt.tight_layout()
        fig.autofmt_xdate()
        plt.legend()
        plt.ylabel(ydata)
        plt.xlabel('Time')
        
        name=self.campagne+', '+ydata+' en fct du temps :'+self.data_calcule['Date'][0][0:10]
        namefig=self.campagne+'_'+ydata+'_fct_du_temps'+self.data_calcule['Date'][0].split('/')[1]+self.data_calcule['Date'][0].split('/')[2][0:2]
        plt.savefig(namefig+'.png',bbox_inches='tight')
        plt.title(name)
        plt.grid()
        plt.savefig(ydata+' en fonction du temps , '+self.apasch_files[index][1:8]+'.png')

    def plot_data_time2(self,ydata='pH',ydata2='Temp',index=0,dossier=''):
        if dossier != '' : dossier+='/'
        SMALL_SIZE = 18
        MEDIUM_SIZE = 20
        BIGGER_SIZE=22
        plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
        plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
        
        xv = [datetime.strptime(d,"%Y/%m/%d %H:%M:%S") for d in self.data_calcule['Date']]
        dates = matplotlib.dates.date2num(xv)
        fig,ax = plt.subplots(figsize=(12,6))
        lns1=ax.plot_date(dates, self.data_calcule[ydata],label=ydata,color='red')
        plt.tight_layout()
        fig.autofmt_xdate()
        ax.set_ylabel(ydata,fontsize=MEDIUM_SIZE,color='red')
        ax2=ax.twinx()
        lns2=ax2.plot_date(dates, self.data_calcule[ydata2],label=ydata2)
        fig.autofmt_xdate()
        ax2.set_ylabel(ydata2,fontsize=MEDIUM_SIZE,color='blue')
        ax2.set_xlabel("Time",fontsize=MEDIUM_SIZE)
        plt.grid()
        # added these three lines
        lns = lns1+lns2
        labs = [l.get_label() for l in lns]
        ax.legend(lns, labs, loc=2,edgecolor="inherit",framealpha=0.95,facecolor='inherit' )
        name=self.campagne+': '+ydata+' et '+ydata2+' en fonction du temps , '+self.data_calcule['Date'][0][0:10]
        ax.set_title(name)
        namefig=self.campagne+'_'+ydata+'_'+ydata2+self.data_calcule['Date'][(len(dates))//2].split('/')[1]+self.data_calcule['Date'][(len(dates))//2].split('/')[2][0:2]
        plt.grid()
        plt.savefig(self.DATA_DIR+'/'+dossier+namefig+'.png',bbox_inches='tight')
        
                
        
      
     


        
if __name__=="__main__":
    print('classe apasch  ok')