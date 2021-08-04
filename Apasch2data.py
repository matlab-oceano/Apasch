# -*- coding: utf-8 -*-

from math import log as ln


class calc():

    def __init__(self):

        # constantes equation de Steinhart-Hart  ASLEC PH_ALC entre -2 et 32°C :
        self.A = 1.464160e-3
        self.B = 2.389356e-4
        self.C = 0.987137e-7

    def temperature(self, cycle, data, CTE):
        self.R0 = CTE["R0"]
        self.Rl = CTE["RL"]
        self.Rh = CTE["RH"]
    
        Data = data[1::].split()
        I1 = int(Data[0])
        I2 = int(Data[1])
        I3 = int(Data[2])
        NH = int(Data[3])
        Nl = int(Data[4])
        NTH = int(Data[5])
        Nth1 = 0
        Nl1 = 0

        if Nl > 4095:
            Nl1 = Nl - 8192

        if NTH > 1000:
            Nth1 = NTH - 8192

        if NH != 0 and Nl != 0:
            Nh1 = NH
            Ks = (float(Nth1) - float(Nl1)) / (float(Nh1) - float(Nl1))
            Bs = self.Rl / (self.Rl + self.R0)
            As = self.R0 * (self.Rh - self.Rl) / ((self.R0 + self.Rl) * (self.R0 + self.Rh))
            Rth = self.R0 * (As * Ks + Bs) / (1 - (As * Ks + Bs))
        else:
            Rth = 2252

        Lrth = ln(Rth)
        if cycle == "PH1":
            # constantes equation de Steinhart-Hart  ASLEC PH sn 002 (LGE) entre -2 et 32°C :
            self.A3 = 1.465947e-3
            self.B3 = 2.38508e-4
            self.C3 = 1.00287e-7

        else:
            # constantes equation de Steinhart-Hart  ASLEC ALC sn 002 (LGE) entre -2 et 32°C :
            self.A3 = 1.474508e-3
            self.B3 = 2.36749e-4
            self.C3 = 1.10191e-7

        Itk = self.A3 + self.B3 * Lrth + self.C3 * Lrth * Lrth * Lrth
        Tc = 1 / Itk - 273.15
        Rth = int(Rth)
        Tc = round(Tc, 2)

        Mesure = {
                     "LAMBDA_1": I1,
                     "LAMBDA_2": I2,
                     "LAMBDA_3": I3,
                     "NH": NH,
                     "NL": Nl,
                     "Nth": NTH,
                     "100_T_cel": Rth,
                     "T_cel": Tc}
        return Mesure

"""    def calc_ph(self, data):
        
        t_start = min(data.index)
        t_stop = max(data.index)
        avg_T_apasch = data["T_cel"].mean()
        S = df_ths.loc[t_start:t_stop, 'salinity'].mean()  # salinité moyenne TSG
        tmoy = df_ths.loc[t_start:t_stop, 'intaketemp'].mean()  # température moyenne TSG
        cycle = cycle.set_index(head, append=True)
        cycle.index = cycle.index.rename(["date", "Cycle"])
        cycle = cycle.groupby(['Cycle']).mean()
        cycle_transpo = cycle.T

        abs_1 = [np.log10(cycle_transpo.loc["LAMBDA_1"][0] / cycle_transpo.loc["LAMBDA_1"][n + 1]) for n in range(0, 4)]
        abs_2 = [np.log10(cycle_transpo.loc["LAMBDA_2"][0] / cycle_transpo.loc["LAMBDA_2"][n + 1]) for n in range(0, 4)]
        abs_3 = [np.log10(cycle_transpo.loc["LAMBDA_3"][0] / cycle_transpo.loc["LAMBDA_3"][n + 1]) for n in range(0, 4)]
        R_indic = [abs_2[n] / abs_3[n] for n in range(0, 4)]
        Tki = 273.15 + tmoy

        e1 = 623.6451 + 0.1879518 * Tki - (1.603867e4 / Tki) - 1.098485e2 * np.log(Tki)

        e4 = 1.560023e3 + 4.811158e-1 * Tki + 1.146155e-1 * S - 1.933045e-3 * S ** 2 - 3.958658e4 / Tki - 2.75658e2 * np.log(
            Tki) - 2.026206e-2 * np.log(Tki) * S + 3.418927e-4 * np.log(Tki) * S ** 2
        pK2e2_corr = 126.1934 - 4.640924 * S + 3.34405e-3 * S ** 2 - 4.154957e3 / Tki - 1.834135e1 * np.log(Tki) + (
                    1.947547e2 * S) / Tki + 6.987689e-1 * S * np.log(Tki) - 5.741784e-4 * S ** 2 * np.log(Tki)

        pHj_corr = [pK2e2_corr + np.log10((R_indic[n] - e1) / (1 - R_indic[n] * e4)) for n in range(0, 4)]
        return data
"""
"""    def calc_alc(self, data):

        print("mesure alcalinité")

        return data
"""
