#################################################
# event.py
#
# Your name: Yee Kit Chan
# Your andrew id: yeekitc
#################################################

import math, os, copy, decimal, datetime, random
from cmu_112_graphics import *
from matrix import *
import module_manager
module_manager.review()


# CalendarEvent("Gaming", )

class CalendarEvent:
    def __init__(self, name, timezone="EST", possibleDays=[], possibleTimes=[], usersAvail=dict()):
        self.timezones = {"EST", "PST"}
        self.timezone = timezone
        self.name = name
        self.id = random.randrange(0, 1e10) # never do this
        self.possibleDays = possibleDays
        self.possibleTimes = possibleTimes
        self.usersAvail = usersAvail # {user:(availability, priority)}

    def __repr__(self):
        return f'CalendarEvent(name="{self.name}", timezone="{self.timezone}", possibleDays={self.possibleDays}, possibleTimes={self.possibleTimes}, usersAvail={self.usersAvail})'

    def setWeekdays(self, weekdays):
        self.possibleDays = weekdays

    def setDates(self, dates):
        self.possibleDays = dates

    def setTimeZone(self, timeZ):
        if timeZ in self.timezones:
            self.timeZone = timeZ
        else:
            return "Please input an available timezone."

    def inviteUser(self, user):
        self.users.append(user)

    def inviteUsers(self, users):
        self.users.extend(users)