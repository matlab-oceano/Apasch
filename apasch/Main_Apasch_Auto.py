# -*- coding: utf-8 -*-

import re
from socket import *
import serial
import time
import os
from optparse import OptionParser
from math import log as ln
from time import gmtime, strftime


class AcqSerie():

    def __init__(self):

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

        timePh=15
        timeAlc=15
        out = ""
        i = 1


        if parametre=="K":

            print("Démmarage_pompe_eau")
            self.ser.write("K".encode())
            time.sleep(0.5)
            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "L":  # ok
            print ("arret pompe à eau")
            self.ser.write("L".encode())
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
                return out

            self.ser.flushOutput()
            self.ser.flushInput()
        elif parametre == "B":  # fini et tester implémenter la sauvegarde de la mesure

            self.ser.write("B".encode())
            time.sleep(7)
            while self.ser.inWaiting() > 0:
                out += self.ser.read(1).decode()

            if out != '':
                return out
            self.ser.flushOutput()
        elif parametre == "C":  # fini et tester implémenter la sauvegarde de la mesure
            self.ser.write("C".encode())
            time.sleep(7)
            while self.ser.inWaiting() > 0:
                out += self.ser.read(1).decode()

            if out != '':
                return out
            self.ser.flushOutput()
        elif parametre == "rinçage-Ph":  # fini a tester
            i = 1
            while i < 3:
                print(" rinçage-ph : {0}".format(i))
                self.ser.write("K".encode())
                self.ser.flushOutput()
                time.sleep(timePh)
                self.ser.write("L".encode())
                self.ser.flushOutput()
                time.sleep(0.5)
                self.ser.write("S".encode())
                self.ser.flushOutput()
                time.sleep(timePh)
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
                time.sleep(timeAlc)
                self.ser.write("L".encode())
                self.ser.flushOutput()
                time.sleep(0.5)
                self.ser.write("Q".encode())
                self.ser.flushOutput()
                time.sleep(timeAlc)
                self.ser.write("R".encode())
                self.ser.flushOutput()
                time.sleep(0.5)
                i += 1

            time.sleep(0.5)
            self.ser.write("K".encode())
            self.ser.flushOutput()
            time.sleep(timeAlc)
            self.ser.write("L".encode())
            self.ser.flushOutput()
            time.sleep(timeAlc)
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

    def close(self):
        self.ser.close()

class calc(object):

    def __init__(self,options):
        print("-------------->",options[0].version)
        if options[0].version == 1:
            self.R0 = 21008.0
            self.RL = 1958.5
            self.RH = 7868.4
        elif options[0].version == 2:
            self.R0 = 21004.0
            self.RL = 1958.7
            self.RH = 7867.6
        elif options[0].version == 3:
            self.R0 = 20987.0
            self.Rl = 1960.5
            self.Rh = 7868.2
        elif options[0].version == 4:
            self.R0 = 20996.0
            self.Rl = 1960.6
            self.Rh = 7869.4
        elif options[0].version == "theorique":
            self.R0 = 21000.0
            self.Rl = 1960.0
            self.Rh = 7870.0

            # constantes equation de Steinhart-Hart  ASLEC PH_ALC entre -2 et 32°C :
            self.A = 1.464160e-3
            self.B = 2.389356e-4
            self.C = 0.987137e-7



    def temperature(self, cycle, data):

        #print (data[4:8],data[10:14],data[16:20])

        Data = data[4::].split()
        I1 = int(Data[0])
        I2 = int(Data[1])
        I3 = int(Data[2])
        NH = int(Data[3])
        Nl = int(Data[4])
        NTH =int(Data[5])
        Nth1= 0
        Nl1= 0
      
        if Nl > 4095:
            Nl1 = Nl - 8192

        if NTH > 1000:
            Nth1 = NTH - 8192
        #print 'data:', data

        if NH != 0 and Nl != 0:
            Nh1=NH
            Ks = (float(Nth1) - float(Nl1)) / (float(Nh1) - float(Nl1))
            Bs = self.Rl / (self.Rl + self.R0)
            As = self.R0 * (self.Rh - self.Rl) / ((self.R0 + self.Rl) * (self.R0 + self.Rh))
            Rth = self.R0 *( As * Ks + Bs) / (1 - (As * Ks + Bs))
        else :
            Rth=2252

        Lrth=ln(Rth)
        if cycle =="pH":
            # constantes equation de Steinhart-Hart  ASLEC PH sn 002 (LGE) entre -2 et 32°C :
            self.A3 = 1.465947e-3
            self.B3 = 2.38508e-4
            self.C3 = 1.00287e-7

        else:
        # constantes equation de Steinhart-Hart  ASLEC ALC sn 002 (LGE) entre -2 et 32°C :
            self.A3 = 1.474508e-3
            self.B3 = 2.36749e-4
            self.C3 = 1.10191e-7

        Itk=self.A3+self.B3*Lrth+self.C3*Lrth*Lrth*Lrth
        Tc=1/Itk-273.15
        Rth=int(Rth)
        Tc=round(Tc,2)

        Mesure=("{0} {1} {2} {3} {4} {5} {6} {7}".format(I1, I2, I3, NH,Nl,NTH,Rth,Tc))
        return Mesure


    def calc_ph(self,data):

        print ("mesure du pH")
        return data

    def calc_alc(self,data):

        print ("mesure alcalinité")




        return data

