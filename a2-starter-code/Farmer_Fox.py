'''Farmer_Fox.py
by Sushma Shankar and Deveshi Modi
UWNetIDs: sshan854, dmodi
Student numbers: 2001840, 2239898

Assignment 2, in CSE 415, Autumn 2025
 
This file contains my problem formulation for the problem of4
the Farmer, Fox, Chicken, and Grain.
'''

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name(s), uwnetid(s), and 7-digit student number(s) are given above in 
# the format shown.

# You should model your code closely after the given example problem
# formulation in HumansRobotsFerry.py

# Put your metadata here, in the same format as in HumansRobotsFerry.

#</METADATA>
PROBLEM_NAME = "Farmer, Fox, Chicken, and Grain"
PROBLEM_VERSION = "1.1"
PROBLEM_AUTHORS = ['S. Shankar, D. Modi']
PROBLEM_CREATION_DATE = "10-OCT-2025"


# Start your Common Code section here.

#<COMMON_CODE>
# change this potentially? what is common code
Farmer_location = 1
Chicken_location = 1
Fox_location = 1
Grain_location = 1
# this below represents the location of the boat
LEFT=1
RIGHT=0

class State():

    def __init__(self, old=None):
        # old = an existing state to copy from
        # if there is no old state, the default state is that everything is on the left side
        if old is None:
            self.farmer_location = LEFT
            self.chicken_location = LEFT
            self.fox_location = LEFT
            self.grain_location = LEFT
            self.boat = LEFT
        else:
            self.farmer = old.farmer_location
            self.chicken = old.chicken_location
            self.fox = old.fox_location
            self.grain = old.grain_location
            self.boat = old.boat

    def __eq__(self, s2):
        if self.farmer_location != s2.farmer_location: return False
        if self.chicken_location != s2.chicken_location: return False
        if self.fox_location != s2.fox_location: return False
        if self.grain_location != s2.grain_location: return False
        if self.boat != s2.boat: return False
        return True
    
    def __str__(self):
        # Produces a textual description of a state.
        txt = "\n Farmer location:"+str(self.farmer_location)+"\n"
        txt += " Chicken location:"+str(self.chicken_location)+"\n"
        txt += " Fox location:"+str(self.fox_location)+"\n"
        txt += " Grain location:"+str(self.grain_location)+"\n"
        if self.boat == LEFT:
            txt += " Boat location: LEFT\n"
        else:
            txt += " Boat location: RIGHT\n"
        return txt
    
    def __hash__(self):
        return (self.__str__()).__hash__()
    
    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        return State(old=self)
    
    def can_move(self, item):
        '''Tests whether it's legal to move the ferry and take
         item (farmer, chicken, fox, grain).'''
        side = self.boat
        # NEED TO IMPLEMENT THIS
        # boat can only have 3 items max
        # fox cannot be with chicken alone
        # chicken cannot be left alone with grain
        # solution: 1) chicken/farmer to R, farmer comes back alone
        # 2) farmer/grain to R, farmer/chicken come back
        # 3) farmer/fox to R, farmer comes back alone
        # 4) farmer/chicken to R


# Put your INITIAL STATE section here.
#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State() #directly from hrf
#</INITIAL_STATE>

# Put your OPERATORS section here.
#<OPERATORS>
HR_combinations = [(1,0),(2,0),(3,0),(1,1),(2,1)] #directly from hrf

class Operator:
    pass

# etc.


# Finish off with the GOAL_TEST and GOAL_MESSAGE_FUNCTION here.

