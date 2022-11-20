# The main file, __init__.py
# This file runs the whole game by calling playGame

# In this directory, we have a file named heroClass.py, a file named monster.py, and a folder named gui which contains the file displayGame.py. We also have a folder named images where all assets are stored.

import heroClass
from monster import *
from gui import displayGame

def playGame():
    # When we import a file normally, we have to reference that file name before
    # the functions/classes in it
    mainPlayer = heroClass.Hero("Fred")

    # When we use from file import *, all the functions/classes from that file
    # get imported directly into our current namespace!
    monsters = spawnMonsters()

    # We can also use from directory import file to organize files nicely
    displayGame.runGame(mainPlayer, monsters)