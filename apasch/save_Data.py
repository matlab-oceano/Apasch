# -*- coding: utf-8 -*-

import csv
from time import strftime
import os



class Save:

    def __init__(self, PARAM, type, name):
        os.getcwd()
        self.HEADER = PARAM['HEADER']
        self.FILENAME = PARAM['FID']
        self.FILEFREQ = "%"+ PARAM['Change_file']
        self.type=type
        if type == 'RAW':
            self.FILEPATH= PARAM['FID']+"data"
            self.create('RAW_',name)
        elif type == 'LOG':
            self.FILEPATH= PARAM['FID']+"log"
            self.create('AVG_',name)

    def create(self, type, name):
        self.timestart = strftime(self.FILEFREQ)
        self.FID = "{}_{}_{}_{}_{}".format(type,self.FILENAME,name,strftime('%m%d-%Y_%H%M%S'),".csv")
        print(self.FILEPATH,type,self.FILENAME,strftime('%m%d-%Y_%H%M%S'),".csv")
        with open(self.FID, 'a') as self.csvfile:
            self.fieldnames = self.HEADER
            writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)

            writer.writeheader()

    def write(self, data):
        with open(self.FID, 'a') as self.csvfile:
            self.fieldnames = self.HEADER
            writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
            writer.writerow(data)
        self.newFile()

    def close(self):
        pass

    def newFile(self):
        if self.timestart != strftime(self.FILEFREQ):
            self.create(self.type)
