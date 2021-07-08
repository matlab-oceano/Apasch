# -*- coding: utf-8 -*-

import yaml

import Apasch_cycles
import UDP_Read
import time
import save_Data
import Apasch2data
import dataBuffer
import pandas as pd


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

        """self.GENERAL = {
            "PH_ACTIVE": True,
            "ALC_ACTIVE": True,
            "Q": {
                "send": "Q",
                "display": "stirrer_Alc_On"
            },
            "C": {
                "send": "C",
                "display": "Read_Ph"
            },
            "B": {
                "send": "B",
                "display": "Read_Alc"
            },
            "S": {
                "send": "S",
                "display": "stirrer_pH_On"
            },
            "R": {
                "send": "R",
                "display": "stirrer_Alc_Off"
            },
            "T": {
                "send": "T",
                "display": "stirrer_pH_Off"
            },
            "K": {
                "send": "K",
                "display": "Water_ON"
            },
            "L": {
                "send": "L",
                "display": "Water_OFF"
            },
            "N": {
                "send": "N",
                "display": "Macro_com_pH"
            },
            "M": {
                "send": "M",
                "display": "Macro_com_Alc"
            },
            "E" : {
                "send": "E",
                "display": "10 cps pompe Alc" 
            },
            "J" : {
                "send": "J",
                "display": "10 cps pompe pH"
            },
           "PH1": {
                "cycle_blanc": {
                    "iteration": 3,
                    "Tr": 6,
                    "send": "C",
                    "display": "Blanc_pH ",
                },
                "cycle_mesure": {
                    "iteration": 4,
                    "Tr": 26,
                    "send": "N",
                    "display": "Mesure_pH ",
                }},
            "ALC": {
                "cycle_blanc": {
                    "iteration": 3,
                    "Tr": 6,
                    "send": "C",
                    "display": "Blanc_Alc ",
                },
                "cycle_mesure": {
                    "iteration": 4,
                    "Tr": 24,
                    "send": "M",
                    "display": "Mesure_Alc ",
                }},
            "RINCE_ph": {
                "send": ["S", "K", "T", "L"],
                "Tp": 5,  # temps pompage
                "Tr": 1,  # temps repos
                "nb_seq": 3,
                "display": "rinçage pH"
            },
            "RINCE_Alc": {
                "send": ["Q", "K", "R", "L"],
                "Tp": 5,  # temps pompage
                "Tr": 1,  # temps repos
                "nb_seq": 3,
                "display": "rinçage Alc"
            }
        }"""

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
                print(" {} --->{}_{}_{} send {}  ".format(time.strftime('%Y/%m/%d %H:%M:%S '), key['display'],cycle,it, key['send'] ))
                read.update({
                    "DATETIME": time.strftime('%Y/%m/%d %H:%M:%S '),
                    "COUNT": count,
                    "TYPE": key['display'],
                    })
                read.update(self.trame())
                read.update(self.tsg())
                read.update(self.conv.temperature(cycle=cycle,
                                                  data=self.apasch.send(cmd=key['send'],
                                                  tr=key['Tr']),
                                                  CTE=self.CTE["THERMISTANCE"]))
                sauve.write(read)
                data_cycle = data_cycle.append(read, ignore_index=True)
                print(data_cycle.tail(1))

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

        if self.GENERAL["PH_ACTIVE"]:
            # self.rince_cel(cel="RINCE_ph")
            self.cycle("PH1", self.save_Raw_ph, count)

            return

    def modeAuto_ALC(self, count):
        if self.GENERAL["ALC_ACTIVE"]:
            #self.rince_cel("RINCE_Alc")
            self.cycle("ALC", self.save_Raw_Alc, count)

            return


if __name__ == '__main__':

    main = Main()
    main.conf()
    cmd = ''
    name = ''

    while cmd != "stop":
        cmd = input("enter mode (cycle/single/test/stop)? ")
        if cmd == "cycle":
            try:
                COUNT = 0
                while True:
                    ph = main.modeAuto_Ph(COUNT)
                    alc = main.modeAuto_ALC(COUNT)
                    COUNT += 1
            except KeyboardInterrupt:
                print("boucle interrompue")

        elif cmd == "single":
            while name != "exit":
                print(name)
                name = input("What is your command? or exit: ")
                sequence = main.cmd_simple(name)
        elif cmd == "test":
            print(main.trame())
            print(main.tsg())
        elif cmd == "stop":
            exit()
