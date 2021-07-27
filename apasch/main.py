#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 15:16:59 2021

@author: spi-2017-12
"""

from Main_Apasch import * 

main = Main()
main.conf()
apa=Apasch()
cmd = ''
name = ''


while cmd != "stop":
    cmd = input("enter mode (cycle/single/test/stop)? ")
    if cmd == "cycle":
        try:
            COUNT = 0
            while COUNT < 2 :
         #   while True:
                if main.GENERAL["PH_ACTIVE"]:
                    ph = main.modeAuto_Ph(COUNT)
                if main.GENERAL["ALC_ACTIVE"]:
                    alc = main.modeAuto_ALC(COUNT,apa)
                    print(alc[['DATE+HEURE','CYCLE',
                                                    'TEMP','Alc 1','Alc 2','Alc 3','Alc Sb']])
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
        main.data_cycle