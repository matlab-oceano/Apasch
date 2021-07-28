# -*- coding: utf-8 -*-

import ntplib
from datetime import datetime

class NTPTime:
    def __init__(self, HOST):
        self.call = ntplib.NTPClient()
        self.HOST = HOST
    def ntpTime(self):
        response = self.call.request(self.HOST, version=2)
        return datetime.utcfromtimestamp(response.orig_time)
