# -*- coding: utf-8 -*-

import serial
import time



class Interface:

    def __init__(self, serie):
        """
             send dictionary {
             com:char,
             baud:int,
             timeout:int,
             xonxoff:True/False
             rtscts:True/False
             dsrdtr:True/False
             """
        try:
            self.ser = serial.Serial(
                serie["com"],
                serie["baud"],
                timeout=serie["timeout"],
                xonxoff=serie["xonxoff"],
                rtscts=serie["rtscts"],
                dsrdtr=serie["dsrdtr"],
            )
            self.ser.flushInput()
            self.ser.flushOutput()
            print("configuré")
        except IOError:
           print(" Erreur ouverture port serie {} ".format(serie["com"]))

    def cmdsimple(self,cmd):
        try:
            self.ser.write(cmd.encode("utf8"))
            time.sleep(0.5)
        except:
            print("perte serial")

    def send(self, cmd, tr):
        try :
            self.ser.write(cmd.encode("utf8"))
            time.sleep(0.5)
            self.fetch()
            time.sleep(tr)
            return self.fetch()
        except:
             # uniquement pour le test... a mettre en commentaire

            return self.fetch()

    def fetch(self):
        out = ''
        try:
            while self.ser.inWaiting() > 0:
                out += self.ser.read(1).decode()

            if out != '':
                time.sleep(0.5)
                self.ser.flushInput()
                self.ser.flushOutput()
                return out
        except:
            out = "5772 5170 2949 3735 4587 4587"
            #self.ser.flushInput()
            #self.ser.flushOutput()
            return out

    def close(self):
        try:

            self.ser.close()
            return "serial closed"
        except:

            return "Can't close serial link"



