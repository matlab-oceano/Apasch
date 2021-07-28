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
from alk import *


class Apasch(object):
    
    def __init__(self,data=[],salinity=38,DATA_DIR='',apasch_files=[''],campagne='campagne',CTE_APASCH={},head=['']):
        self.head=head
        self.data=data
        self.salinity=salinity
        self.apasc_file=apasch_files
        cwd = os.getcwd()
        DATA_DIR = os.path.join(cwd)
        self.DATA_DIR=DATA_DIR
        colonnes_alc=['CYCLE','DATE+HEURE','TEMP','A591','A437',"R'",
                                       'BLANC T591','BLANC T434','BLANC T810',
                                       'MESURE T591','MESURE T434','MESURE T810',
                                       'NH','NL','NTH(ALC)','RTH(ALC)','Alc 1',
                                       'Alc 2','Alc 3','Alc Sb']
        colonnes_pH=['Date','Temp','pH','Abs_LED3','Abs_LED2','Abs_LED1','R_indic']
        
        self.data_calcule=pd.DataFrame(columns=colonnes_pH)
        self.data_alk_calcule=pd.DataFrame(columns=colonnes_alc)
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
                


    
    def triplicate (self, data_pd) :
            for i in range(z,z+14,3) :#average the triplicate data:
                il=il+1;
                Ti.append(data_pd.iloc[i][10]);
                Avg_LED1.append((data_pd['LAMBDA_1'][i:i+3].mean()));
                Avg_LED2.append((data_pd['LAMBDA_2'][i:i+3].mean()));
                Avg_LED3.append((data_pd['LAMBDA_3'][i:i+3].mean()));
                Avg_Ref_LED1.append((data_pd['NL'][i:i+3].mean()));
                Avg_Ref_LED2.append((data_pd['Nthph'][i:i+3].mean()));
                Avg_Ref_LED3.append((data_pd['100_T_cel'][i:i+3].mean()));
        
        

    def calcul_pH(self,data_pd) :
        
        # Initialisation 
        # Salinité
        S=self.salinity;
        size_data=15
        Abs_LED1 = np.zeros((size_data//15,4))
        Abs_LED2 = np.zeros((size_data//15,4))
        Abs_LED3 = np.zeros((size_data//15,4))
        R_indic  = np.zeros((size_data//15,4))
        pHj  = []
        temp=[]
        datef=[]
        
        zl=0
        for z in range (0,15,15) : #1 measurement=15 lines
            zl+=1;
        # date of the sample
            #date_sample=data_pd.iloc[z][0]+' '+data_pd.iloc[z][1];
            date_sample=data_pd.iloc[z][0]
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
                Ti.append(data_pd.iloc[i][9]/100);
                Avg_LED1.append(data_pd.iloc[i:i+3,3].mean());
                Avg_LED2.append(data_pd.iloc[i:i+3,4].mean());
                Avg_LED3.append(data_pd.iloc[i:i+3,5].mean());
                Avg_Ref_LED1.append((data_pd.iloc[i:i+3,7].mean()));
                Avg_Ref_LED2.append((data_pd.iloc[i:i+3,8].mean()));
                Avg_Ref_LED3.append((data_pd.iloc[i:i+3,9].mean()));
        
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
  #      self.data_calcule = df.round(4)
        self.data_calcule = pd.concat([self.data_calcule,df.round(4)]
            , axis=0, join="inner",ignore_index=True)
        return True
    
    def calcul_alk_ed_cycle(self,un_cycle): 
        # moyennes du cycle
        moyennes=param_alk().calcul_moyenne (un_cycle)
        # calcul des differentes alcalinites
        alk=param_alk().caclul_alcalinites (un_cycle)
        # concatenation
        alc=pd.concat([moyennes, alk], axis=1, join="inner")
        self.data_alk_calcule=pd.concat([self.data_alk_calcule,alc]
            , axis=0, join="inner",ignore_index=True)
      
     
        
if __name__=="__main__":
    print('classe apasch  ok')
    # apa=Apasch()
    # apa.campagne='Moose 2019'
    # apa.list_apasch_files('TXT','apasch_files')
    # apa.head=['DATE','TIME','COUNT','TYPE','LED1','LED2','LED3','NH','Ref_LED1','Ref_LED2','Ref_LED3','T_cel']
    # apa.CTE_APASCH = {"header": None,
    #               "sep": '\s+',
    #               "ext": 'txt',
    #               "col": [],
    #               "t_format": '%Y/%m/%d %H:%M:%S',
    #               "t_name": 'DATE_TIME',
    #               "path": apa.DATA_DIR,
    #               }
    # # On transforme le premier fichier de donnees (indice 0 ) en dataframe  
    # apa.file2dataframe(0)
    # # On fait le calcul pour chaque cycle du fichier 
    # print("Caclul de l'alcalinité en eaux douces : ")
    # # un cycle tient sur 6 lignes
    # for j in range(0,len(apa.data)//6)  :
    #     un_cycle=apa.data[apa.data['COUNT']==j+1]
    #     apa.calcul_alk_ed_cycle(un_cycle)
    # # Ecriture sur un fichier txt des resultats
            
    # filename='catenoy_alk.txt'
    # sep='\t'
    # apa.data_alk_calcule.to_csv(filename,columns=['CYCLE','DATE+HEURE','TEMP','Alc 1','Alc 2','Alc 3','Alc Sb'],float_format='%.6f'
    #            ,sep = sep,index=None)  