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

#<METADATA> 
PROBLEM_NAME = "Farmer, Fox, Chicken, and Grain"
PROBLEM_VERSION = "1.1"
PROBLEM_AUTHORS = ['S. Shankar, D. Modi']
PROBLEM_CREATION_DATE = "10-OCT-2025"

PROBLEM_DESC=\
    '''The <b>"Farmer, Fox, Chicken, and Grain"</b> problem is a classic river-crossing puzzle.
    The player starts off with one of each of the four items on the left bank of a river. The objective is to
    transfer all items to the right bank of the river using a boat that can carry only the farmer and one item at a time.
    The challenge is to ensure that the fox is never left alone with the chicken (as the fox would eat the chicken),
    and the chicken is never left alone with the grain (as the chicken would eat the grain) when the farmer is not present.
    The computer will not allow any move that would result in an unsafe situation, and it will only show moves that can be executed safely.
    '''
#</METADATA>

# Start your Common Code section here.

#<COMMON_CODE>
# this below represents the location of the boat
LEFT=1
RIGHT=0

class State():

    def __init__(self, old=None):
        # old = an existing state to copy from
        # if there is no old state, the default state is that everything is on the left side
        if old is None:
            self.farmer_location = LEFT
            self.fox_location = LEFT
            self.chicken_location = LEFT
            self.grain_location = LEFT
            self.boat = LEFT
        else:
            self.farmer_location = old.farmer_location
            self.fox_location = old.fox_location
            self.chicken_location = old.chicken_location
            self.grain_location = old.grain_location
            self.boat = old.boat

    def __eq__(self, s2):
        if self.farmer_location != s2.farmer_location: return False
        if self.fox_location != s2.fox_location: return False
        if self.chicken_location != s2.chicken_location: return False
        if self.grain_location != s2.grain_location: return False
        if self.boat != s2.boat: return False
        return True
    
    def __str__(self):
        # Produces a textual description of a state.
        txt = "\n Farmer location:"+str(self.farmer_location)+"\n"
        txt += " Fox location:"+str(self.fox_location)+"\n"
        txt += " Chicken location:"+str(self.chicken_location)+"\n"
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
        '''Tests whether it's legal to move the ferry and take the
         item (fox, chicken, grain) with the farmer.'''
        side = self.boat
        # boat can only have 3 items max
        # fox cannot be with chicken alone
        # chicken cannot be left alone with grain
        # solution: 
        # 1) chicken/farmer to R, farmer comes back alone
        # 2) farmer/grain to R, farmer/chicken come back
        # 3) farmer/fox to R, farmer comes back alone
        # 4) farmer/chicken to R

        # farmer must be on the boat
        if self.farmer_location != side:
            return False
        
        # check if item is on the same side as the boat
        if item != 'farmer':
            if item == 'fox' and self.fox_location != side:
                return False
            if item == 'chicken' and self.chicken_location != side:
                return False
            if item == 'grain' and self.grain_location != side:
                return False

        new_side = 1 - side
        # simulate the move
        new_farmer_location = new_side  

        if item == 'fox':
            new_chicken_location = self.chicken_location
            new_fox_location = new_side
            new_grain_location = self.grain_location
        elif item == 'chicken':
            new_chicken_location = new_side
            new_fox_location = self.fox_location
            new_grain_location = self.grain_location
        elif item == 'grain':
            new_chicken_location = self.chicken_location
            new_fox_location = self.fox_location
            new_grain_location = new_side
        else:  # item is farmer only
            new_chicken_location = self.chicken_location
            new_fox_location = self.fox_location
            new_grain_location = self.grain_location
        
        # check if chicken is with the fox
        if new_fox_location == new_chicken_location and new_farmer_location != new_chicken_location:
            return False
        
        # check if chicken is with the grain
        if new_chicken_location == new_grain_location and new_farmer_location != new_chicken_location:
            return False
        
        return True
    
    def move(self, item):
        '''Assuming it's legal to make the move, this computes
       the new state resulting from moving the item with the farmer.'''
        news = self.copy() 
        new_side = 1 - self.boat
        news.farmer_location = new_side

        if item == 'fox':
            news.fox_location = new_side
        elif item == 'chicken':
            news.chicken_location = new_side
        elif item == 'grain':
            news.grain_location = new_side
        # move the boat
        news.boat = new_side
        return news
    
    def is_goal(self):
        '''If everything is on the right side, then s is a goal state.'''
        return (self.farmer_location == RIGHT and 
                self.fox_location == RIGHT and 
                self.chicken_location == RIGHT and 
                self.grain_location == RIGHT)

class Operator:
    def __init__(self, item):
        self.item = item
        if item == 'farmer':
            self.name = "Farmer crosses alone"
        else:
            self.name = "Farmer takes " + item + "across"
    
    def is_applicable(self, s):
        return s.can_move(self.item)
    
    def apply(self, s):
        return s.move(self.item)
    
    def __str__(self):
        # if self.item == 'farmer':
        #     return "Farmer crosses alone"
        # else:
        #     return "Farmer takes " + self.item + "across"
        return self.name

#</COMMON_CODE>

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State() 
#</INITIAL_STATE>

# Put your OPERATORS section here.
#<OPERATORS>
ITEMS = ['farmer', 'fox', 'chicken', 'grain']
OPERATORS = [Operator(item) for item in ITEMS]
#</OPERATORS>

# etc.


# Finish off with the GOAL_TEST and GOAL_MESSAGE_FUNCTION here.
#<GOAL_TEST>
# GOAL_TEST = lambda s: (s.farmer_location == RIGHT and 
#                        s.fox_location == RIGHT and
#                        s.chicken_location == RIGHT and 
#                        s.grain_location == RIGHT)
GOAL_TEST = lambda s: s.is_goal()
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: "Congratulations! The farmer has successfully transported the fox, chicken, and grain across the river!"
#</GOAL_MESSAGE_FUNCTION>

