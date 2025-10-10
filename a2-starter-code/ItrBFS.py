#!/usr/bin/python3
""" ItrBFS.py
Student Names: Sushma Shankar, Deveshi Modi
UW NetIDs: sshan854, dmodi
CSE 415, Autumn, 2025, University of Washington

This code contains my implementation of the Iterative BFS algorithm.

Usage:
 python ItrBFS.py HumansRobotsFerry
"""

import sys
import importlib


class ItrBFS:
    """
    Class that implements Iterative BFS for any problem space (provided in the required format)
    """

    def __init__(self, problem):
        """ Initializing the ItrBFS class.
        Please DO NOT modify this method. You may populate the required instance variables
        in the other methods you implement.
        """
        self.Problem = importlib.import_module(problem)
        self.COUNT = None  # Number of nodes expanded
        self.MAX_OPEN_LENGTH = None  # Maximum length of the open list
        self.PATH = None  # Solution path
        self.PATH_LENGTH = None  # Length of the solution path
        self.BACKLINKS = None  # Predecessor links, used to recover the path
        print("\nWelcome to ItrBFS")

    def runBFS(self):
        # Comment out the line below when this function is implemented.
        # raise NotImplementedError
        """This is an encapsulation of some setup before running
        BFS, plus running it and then printing some stats."""
        initial_state = self.Problem.CREATE_INITIAL_STATE()
        print("Initial State:")
        print(initial_state)

        self.COUNT = 0
        self.MAX_OPEN_LENGTH = 0
        self.BACKLINKS = {}

        self.IterativeBFS(initial_state)
        print(f"Number of states expanded: {self.COUNT}")
        print(f"Maximum length of the open list: {self.MAX_OPEN_LENGTH}")

    def IterativeBFS(self, initial_state):
        """This is the actual algorithm"""
        #Step 1: start by putting the start state on a list OPEN
        OPEN = [initial_state]
        CLOSED = []
        self.BACKLINKS[initial_state] = None

        #Step 2: If OPEN is empty, output "DONE" and stop.
        while OPEN != []:
            report(OPEN, CLOSED, self.COUNT)
            if len(OPEN) > self.MAX_OPEN_LENGTH:
                self.MAX_OPEN_LENGTH = len(OPEN)

            #Step 3: Select the first state on OPEN and call it S.
            S = OPEN.pop(0)
            CLOSED.append(S)

            if S.is_goal():
                try:
                    print(self.Problem.GOAL_MESSAGE_FUNCTION(S))
                except:
                    print(self.Problem.goal_message(S))

                self.PATH = [str(state) for state in self.backtrace(S)]
                self.PATH_LENGTH = len(self.PATH) - 1
                print(f"Length of solution path found: {self.PATH_LENGTH} edges")
                return
            self.COUNT += 1

            #Step 4: Generate the list L of states reachable from S by one legal operator.
            L = []
            for op in self.Problem.OPERATORS:
                if op.is_applicable(S):
                    new_state = op.apply(S)
                    # check if state is alr in OPEN
                    if not (new_state in CLOSED):
                        if not (new_state in OPEN):
                            L.append(new_state)
                            self.BACKLINKS[new_state] = S
            
            # Step 5: add L to OPEN and append all members of L to the end of open
            OPEN = L + OPEN
            print_state_list("OPEN", OPEN)
            
            #Step 5: Delete from L those states already appearing on CLOSED or OPEN.
                    
        


if __name__ == '__main__':
    if sys.argv == [''] or len(sys.argv) < 2:
        Problem = "TowersOfHanoi"
    else:
        Problem = sys.argv[1]
    BFS = ItrBFS(Problem)
    BFS.runBFS()
