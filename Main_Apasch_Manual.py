# -*- coding: utf-8 -*-

import re
from socket import *
import serial
import time
import os
from optparse import OptionParser
from math import log as ln


class acq_serie(object):
    def __init__(self, setparser):
        self.port = "/dev/ttyUSB0"
        self.baudrate = 9600
        self.ser = ''
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=10, xonxoff=False, rtscts=False, dsrdtr=False)
            self.ser.flushInput()
            self.ser.flushOutput()
            print("configuré")
        except IOError:
            print ("Erreur ouverture port serie " + self.port)
            exit()

    def read(self, parametre):
    #CHANGER ICI LES TEMPORISATIONS POMPE EAU ON OFF
        TimePh=15
        TimeAlc=15
    ################################################
        out = ""
        

        if parametre=="K":
            print("Démmarage_pompe_eau")
            self.ser.write("K".encode())
            time.sleep(0.5)
            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "L":  # ok
            print ("arret pompe à eau")
            self.ser.write("L")
            time.sleep(0.5)
            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "M":  # ok
            print(" Macro com Alc")
            self.ser.write("M".encode())
            time.sleep(25)
            while self.ser.inWaiting() > 0:
                out += self.ser.read(1).decode()

            if out != '':
                print(out)
                return out

            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "N":  # ok
            self.ser.write("N".encode())
            print(" Macro com pH")
            time.sleep(23)
            while self.ser.inWaiting() > 0:
                out += self.ser.read(1).decode()

            if out != '':
                print(out)
                return out

            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "B":  #mesure blanc Alcalinité

            self.ser.write("B".encode())
            time.sleep(7)
            while self.ser.inWaiting() > 0:
                out += self.ser.read(1).decode()

            if out != '':
                return out
            self.ser.flushOutput()
        elif parametre == "C":  # Mesure blanc pH
            self.ser.write("C".encode())
            time.sleep(7)
            while self.ser.inWaiting() > 0:
                out += self.ser.read(1).decode()
            if out != '':
                print(out)
                return out
            self.ser.flushOutput()
        elif parametre == "rinçage-Ph":  # fini a tester
            i = 1
            while i < 3:
                print(" rinçage-ph : {0}".format(i))
                self.ser.write("K".encode())
                self.ser.flushOutput()
                time.sleep(TimePh)
                self.ser.write("L".encode())
                self.ser.flushOutput()
                time.sleep(0.5)
                self.ser.write("S".encode())
                self.ser.flushOutput()
                time.sleep(TimePh)
                self.ser.write("T".encode())
                self.ser.flushOutput()
                time.sleep(0.5)
                i += 1

            time.sleep(0.5)
            self.ser.write("K".encode())
            self.ser.flushOutput()
            time.sleep(15)
            self.ser.write("L".encode())
            self.ser.flushOutput()
            time.sleep(10)
            i+= 1
            print("fin du rinçage-ph")
            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "rinçage-alc":  # fini a tester
            i = 1
            while i < 3:
                print(" rinçage-Alc : {0}".format(i))
                self.ser.write("K".encode())
                self.ser.flushOutput()
                time.sleep(TimeAlc)
                self.ser.write("L".encode())
                self.ser.flushOutput()
                time.sleep(0.5)
                self.ser.write("Q".encode())
                self.ser.flushOutput()
                time.sleep(TimeAlc)
                self.ser.write("R".encode())
                self.ser.flushOutput()
                time.sleep(0.5)
                i += 1

            time.sleep(0.5)
            self.ser.write("K".encode())
            self.ser.flushOutput()
            time.sleep(15)
            self.ser.write("L".encode())
            self.ser.flushOutput()
            time.sleep(10)
            i += 1
            print("fin du rinçage-Alc")
            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "read_sensor":
            while self.ser.inWaiting() > 0:
                out += self.ser.read(1).decode()
            if out != '':
                out=out.split('\r\n')
                print ("valeur brut {0}".format(out))
                return out
            self.ser.flushInput()
            self.ser.flushOutput()
        elif parametre == "J":
            self.ser.write("J".encode())
            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "E":
            self.ser.write("E".encode())
            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "S": #demarrage agitateur Ph
            self.ser.write("S".encode())
            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "T": #arret agitateur Ph
            self.ser.write("T".encode())
            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "Q": #demarrage agitateur Ph
            self.ser.write("Q".encode())
            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "R": #arret agitateur Ph
            self.ser.write("R".encode())
            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "2": #mesure T voie 2
            self.ser.write("2".encode())
            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "3": #electovanne on  Ph
            self.ser.write("3".encode())
            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "4": #electovanne off Ph
            self.ser.write("4".encode())
            self.ser.flushOutput()
            self.ser.flushInput()

    def close(self):
        self.ser.close()

