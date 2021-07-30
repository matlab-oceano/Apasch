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
        self.save_Raw_ph = []
        self.save_Raw_Alc = []


    def clear_screen2(self):
            # for windows
        if name == 'nt':
            _ = system('cls')
            # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

    def clear_screen(self):
            # for windows
        print('')

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
            self.filename=self.save_Raw_ph.FID

        if self.GENERAL["ALC_ACTIVE"]:
            print('Voie Alcalinité activé')
            self.save_Raw_Alc = save_Data.Save(PARAM=self.SAUVE, type="RAW", name="ALC")
            self.filename=self.save_Raw_Alc.FID

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
        
    def update_read (self,read,count,key,cycle,data,CTE) :
        read.update({
                    "DATETIME": time.strftime('%Y/%m/%d %H:%M:%S '),
                    "COUNT": count,
                    "TYPE": key['display'],
                    })
        read.update(self.trame())
        read.update(self.tsg())
        read.update(self.conv.temperature(cycle,data,CTE))
