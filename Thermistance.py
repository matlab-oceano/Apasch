# -*- coding: utf-8 -*-

import os

class CalcThermistance:
    
    def __init__(self, *args, **kwargs):
        version, path =  kwargs.get('version', 'path')
        print(version +'\r\n'+ path)
    def thermistance(self, value):
        pass
if __name__ == "__main__":
    calc = CalcThermistance(version=1, path = os.getcwd)