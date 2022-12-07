#################################################
# event.py
#
# Your name: Yee Kit Chan
# Your andrew id: yeekitc
#################################################

import math, os, copy, decimal, datetime
from cmu_112_graphics import *
import module_manager
module_manager.review()

class Event:
    def __init__(self, name):
        self.timezones = {"EST", "PST"}
        self.name = name
        self.possibleDays = []
        self.possibleTimes = []
        self.timeZone = "EST"
        self.usersAvail = dict() # user:availability
        self.usersPriority = []

    def setWeekdays(self, weekdays):
        self.possibleDays = weekdays

    def setDates(self, dates):
        self.possibleDays = dates

    def setTimeZone(self, timeZ):
        if timeZ in self.timezones:
            self.timeZone = timeZ
        else:
            return "Please input a correct timezone."

    def inviteUser(self, user):
        self.users.append(user)

    def inviteUsers(self, users):
        self.users.extend(users)