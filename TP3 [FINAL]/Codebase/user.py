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

# User class
class User:
    def __init__(self, username, pw, name="", email="", timezone="EST", invitedEvents=[], myEvents=[]):
        self.name = name            # user's name
        self.username = username    # user's username
        self.email = email          # user's email
        self.pw = pw                # user's password
        
        self.invitedEvents = invitedEvents # user's invites
        self.myEvents = myEvents           # user's created events
        self.timeZone = timezone           # user's timezone

    # repr function for the User class
    def __repr__(self):
        return f'User(username={self.username}, pw={self.pw}, name={self.name},\
            email={self.email}, timezone={self.timeZone}, invitedEvents={self.invitedEvents}),\
            myEvents={self.myEvents})'
