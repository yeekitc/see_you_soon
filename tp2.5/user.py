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
    def __init__(self, username, pw, name="", email="", timezone="EST", invitedEvents=[], myEvents=[]):
        self.name = name
        self.username = username
        self.email = email
        self.pw = pw
        
        self.invitedEvents = invitedEvents
        self.myEvents = myEvents
        self.timeZone = timezone

    def __repr__(self):
        return f'User(username={self.username}, pw={self.pw}, name={self.name},\
            email={self.email}, timezone={self.timeZone}, invitedEvents={self.invitedEvents}),\
            myEvents={self.myEvents})'

    def setTimeZone(self, timeZ):
        self.timeZone = timeZ

    def setEmail(self, email):
        self.email = email
