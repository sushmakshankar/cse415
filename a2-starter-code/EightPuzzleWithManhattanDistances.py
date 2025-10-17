""" EightPuzzleWithManhattanDistances.py

The total of the Manhattan distances for the 8 tiles puzzle.
Partnership? (YES or NO): YES
Student Name 1: Sushma Shankar
Student Name 2: Deveshi Modi

UW NetIDs: sshan854, dmodi
CSE 415, Autumn 2025, University of Washington

This code contains our implementation to find the total of the 
Manhattan distances for the 8 tiles.

Usage:
python3 AStar.py EightPuzzleWithManhattanDistances
"""

import sys
import importlib
from PriorityQueue import My_Priority_Queue

class EightPuzzleWithManhattanDistances:
    """
    Class that implements the Manhattan distance heuristic for the 8 tiles puzzle.
    """

    def __init__(self, problem):
        """ Initializing the ManhattanDistances class.
        Please DO NOT modify this method. You may populate the required instance variables
        in the other methods you implement.
        """
        self.Problem = importlib.import_module(problem)
        self.COUNT = None  # Number of nodes expanded.
        self.MAX_OPEN_LENGTH = None  # How long OPEN ever gets.
        self.PATH = None  # List of states from initial to goal, along lowest-cost path.
        self.PATH_LENGTH = None  # Number of states from initial to goal, along lowest-cost path.
        self.TOTAL_COST = None  # Sum of edge costs along the lowest-cost path.
        self.BACKLINKS = {}  # Predecessor links, used to recover the path.
        self.OPEN = None  # OPEN list
        self.CLOSED = None  # CLOSED list
        self.VERBOSE = True  # Set to True to see progress; but it slows the search.

        # The value g(s) represents the cost along the best path found so far
        # from the initial state to state s.
        self.g = {}  # We will use a hash table to associate g values with states.
        self.h = self.Problem.h  # Heuristic function

        print("\nWelcome to Manhattan Distance")