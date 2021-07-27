import os, glob, json
from datetime import date, timedelta, datetime
import pandas as pd
from netCDF4 import Dataset
import numpy as np
import configparser


class ReadFile:

    def makeList(self, context):
        return glob.glob(context['path']+context['ext'])

    def readFid (self,fid,context):
        """

        :param fid:
        :param context:
        :return:
        """
        df = []
        print("lecture de {} fichier  {}".format(len(fid) , context['ext']))
        if context['ext'] in ['csv', 'txt']:
            for f in fid:
                data = pd.read_table(
                                      context['path']+"/"+f,
                                      header=context['header'],
                                      sep=context['sep'],
                                                     )
                df.append(pd.DataFrame(data))
        elif context['ext'] in  ['ths','gps', 'netcdf','nvi' ]:
            df2=[]
            for f in fid:
                file = context['path']+"/"+f
                nc = Dataset(file,'r')
                index = list(nc.variables)
                data = dict((v, nc.variables[v][:]) for v in context['col'])
                df.append(pd.DataFrame(data))
        return   pd.concat(df, axis=0, ignore_index=False)

    def concat_DT(self, df):
        """
        Concatenate Date time in the array
        :param df:
        :return:
        """
        DATE_TIME =[]
        [DATE_TIME.append(DATE + " " + TIME) for (DATE, TIME) in zip(df['DATE'], df['TIME'])]
        df.insert(0, 'DATE_TIME', DATE_TIME) #incère la colone a la position O
        return df

    def formatDatetime(self, df,context):
        """

        :param df:
        :param context:
        :return:
        """

        df[context['t_name']] = pd.to_datetime(df[context['t_name']])
        return  df

    def time2greg(sel,df,context):
        """
        Transform Date time into gregorian time
        :param df: dataframe
        :param context:  need t_name column and Sart date time to convert (1899, 12, 30)
        :return: dataframe
        """
        START_DATE = datetime(1899, 12, 30)
        df[context['t_name']]= df[context['t_name']].apply(lambda x : (START_DATE+timedelta(x)).strftime('%Y-%m-%d %H:%M:%S'))
        return df

    def popCol (self, df, name):
        df.pop( name )
        return df


