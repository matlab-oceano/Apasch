#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 06:02:55 2021

@author: spi-2017-12
"""
from class_main import *
from tkinter import *
import matplotlib.pyplot as plt
import csv

class commande(Main):

    def __init__(self):
        super().__init__ ()
        super().conf()



    def modesingle(self, cmd):
        if "RINCE" in cmd:
            self.rince_cel(cmd)
        else:
            super().apasch.cmdsimple(cmd=cmd)
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
                    super( ).apasch.cmdsimple(send)
                    if send == "K":
                        time.sleep(cmd["Tp"])
                    time.sleep(cmd["Tr"])
            print("{} ---> Rinçage fini".format(time.strftime('%Y/%m/%d %H:%M:%S ')))
        except:
            print(" {} ---> it seems like {} does not exist ".format(time.strftime('%Y/%m/%d %H:%M:%S '), cel))

        return time.strftime('%Y/%m/%d %H:%M:%S ')


    def cmd_simple(self, cmd):
        if cmd !="exit":
            try:
                send = self.GENERAL[cmd]['send']
                print(" {} ---> send {}  ".format(time.strftime('%Y/%m/%d %H:%M:%S '), send))
#                print (self.apasch.send(send,tr=self.GENERAL[cmd]['Tr']))
                return (self.apasch.send(send,tr=self.GENERAL[cmd]['Tr']))

            except:
                print(" {} ---> it seems like {} does not exist here ".format(time.strftime('%Y/%m/%d %H:%M:%S '),cmd))
                return "error"


    def cycle(self, cycle, sauve, count):
       # super().clear_screen()
        for key in self.GENERAL[cycle]:
            it = 0
            while it < key["iteration"]:
                it+=1
                read = {key: '' for key in self.SAUVE["HEADER"]}
                for send in key["send"]:
                   # time.sleep(0.4)

                    # effacer la console
                    # affichage à l'ecran
                    print("Cycle {} , {}_{} : ".format(count ,key['display'],it))
                    CTE=self.CTE["THERMISTANCE"]
                    cmd=send
                    commande=self.cmd_simple(cmd)
                    # mise à jour read
                    super( ).update_read(read,count,key,cycle,commande,CTE)
                    sauve.write(read)
                    self.data_cycle = self.data_cycle.append(read, ignore_index=True)
                    print(self.data_cycle.tail(1))

    def modeAuto_Ph(self, count , apa):
            self.cycle("PH1", self.save_Raw_ph, count)
            cycle_brut=self.data_cycle
            # Calcul du pH
            if count == 0 : cycle_brut.drop(0,0,inplace=True)
            apa.calcul_pH(cycle_brut.tail(15))
            return apa.data_calcule


    def modeAuto_ALC(self, count,apa):

            self.cycle("ALC", self.save_Raw_Alc, count)
            cycle_brut=self.data_cycle
            # Calcul de l'alcalinité
            if count == 0 : cycle_brut.drop(0,0,inplace=True)
            apa.calcul_alk_ed_cycle(cycle_brut.tail(15),apa.water)
            return apa.data_alk_calcule

    def launch (self,cmd='cycle',running='True') :

       # main = commande()
        k = plot_ph()
        a = self.filename
        apa=Apasch()
        apa.water = 'douce'
        print('Vous avez choisi la commande : ', cmd)
        name = ''

        fieldnames = ["Datetime", "Temp", "pH"]
        with open('data.txt', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()

        while cmd != "stop":
         #   cmd = input("enter mode (cycle/single/test/stop)? ")
            if cmd == "cycle":
                try:
                    COUNT = 0
                    #while COUNT < 2 :
                    while running:
                        if self.GENERAL["PH_ACTIVE"]:
                            pH = self.modeAuto_Ph(COUNT,apa)
                            print(pH)
                            #commande().clear_screen()

                            with open('data.txt', 'a') as csv_file:
                                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                                info = {
                                    "Datetime": pH.iloc[-1,0],
                                    "Temp": pH.iloc[-1,1],
                                    "pH": pH.iloc[-1,2]
                                }
                                csv_writer.writerow(info)
                        if self.GENERAL["ALC_ACTIVE"]:
                            alc = self.modeAuto_ALC(COUNT,apa)
                            #commande().clear_screen()
                            print(alc[['DATE+HEURE','CYCLE',
                                                            'TEMP','Alc 1','Alc 2','Alc 3','Alc Sb']])

                            alk = alc[['DATE+HEURE','TEMP','Alc Sb']].round(4)
                            with open('data.txt', 'a') as csv_file:
                                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                                info = {
                                    "Datetime": alk.iloc[-1,0],
                                    "Temp": alk.iloc[-1,1],
                                    "pH": alk.iloc[-1,2]
                                }
                                csv_writer.writerow(info)


                        COUNT += 1
                except KeyboardInterrupt:
                    print("boucle interrompue")

            elif cmd == "single":
                while name != "exit":
                    print(name)
                    name = input("What is your command? or exit: ")
                    sequence = self.cmd_simple(name)
            elif cmd == "test":
                print(self.trame())
                print(self.tsg())
            elif cmd == "stop":
                self.data_cycle







    def launch2 (self,cmd,running) :

        print('Vous avez choisi la commande : ', cmd)
        while cmd != "stop":
         #   cmd = input("enter mode (cycle/single/test/stop)? ")
            if cmd == "cycle":
                    while running:
                        print(running)
                        print('ça tourne')

            elif cmd == "test":
                print(self.trame())
                print(self.tsg())
            elif cmd == "stop":
                self.data_cycle



if __name__ == '__main__':
    commande().launch()