class calc(object):
    def __init__(self,setparser):
        options = 3
        if options == 1:
            self.R0 = 21008.0
            self.RL = 1958.5
            self.RH = 7868.4
        elif options == 2:
            self.R0 = 21004.0
            self.RL = 1958.7
            self.RH = 7867.6
        elif options == 3:
            self.R0 = 20987.0
            self.Rl = 1960.5
            self.Rh = 7868.2
        elif options == 4:
            self.R0 = 20996.0
            self.Rl = 1960.6
            self.Rh = 7869.4
        elif options == "theorique":
            self.R0 = 21000.0
            self.Rl = 1960.0

        # constantes equation de Steinhart-Hart  ASLEC PH_ALC entre -2 et 32°C :
        self.A = 1.464160e-3
        self.B = 2.389356e-4
        self.C = 0.987137e-7
        # constantes equation de Steinhart-Hart  ASLEC PH sn 002 (LGE) entre -2 et 32°C :

        self.A3 = 1.465947e-3
        self.B3 = 2.38508e-4
        self.C3 = 1.00287e-7
        # constantes equation de Steinhart-Hart  ASLEC ALC sn 002 (LGE) entre -2 et 32°C :
        """self.A1 = 1.474508e-3
            self.B1 = 2.36749e-4
            self.C1 = 1.10191e-7
        # repertoire écriture des données"""

    def temperature(self,data):

        #print (data[4:8],data[10:14],data[16:20])
        Data = data[4::].split()
        
        I1 = int(Data[0])
        I2 = int(Data[1])
        I3 = int(Data[2])
        Nh = int(Data[3])
        Nl = int(Data[4])
        Nth = int(Data[5])

        if Nl > 4095:
            Nl1 = Nl - 8192

        if Nth > 4095:
            Nth1 = Nth - 8192


        if Nh != 0 and Nl != 0:
            Nh1=Nh
            Ks = (float(Nth1) - float(Nl1)) / (float(Nh1) - float(Nl1))
            Bs = self.Rl / (self.Rl + self.R0)
            As = self.R0 * (self.Rh - self.Rl) / ((self.R0 + self.Rl) * (self.R0 + self.Rh))
            Rth = self.R0 *( As * Ks + Bs) / (1 - (As * Ks + Bs))
        else :
            Rth=2252

        Lrth=ln(Rth)
        Itk=self.A3+self.B3*Lrth+self.C3*Lrth*Lrth*Lrth
        Tc=1/Itk-273.15
        Rth=int(Rth)
        Tc=round(Tc,2)

        Mesure=("{0} {1} {2} {3} {4} {5} {6} {7}".format(I1, I2, I3, Nh,Nl,Nth,Rth,Tc))
        return Mesure


    def calc_ph(self,data):
        print ("mesure du pH")
        return data
    def calc_alc(self,data):
        print ("mesure alcalinité")
        return data

class sauve():
    def __init__(self, date, setparser):

            self.file_path = os.getcwd() + "/" + '3' + "_" + date + ".dat"
            self.file_save = open(self.file_path, "a")
            print(self.file_path)
    def sauve(self,data):
        with open(self.file_path, 'a') as f:
            f.write(data+"\r\n")
    def close(self):
            self.file_path.close()




