import math, os, copy, decimal, datetime, random
from cmu_112_graphics import *
from button import *
from textBox import *
import module_manager
module_manager.review()

def aCommand():
    print("yess")

newB = Bbutton(1, 2, 3, 4, "5", aCommand)
print(eval(newB.__repr__()) == newB)