class CalcApasch():

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('Cte.ini')
        self.Cte_general = config['CTE_SEA']
        Cte_Ph_Calcul = config['CTE_PH']
        Cte_Alc_calcul = config['CTE_ALC']

        self.Vpompe = float(Cte_Alc_calcul['Vpompe'])
        self.Vcuve = float(Cte_Alc_calcul['Vcuve'])

        self.stock = float(Cte_Ph_Calcul['stock'])
        self.Vcell = float(Cte_Ph_Calcul['Vcell'])
        self.Vstroke = float(Cte_Ph_Calcul['Vstroke'])
        self.Sea_surface_T = float(self.Cte_general['Sea_surface_T'])
        self.Sea_surface_S = float(self.Cte_general['Sea_surface_S'])

        self.HFo_CWA=0.161878447824879    # concentration de HFo dans le stock de CWA
        self.C_HFo=self.HFo_CWA*(self.Vpompe*4)/(self.Vcuve+self.Vpompe*4)
        self.dilu_ech=self.Vcuve/(self.Vcuve+self.Vpompe*4)

    def calculPh(self, data, val):
        self.Sea_surface_S = val['salinity']

        """"""
        self.C_HFo = self.HFo_CWA * (self.Vpompe * 4) / (self.Vcuve + self.Vpompe * 4)
        self.dilu_ech = self.Vcuve / (self.Vcuve + self.Vpompe * 4)  # dilution de l'échantillon_
        e1 = -0.007762 + 4.5174e-5 * self.Sea_surface_T
        e3bye2 = -0.020813 + 2.60262e-4 * self.Sea_surface_T + 1.0436e-4 * (self.Sea_surface_S - 35)
        a = -246.64209 + 0.315971 * self.Sea_surface_S + 2.8855e-4 * self.Sea_surface_S ** 2
        b = 7229.23864 - 7.098137 * self.Sea_surface_S - 0.057034 * self.Sea_surface_S ** 2
        c = 44.493382 - 0.052711 * self.Sea_surface_S
        d = 0.0781344
        pK2e2 = a + b / self.Sea_surface_T + c * np.log10(self.Sea_surface_T) - d * self.Sea_surface_T


        Abs1 = []
        Abs2 = []
        Abs3 = []
        R_inc = []
        T_moy = []
        avg_led_1 = []
        avg_led_2 = []
        avg_led_3 = []
        avg_T = []
        e1_apasch = []
        e4_apasch = []


        cycle = np.reshape(data.to_numpy(), (5, 3, 12))
        for j in cycle:
            avg_led_1.append(np.mean(j[0:3, 3]))
            avg_led_2.append(np.mean(j[0:3, 4]))
            avg_led_3.append(np.mean(j[0:3, 5]))
            avg_T.append(np.mean(273.15 + j[0:3, 10] / 100))

        for a in range(0, 4):
            Abs1.append(np.log10(avg_led_1[0]) / avg_led_1[a + 1])
            Abs2.append(np.log10(avg_led_2[0]) / avg_led_2[a + 1] - Abs1[a])
            Abs3.append(np.log10(avg_led_3[0]) / avg_led_3[a + 1] - Abs1[a])
            R_inc.append(Abs2[a] / Abs3[a])

        for a in range(0, 4):
                # e1_apasch=3495.945318+1.074868*avg_T[a+1]-(88693.999793/avg_T[a+1])-617.614166*np.log(avg_T[a+1])
                # e4_apasch = -0.0306923086+0.0004114445*avg_T[a+1]+0.000065781*self.Sea_surface_S
                e1_apasch = 0.0170595
                e4_apasch = 1.560023E3 + 4.811158E-1 * avg_T[
                    a + 1] + 1.146155E-1 * self.Sea_surface_S - 1.933045E-3 * self.Sea_surface_S * self.Sea_surface_S - 3.958658E4 / \
                            avg_T[a + 1] - 2.75658E2 * np.log(avg_T[a + 1]) - 2.026206E-2 * np.log(
                    avg_T[a + 1]) * self.Sea_surface_S + 3.418927E-4 * np.log(avg_T[a + 1]) * self.Sea_surface_S ** 2

                pK2e2 = 1.262784E2 - 4.640924 * self.Sea_surface_S + 3.34405E-3 * self.Sea_surface_S ** 2 - (
                    4.154957E+3) / avg_T[a + 1] - (1.834135E1) * np.log(avg_T[a + 1]) + (
                                    1.947547E2 * self.Sea_surface_S) / avg_T[
                            a + 1] + 6.987689E-1 * self.Sea_surface_S * np.log(
                    avg_T[a + 1]) - 5.741784E-4 * self.Sea_surface_S ** 2 * np.log(avg_T[a + 1]);

                # pK2e2_corr = -4848.0239-1.455758*avg_T[a+1]+6.085273*avg_T[a+1]-5.862947E-5*self.Sea_surface_S**2+1.261238E+5/avg_T[a+1]+8.541799E+2*np.log(avg_T[a+1])-(2.590371E+2*self.Sea_surface_S)/avg_T[a+1]+(3.398063E-2*self.Sea_surface_S**2)/avg_T[a+1]-9.164758E-1*self.Sea_surface_S*np.log(avg_T[a+1])
                pHj_corr = pK2e2 + np.log10((R_inc[a] - e1_apasch) / (1 - R_inc[a] * e4_apasch))

                #print("{}, {}, {}, {}".format(pK2e2, e1_apasch, e4_apasch, pHj_corr))


if __name__=="__main__":
    run = ReadFile()
    path = os.getcwd()
    context = {"header":0,
                "sep":'\s+',
                "ext":'txt',
                "col":[],
                "t_format": '%Y/%m/%d %H:%M:%S',
                "t_name" : 'DATE_TIME',
                "path": path+ "\DATA\*."
               }



    df = run.readFid(run.makeList(context),context)
    df = run.concat_DT(df)
    df = run.formatDatetime(df,context)
    df = run.popCol(df, 'DATE')
    df = run.popCol(df, 'TIME')

