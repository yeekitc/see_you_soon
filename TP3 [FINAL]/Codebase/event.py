#################################################
# event.py
#
# Your name: Yee Kit Chan
# Your andrew id: yeekitc
#################################################

import random
from cmu_112_graphics import *
from matrix import *
import module_manager
module_manager.review()

# the CalendarEvent class
class CalendarEvent:
    def __init__(self, name, timezone="EST", possibleDays=[], possibleTimes=[], usersAvail=dict()):
        self.timezones = {"EST", "PST"}
        self.timezone = timezone            # timezone of the event
        self.name = name                    # name of the event
        self.id = random.randrange(0, 1e10) # id of the event
        self.possibleDays = possibleDays    # possible days for the event
        self.possibleTimes = possibleTimes  # possible times for the event
        self.usersAvail = usersAvail # {user:(availability, priority)}

    # repr function for the CalendarEvent class
    def __repr__(self):
        return f'CalendarEvent(name="{self.name}", timezone="{self.timezone}", possibleDays={self.possibleDays}, possibleTimes={self.possibleTimes}, usersAvail={self.usersAvail})'