if __name__ == '__main__':

    date = time.strftime('%Y%m%d%H%M%S')
    out_f = os.getcwd()
    print("lancement application apache il est {0} ""le fichier de destitation est {1}".format(date, out_f))


    parser = OptionParser('usage du $prog'
                          '-o fichier de destination'
                          '-s vitesse du port'
                          '-p port ')
    parser.add_option("-o", "--output", dest="out_f",
                      help="fichier de destination des données ",
                      default=out_f)
    parser.add_option("-p", "--port", dest="port",
                      help="port (/dev/ttyUSB') ",
                      default='/dev/ttyUSB0')
    parser.add_option("-s", "--speed", dest="baudrate",
                      help="vitesse ",
                      default=9600)
    parser.add_option("-v", "--version", dest="version",
                      help="type de version ",
                      default="3")
    setparser = parser.parse_args()


    cmd = acq_serie(setparser)
    save = sauve(date, setparser)
    conv=calc(setparser)

    entrer = 1
    while 1:  # envoie des commandes manuellement
        entrer = input(">> ")
        cnt=0
        if entrer == "exit":
            donnees = cmd.close()
            exit()
        elif entrer == "PH-Alc":  # séquence Ph-Alc"
            print("*******************************")
            print("démarrage de la séquence Ph-Alc")
            print("*******************************")
            donnees = cmd.read(input)

        elif entrer == "Ph":  # séquence Ph
            cnt+=1
            n = 1
          


            print("*******************************")
            print("démarrage de la séquence Ph")
            print("*******************************")

            donnees = cmd.read("rinçage-Ph")



            while n < 4:
                donnees = cmd.read("C")
                data = conv.temperature(donnees)
                Data_to_save = ("{} {} Blanc_pH {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data))
                #Data_to_save = time.strftime('%Y/%m/%d %H:%M:%S ')+cnt + " blanc_pH " + data
                print (Data_to_save)

                save.sauve(Data_to_save)
                n += 1
            n = 1

            while n < 5:
                print("{0} cycle de micro_com pH".format(n))
                donnees = cmd.read("N")
                data = conv.temperature(donnees)
                Data_to_save = ("{} {} Mesure_pH {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data))
                print (Data_to_save)
                save.sauve(Data_to_save)
                time.sleep(0.5)
                donnees = cmd.read("C")
                data = conv.temperature(donnees)
                Data_to_save = ("{} {} Mesure_pH {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data))
                print (Data_to_save)
                save.sauve(Data_to_save)
                time.sleep(0.5)
                donnees = cmd.read("C")
                data = conv.temperature(donnees)
                Data_to_save = ("{} {} Mesure_pH {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data))
                print (Data_to_save)
                save.sauve(Data_to_save)
                time.sleep(0.5)
                n += 1
            donnees = cmd.read("rinçage-Ph")

        elif entrer == "Alc":  # séquence Alc
            n = 1
            cnt+=1
            print("*******************************")
            print("démarrage de la séquence Alc")
            print("*******************************")
            donnees = cmd.read("rinçage-alc")

            while n < 4:
                donnees = cmd.read("B")
                data = conv.temperature(donnees)
                Data_to_save = ("{} {} Blanc_Alc {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data))
                print (Data_to_save)

                save.sauve(Data_to_save)
                n += 1
            n = 1

            while n < 2:
                print("{0} cycle de micro_com Alc".format(n))
                donnees = cmd.read("M")
                data = conv.temperature(donnees)
                Data_to_save = ("{} {} Mesure_Alc {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data))
                print (Data_to_save)
                save.sauve(Data_to_save)
                time.sleep(0.5)
                donnees = cmd.read("B")
                data = conv.temperature(donnees)
                Data_to_save = ("{} {} Mesure_Alc {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data))
                print (Data_to_save)
                save.sauve(Data_to_save)
                time.sleep(0.5)
                donnees = cmd.read("B")
                data = conv.temperature(donnees)
                Data_to_save = ("{} {} Mesure_Alc {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data))
                print (Data_to_save)
                save.sauve(Data_to_save)
                time.sleep(0.5)
                n += 1
            donnees = cmd.read("rinçage-alc")

        elif entrer == "PH-PH2":  # séquence Ph-Ph2
            print("*******************************")
            print("démarrage de la séquence Ph-Ph2")
            print("*******************************")
            donnees = cmd.read(input)

        elif entrer == "PH3":  # séquence Ph3
            print ("*******************************")
            print("démarrage de la séquence Ph3")
            print("*******************************")
            donnees = cmd.read(input)
        elif entrer == "PH2":  # séquence Ph2
            print("*******************************")
            print("démarrage de la séquence Ph2")
            print("*******************************")
            n = 1
            donnees = cmd.read("rinçage-alc")
            while n < 4:
                donnees = cmd.read("B")
                n += 1
            n = 1
            while n < 5:
                donnees = cmd.read("Y")
                donnees = cmd.read("B")
                donnees = cmd.read("B")
            donnees = cmd.read("rinçage-alc")
        elif entrer == "C":  # mesure du blanc Ph
            print("*******************************")
            print("démarrage de la mesure de blanc pH")
            print("*******************************")
            donnees = cmd.read("C")
            data = conv.temperature(donnees)
            Data_to_save = time.strftime('%Y/%m/%d %H:%M:%S ') + "blanc_pH " + data
            print(Data_to_save)
        elif entrer == "B":  # mesure du blanc Alc
            print("*******************************")
            print("démarrage de la mesure de blanc alc")
            print("*******************************")
            donnees = cmd.read("B")
            data=conv.temperature(donnees)
            print(data)

            Data_to_save = time.strftime('%Y/%m/%d %H:%M:%S ') + "blanc_ALC " + donnees[4::]
            print(Data_to_save)
        elif entrer == "L": # pompe eau off
            donnees = cmd.read(input)
            donnees = cmd.read("read_sensor")
        elif entrer == "K": # pompe eau on
            donnees = cmd.read(input)
            donnees = cmd.read("read_sensor")
        elif entrer =="9":#mesure de temprature interne"
            donnees=cmd.read(input)
            time.sleep(1)
            donnees=cmd.read("read_sensor")
            print (donnees)
        elif entrer=="cal_ph":
            print("*******************************")
            print("démarrage de la calibration PH")
            print("*******************************")
        elif entrer=="cal_alc":
            print("*******************************")
            print("démarrage de la calibration alc")
            print("*******************************")
        elif entrer=="1":
            donnees = cmd.read(input)
            print("*******************************")
            print("mesure de T voie 1 alcalinité")
            print("*******************************")
            time.sleep(1)
            donnees=cmd.read("read_sensor")
        elif entrer=="2":
            donnees = cmd.read(input)
            print("*******************************")
            print("mesure de T voie 2 pH")
            print("*******************************")
            time.sleep(1)
            donnees = cmd.read("read_sensor")
            print (donnees)
        elif entrer=="3":
            donnees = cmd.read(input)
            print("*******************************")
            print("activation electrovanne")
            print("*******************************")
            time.sleep(1)
            donnees = cmd.read("read_sensor")
        elif entrer=="4":
            donnees = cmd.read(input)
            print("*******************************")
            print("fermeture electrovanne")
            print("*******************************")
            time.sleep(1)
            donnees = cmd.read("read_sensor")
        elif entrer == "J": #amorçage collorant Ph
            donnees = cmd.read(input)
            print("10 coup de pompe Ph")
            donnees = cmd.read("read_sensor")
        elif entrer == "E": #amorçage collorant Alc
            donnees = cmd.read(input)
            print("10 coup de pompe Alc")
            donnees = cmd.read("read_sensor")
        elif entrer =="Read":
            donnees=cmd.read(input)
            time.sleep(1)
            donnees=cmd.read("read_sensor")
            print (donnees)
        elif entrer =="S":
            print("Agitateur Ph On")
            donnees=cmd.read(input)
            time.sleep(1)
            donnees=cmd.read("S")
        elif entrer =="T": #Agitateur Ph Off
            print("Agitateur Ph Off")
            donnees=cmd.read(input)
            time.sleep(1)
            donnees=cmd.read("T")
        elif entrer =="Q": #Agitateur Alc On
            print("Agitateur Alc On")
            donnees=cmd.read(input)
            time.sleep(1)
            donnees=cmd.read("Q")
        elif entrer =="R": #Agitateur Alc Off
            print("Agitateur Alc Off")
            donnees=cmd.read(input)
            time.sleep(1)
            donnees=cmd.read("R")
        elif entrer =="N": #macro mesure ph
            print("macro mesure ph")
            time.sleep(1)
            donnees=cmd.read("N")
        elif entrer =="M": #macro mesure Alc
            print("macro mesure Alc")
            time.sleep(1)
            donnees=cmd.read("M")
