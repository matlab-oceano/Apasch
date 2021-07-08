# -*- coding: utf-8 -*-

import os
import yaml

class ConfParse:
    file = os.path.join(os.getcwd(), "conf.yml")


    print("Fichier lu {}".format(file))
    config = yaml.safe_load(open("conf.yml", 'r'))


    def __init__(self):
        self.config.read(self.file)


    def read(self, key, value):
        return self.config.get(key, value)

    def write(self, key, value):
        self.config.write(key, value)

    def getItem(self, section):
        return dict(self.config.items(section))

if __name__ == '__main__':

    Conf = ConfParse()