#################################################
# user.py
#
# Your name: Yee Kit Chan
# Your andrew id: yeekitc
#################################################

import math, os, copy, decimal, datetime
from cmu_112_graphics import *
import module_manager
module_manager.review()

class User:
    def __init__(self, name, username, email, pw):
        self.name = name
        self.username = username
        self.email = email
        self.pw = pw
        
        self.invitedEvents = []
        self.myEvents = []
        self.timeZone = "EST"

    def setTimeZone(self, timeZ):
        self.timeZone = timeZ