class sauve():

    def __init__(self, date, path):
        if not os.path.isdir(path):
            print ("Création du repertoire "+ path)
            os.mkdir(path)

    def createfile(self, date, path):
        print("fichier de données dans {}".format(path))
        self.file_path_pH = path+"/" +"Moose_GE_02_pH"+ date + ".txt"
        self.file_path_Alc = path+"/" + "Moose_GE_02_Alc"+ date + ".txt"
        print ("fichier de données: \r\n {} \r\n {} \r\n ".format( self.file_path_pH,self.file_path_Alc))
        self.file_save = open(self.file_path_Alc, "a")
        self.file_save = open(self.file_path_pH, "a")

    def sauve_pH(self,data):
        with open(self.file_path_pH, 'a') as f:
            f.write(data+"\r\n")

    def sauve_Alc(self,data):
        with open(self.file_path_Alc, 'a') as f:
            f.write(data+"\r\n")

    def close(self):
        self.file_path_pH.close()
        self.file_path_Alc.close()

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
                      default=3)
    options = parser.parse_args()

    Time0=strftime("%d")
    print(Time0)
    cmd = AcqSerie()
    save = sauve(date,path=out_f )
    save.createfile(date, path=out_f)
    conv=calc(options)
    BUFFERSIZE=1000
    #s = socket(AF_INET, SOCK_DGRAM)
    #s.bind(("", 10006))
    #socket()
    data=""
    expression="NABAT"
    input = 1
    cnt=0
    while True:

        if Time0 != strftime("%d"):#changement de la condition pour changer les fichier de sauvegarde
            
            print("changement des fichiers de sauvegarde pH et Alc")
            Time0=strftime('%d')
            print("nouveau To: "+Time0)
            save.createfile(Time0)
            cnt=0

        cnt +=1
        n = 1
        print("*******************************")
        print("démarrage de la séquence Ph")
        print("*******************************")


        donnees = cmd.read("rinçage-Ph")



        while n < 4:
            #nmea, addr = s.recvfrom(BUFFERSIZE, 0)
            donnees = cmd.read("C")
            data = conv.temperature("pH",donnees)
            Data_to_save = ("{} {} Blanc_pH {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data))

            #Data_to_save = ("{} {} Blanc_pH {} {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data,nmea))
            #Data_to_save = time.strftime('%Y/%m/%d %H:%M:%S ')+cnt + " blanc_pH " + data
            print(Data_to_save)

            save.sauve_pH(Data_to_save)
            n += 1
        n = 1

        while n < 5:
            #nmea, addr = s.recvfrom(BUFFERSIZE, 0)

            print("{0} cycle de micro_com pH".format(n))
            donnees = cmd.read("N")
            data = conv.temperature("pH",donnees)
            Data_to_save = ("{} {} Mesure_pH {}".format(time.strftime('%Y/%m/%d %H:%M:%S '), cnt, data))
            #Data_to_save = ("{} {} Mesure_pH {} {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data,nmea))
            print (Data_to_save)
            save.sauve_pH(Data_to_save)
            time.sleep(0.5)
            donnees = cmd.read("C")
            data = conv.temperature("pH",donnees)
            #Data_to_save = ("{} {} Mesure_pH {} {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data,nmea))
            Data_to_save = ("{} {} Mesure_pH {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data))
            print(Data_to_save)
            save.sauve_pH(Data_to_save)
            time.sleep(0.5)
            donnees = cmd.read("C")
            data = conv.temperature("pH",donnees)
            #Data_to_save = ("{} {} Mesure_pH {} {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data,nmea))
            Data_to_save = ("{} {} Mesure_pH {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data))
            print (Data_to_save)
            save.sauve_pH(Data_to_save)
            time.sleep(0.5)
            n += 1
        donnees = cmd.read("rinçage-Ph")


        """n = 1
        print("*******************************")
        print("démarrage de la séquence Alc")
        print("*******************************")
        donnees = cmd.read("rinçage-alc")

        while n < 4:
            donnees = cmd.read("B")
            data = conv.temperature("Alc",donnees)
            Data_to_save = ("{} {} Blanc_Alc {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data))
            print Data_to_save

            save.sauve_Alc(Data_to_save)
            n += 1
        n = 1

        while n < 2:
            print("{0} cycle de micro_com Alc".format(n))
            donnees = cmd.read("M")
            data = conv.temperature("Alc",donnees)
            Data_to_save = ("{} {} Mesure_Alc {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data))
            print Data_to_save
            save.sauve_Alc(Data_to_save)
            time.sleep(0.5)
            donnees = cmd.read("B")
            data = conv.temperature("Alc",donnees)
            Data_to_save = ("{} {} Mesure_Alc {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data))
            print Data_to_save
            save.sauve_Alc(Data_to_save)
            time.sleep(0.5)
            donnees = cmd.read("B")
            data = conv.temperature("Alc",donnees)
            Data_to_save = ("{} {} Mesure_Alc {}".format(time.strftime('%Y/%m/%d %H:%M:%S '),cnt,data))
            print Data_to_save
            save.sauve_Alc(Data_to_save)
            time.sleep(0.5)
            n += 1
        donnees = cmd.read("rinçage-alc")"""
        t=60


        #changer ici pour le temps de repos
        donnees = cmd.read("K")

        time.sleep(120)
