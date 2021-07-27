# -*- coding: utf-8 -*-

import yaml
from apasch_class_alc import *
import Apasch_cycles
import UDP_Read
import time
import save_Data
import Apasch2data
import dataBuffer
import pandas as pd
# import only system from os
from os import system, name

def display (self , mtype , message) :
    if mtype == 'error' :
        print("\033[91m {}  \033[89m".format(message))
    
    

def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear') 

class Main():

    def __init__(self):

        ###############_Init from conf file_###############
        yaml_content = yaml.safe_load(open("conf.yml", 'r'))
        self.TSG = yaml_content["TSG"]
        self.UDP = yaml_content["TSG"]
        self.NTP = yaml_content["NTP"]
        self.NMEA = yaml_content["NMEA"]
        self.GENERAL = yaml_content["GENERAL"]
        self.SAUVE = yaml_content["SAUVE"]
        self.CTE = yaml_content["CTE"]
        self.apasch = Apasch_cycles.Interface(yaml_content["RS232"])
        self.conv = Apasch2data.calc()
        self.data_cycle=pd.DataFrame([{key: '' for key in self.SAUVE["HEADER"]}])


    def conf(self):

        #############_init UDP NMEA_########################
        if self.NMEA['is_active']:
            try:
                self.nav = UDP_Read.Udp(self.NMEA)
            except:
                print("connection error on UDP NMEA")
        else:
            print("\033[91m NMEA is not activate  \033[89m")

        #############_init TSG_#############################
        if self.TSG['is_active']:
            try:
                self.termosalino = UDP_Read.Udp(self.TSG)
            except:
                print("connection error on UDP TSG")

        if self.GENERAL["PH_ACTIVE"]:
            print('Voie pH activé')
            self.save_Raw_ph = save_Data.Save(PARAM=self.SAUVE, type="RAW",name="PH" )

        if self.GENERAL["ALC_ACTIVE"]:
            print('Voie Alcalinité activé')
            self.save_Raw_Alc = save_Data.Save(PARAM=self.SAUVE, type="RAW", name="ALC")

        return self.GENERAL

    def trame(self):
        if self.NMEA['is_active']:
            return self.nav.read_Udp()
        else:
            return {"NMEA": "nan"}

    def tsg(self):
        if self.TSG['is_active']:
            return self.termosalino.read_Udp()
        else:
            return {"TSG": ""}

    def modesingle(self, cmd):
        if "RINCE" in cmd:
            self.rince_cel(cmd)

        else:
            self.apasch.cmdsimple(cmd=cmd)
        return "message envoyé single"

    def rince_cel(self, cel):

        n = 0
        cmd = self.GENERAL[cel]

        try:

            while n < cmd["nb_seq"]:
                n += 1
                print("{} n° {} de la celulle".format(cmd["display"], n))
                for send in cmd["send"]:
                    print(" {} ---> send {}  ".format(time.strftime('%Y/%m/%d %H:%M:%S '), send))
                    self.apasch.cmdsimple(send)
                    if send == "K":
                        time.sleep(cmd["Tp"])
                    time.sleep(cmd["Tr"])
            print("{} ---> Rinçage fini".format(time.strftime('%Y/%m/%d %H:%M:%S ')))
        except:
            print(" {} ---> it seems like {} does not exist ".format(time.strftime('%Y/%m/%d %H:%M:%S '), cel))

        return time.strftime('%Y/%m/%d %H:%M:%S ')

    def cycle(self, cycle, sauve, count):
        data_cycle = pd.DataFrame(columns=self.SAUVE["HEADER"])
        for key in self.GENERAL[cycle]:
            it = 0
            while it < key["iteration"]:
                it+=1
                read = {key: '' for key in self.SAUVE["HEADER"]}
                ### A verifier ! 
                read.update({
                    "DATETIME": time.strftime('%Y/%m/%d %H:%M:%S '),
                    "COUNT": count,
                    "TYPE": key['display'],
                    })
                read.update(self.trame())
                read.update(self.tsg())
                for send in key["send"]:
                    
                  #  clear_screen()
                    # sys.stdout.write("\r" +"Rinçage du cycle {} il reste {} secondes   ". format(n['name'],int(time_f-time.time())))
                    # sys.stdout.flush()
                    # time.sleep(1)
                    # sys.stdout.write("\n")
                    
                    print(" {} --->{}_{}_{} send {}  ".format(time.strftime('%Y/%m/%d %H:%M:%S '), key['display'],cycle,it, send ))
                    tr=self.GENERAL[send]["Tr"]
                    data=self.apasch.send(send,tr)
                    CTE=self.CTE["THERMISTANCE"]
                    read.update(self.conv.temperature(cycle,data,CTE))
                    
                    # read.update(self.conv.temperature(cycle=cycle,
                    #                               data=self.apasch.send(cmd=send,
                    #                               tr=self.GENERAL[send]["Tr"]),
                    #                               CTE=self.CTE["THERMISTANCE"]))
                    
                sauve.write(read)
                self.data_cycle = self.data_cycle.append(read, ignore_index=True)
                # print(self.data_cycle.tail(1))

        return data_cycle
    
    
    def cmd_simple(self, cmd):
        if cmd !="exit":
            try:
                send = self.GENERAL[cmd]['send']
                print(" {} ---> send {}  ".format(time.strftime('%Y/%m/%d %H:%M:%S '), send))
                print(self.apasch.send(send,tr=self.GENERAL[cmd]['Tr']))
            except:
                print(" {} ---> it seems like {} does not exist here ".format(time.strftime('%Y/%m/%d %H:%M:%S '),cmd))
                return "error"

    def close(self):
        pass

    def modeAuto_Ph(self, count):

 #       if self.GENERAL["PH_ACTIVE"]:
            # self.rince_cel(cel="RINCE_ph")
            self.cycle("PH1", self.save_Raw_ph, count)

            return

    def modeAuto_ALC(self, count,apa):
#        if self.GENERAL["ALC_ACTIVE"]:
            #self.rince_cel("RINCE_Alc")
            self.cycle("ALC", self.save_Raw_Alc, count)
            cycle_brut=self.data_cycle
            cycle_brut.drop(0,0,inplace=True)
            apa.calcul_alk_ed_cycle(cycle_brut)
            return (apa.data_alk_calcule)



if __name__ == '__main__':
    print('class main ok')