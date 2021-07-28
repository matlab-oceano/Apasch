#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 12:07:42 2021

@author: spi-2017-12
"""

import os, glob, json
from datetime import date, timedelta, datetime
import pandas as pd
from netCDF4 import Dataset
import numpy as np
import configparser
import matplotlib.pyplot as plt
import matplotlib


class param_alk(object):
    def __init__(self,param1=[],calib=[],epsilon=[]):
        self.param1 = self.parametres()
        self.calib = self.calibration()
        self.epsilons=self.calcul_epsilons()
        self.param_optiques=self.calcul_param_optiques()

    def parametres (self) :
        vpompe=5.37e-5
        hfo_cwa=2.1805e-1
        indic_cwa=2e-4 
        dilu_color=0.0063/(vpompe*4)
        dilu_ech= 0.0063/(0.0063-(vpompe*4))
        
        parametres = pd.DataFrame({'Volume pompe' : '{:,.7f}'.format(vpompe) , 'Dilution colorant': dilu_color, 
                               'Dilution echantillon':dilu_ech,
                               'hfo(cwa)' : hfo_cwa,'hfo(cellule)': hfo_cwa/dilu_color,
                               'indicateur(cwa)' :indic_cwa, 'indicateur(cellule)' :'{:,.8f}'.format(indic_cwa/dilu_color)
                              },index=[0])
        return parametres


    def calibration(self):
        calibrer=pd.DataFrame({'A434': pd.Series([0.0851,0.1,0.0064,0.0823], index = ['Acide', 'Alc ON', 'NaOH','eau'])
                      , 'A591': pd.Series([0.0005,0.0479,0.3164,0.1001], index = ['Acide', 'Alc ON', 'NaOH','eau'])})
        fit=np.polyfit([0.1,0.0064,0.0823], [0.0479,0.3164,0.1001], 1, rcond=None, full=False, w=None, cov=False)
        pente=fit[0]
        oo= fit[1]
        return calibrer,pente,oo
        
            
    
    def calcul_epsilons(self):
        parametres=self.param1
        ae_591 = 0.000480708
        ae_434 = ( ae_591 - self.calib[2] )/self.calib[1]
        eps437j = ae_434/float(parametres['indicateur(cellule)'])
        eps437b = self.calib[0]['A434']['NaOH'] /float(parametres['indicateur(cellule)'])
        eps591j = ae_591/float(parametres['indicateur(cellule)'])
        eps591b = self.calib[0]['A591']['NaOH'] /float(parametres['indicateur(cellule)'])
        
        epsilon = pd.DataFrame({'eps(437,J)': eps437j, 
                                 'eps(437,B)': eps437b,
                                 'eps(591,J)': eps591j,
                                 'eps(591,B)': eps591b,             
                              },index=[0])
        return epsilon
    
    def calcul_param_optiques (self) : 
        e1 = self.epsilons['eps(591,J)']/ self.epsilons['eps(437,J)']
        e2 = self.epsilons['eps(591,B)']/ self.epsilons['eps(437,J)']
        e3 = self.epsilons['eps(437,B)']/ self.epsilons['eps(437,J)']
        e4 = e3/e2
        s=self.calib[1]
        e2_sb = -s/(1-s*e4)
        B591 = self.calib[0]['A591']['NaOH'] 
        param_optiques = pd.DataFrame({'e1': e1, 
                                 'e2': e2,
                                 'e3': e3,
                                 'e4': e4,  
                                 's': s,  
                                 'e2 (Sb)': e2_sb,  
                                 'B591' : B591
                              },index=[0])
        return param_optiques
    
    
    
    def calcul_moyenne(self,un_cycle=[]):
        
        df=un_cycle
        # calcul des moyennes 
        CYCLE=int(df['COUNT'].mean())
        TEMP=df['T_cel'].mean()/100
        NH=df.iloc[:,6].mean()
        NL=df.iloc[:,7].mean()
        NTH=df.iloc[:,8].mean()
        RTH=df.iloc[:,9].mean()
        T810_blanc=df[df.iloc[:,2]=='Blanc_Alc'].mean().iloc[1]
        T810_mesure=df[df.iloc[:,2]=='Mesure_Alc'].mean().iloc[1]
        T434_blanc=df[df.iloc[:,2]=='Blanc_Alc'].mean().iloc[3]
        T434_mesure=df[df.iloc[:,2]=='Mesure_Alc'].mean().iloc[3]
        T591_blanc=df[df.iloc[:,2]=='Blanc_Alc'].mean().iloc[2]
        T591_mesure=df[df.iloc[:,2]=='Mesure_Alc'].mean().iloc[2] 
        # calcul des deux coeff avec log
        A591=( np.log10(T591_blanc/T591_mesure) - np.log10( T810_blanc/T810_mesure) ) /2.2
        A437=( np.log10( T434_blanc/T434_mesure)-np.log10( T810_blanc/T810_mesure) ) /2.2
        R_prime=A437/A591
        
        # time= pd.to_datetime(df['DATE']+' '+df['TIME'], format='%d/%m/%Y %H:%M:%S')
        time= pd.to_datetime(df['DATETIME'], format='%Y/%m/%d %H:%M:%S')
        TIME=time.mean().strftime('%Y-%m-%d %H:%M:%S.%f')[0:23]
        TIME= pd.to_datetime(TIME, format='%Y-%m-%d %H:%M:%S.%f')
        
        moy = pd.DataFrame({'CYCLE' : CYCLE ,'DATE+HEURE' : TIME,
                                       'TEMP' : TEMP ,'A591' : A591,'A437':A437,"R'":R_prime,
                                       'BLANC T591':T591_blanc,'BLANC T434':T434_blanc,'BLANC T810' : T810_blanc,
                                       'MESURE T591' : T591_mesure,'MESURE T434':T434_mesure,'MESURE T810':T810_mesure,
                                       'NH':NH,'NL':NL,'NTH(ALC)':NTH,'RTH(ALC)':RTH },index=[0])

        return moy 
      
    
    def caclul_alcalinites (self,un_cycle,pka_ind=3.89):
        param_optique=self.param_optiques
        calib=self.calib[0]
        parametres=self.param1
        moy=self.calcul_moyenne(un_cycle)
        B591=moy['A591']-(param_optique['s']*moy['A437'])/(1-param_optique['e3'])
        Dr1=((1/moy["R'"])-param_optique['e1'])/(param_optique['e2']-(1/moy["R'"])*(param_optique['e3']))
        Dr2=moy["R'"]*param_optique['e2']-param_optique['e3']
        Dr3a=Dr1
        Dr3b=Dr2
        Drsb=param_optique['e2 (Sb)']*(moy["R'"]-param_optique['e4'])
        # Calcul des pH
        pH1= pka_ind-np.log(Dr1)
        pH2=pka_ind-np.log(Dr2)
        pH3a = pka_ind-np.log(Dr3a)
        pH3b = pka_ind-np.log(Dr3b)
        pHsb = pka_ind-np.log(Drsb)
        # calcul du pKA
        pka_hfo=0.014*(moy["TEMP"]+273.15)+(1278.3/(moy["TEMP"]+273.15)-4.9285+0.08)
        #calcul de K
        k_ind=10**(-pka_ind)/10**(-pka_hfo)
        
        # calcul de l'alcalinité
        
        alc1=(((parametres["hfo(cellule)"]*((moy['A591']-param_optique['e1']*moy['A437'])/
             (param_optique['B591']-calib['A434']['NaOH']*param_optique['e1']))*
             ((1+(1/Dr1))/(1+(k_ind*(1/Dr1)))))-(10**(-pka_ind)*(1/Dr1)))*parametres['Dilution echantillon'])/(1-
                                                                             (0.0000003/(10**-pka_ind*(1/Dr1))))
        alc2 =(((parametres["hfo(cellule)"]*(moy['A591']/param_optique['B591'])*
              ((1+Dr2)/(1+(k_ind*Dr2))))-(10**(-pka_ind)*Dr2))
              *parametres['Dilution echantillon'])/(1-(0.0000003/(10**(-pka_ind)*Dr2)))
        
        alc3=1000000*(((parametres["hfo(cellule)"]*(moy['A591']/param_optique['B591'])
                    *((1+Dr3b)/(1+(k_ind*Dr3b))))-(10**-pka_ind*Dr3b))
                    *parametres['Dilution echantillon'])/(1-(0.0000003/(10**-pka_ind*Dr3b)))
        
        alcsb=(((parametres["hfo(cellule)"]*((1-param_optique['s']*param_optique['e4'])/(1-param_optique['s']*moy["R'"]))
               *((1+Drsb)/(1+(k_ind*Drsb))))-(10**-pka_ind*Drsb))
               *parametres['Dilution echantillon'])/(1-(0.0000003/(10**-pka_ind*Drsb)))
    
        alcalinites = pd.DataFrame({'Alc 1' : alc1 ,'Alc 2' : alc2,'Alc 3' : alc3,'Alc Sb' : alcsb},index=[0])
    
        return alcalinites
     
        

   
        
if __name__=="__main__":
    
    
    print('classe alcalinité eaux douces')