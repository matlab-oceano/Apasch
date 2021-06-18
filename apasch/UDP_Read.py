# -*- coding: utf-8 -*-

import socket

UDP_IP = ""
#UDP_PORT = 12251 # SBE21 TSG
UDP_PORT = 12007 # NMEA

class Udp:
    def __init__(self, PARAM):
        self.PARAM = PARAM
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", PARAM["PORT"]))

    def read_Udp(self):
        try :
            data, addr = self.sock.recvfrom(1024)
            return {self.PARAM["NAME"]:data}
        except:
            print("UDP error")
            return {self.PARAM["NAME"]: 'nan'}
    #print(data.decode('utf8').split(','))



