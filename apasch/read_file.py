#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 13:54:02 2021

@author: spi-2017-12
"""

import os, glob, json
from datetime import date, timedelta, datetime
import pandas as pd
from netCDF4 import Dataset
import numpy as np
import configparser


class ReadFile:

    def makeList(self, context):
        return glob.glob(context['path']+context['ext'])

    def readFid (self,fid,context):
        """

        :param fid:
        :param context:
        :return:
        """
        df = []
        print("lecture de {} fichier  {}".format(len(fid) , context['ext']))
        if context['ext'] in ['csv', 'txt']:
            for f in fid:
                data = pd.read_table(
                                      context['path']+"/"+f,
                                      header=context['header'],
                                      sep=context['sep'],
                                                     )
                df.append(pd.DataFrame(data))
        elif context['ext'] in  ['ths','gps', 'netcdf','nvi' ]:
            df2=[]
            for f in fid:
                file = context['path']+"/"+f
                nc = Dataset(file,'r')
                index = list(nc.variables)
                data = dict((v, nc.variables[v][:]) for v in context['col'])
                df.append(pd.DataFrame(data))
        return   pd.concat(df, axis=0, ignore_index=False)

    def concat_DT(self, df):
        """
        Concatenate Date time in the array
        :param df:
        :return:
        """
        DATE_TIME =[]
        [DATE_TIME.append(DATE + " " + TIME) for (DATE, TIME) in zip(df['DATE'], df['TIME'])]
        df.insert(0, 'DATE_TIME', DATE_TIME) #incère la colone a la position O
        return df

    def formatDatetime(self, df,context):
        """

        :param df:
        :param context:
        :return:
        """

        df[context['t_name']] = pd.to_datetime(df[context['t_name']])
        return  df

    def time2greg(sel,df,context):
        """
        Transform Date time into gregorian time
        :param df: dataframe
        :param context:  need t_name column and Sart date time to convert (1899, 12, 30)
        :return: dataframe
        """
        START_DATE = datetime(1899, 12, 30)
        df[context['t_name']]= df[context['t_name']].apply(lambda x : (START_DATE+timedelta(x)).strftime('%Y-%m-%d %H:%M:%S'))
        return df

    def popCol (self, df, name):
        df.pop( name )
        return df

