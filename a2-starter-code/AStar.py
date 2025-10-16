""" AStar.py

A* Search of a problem space.
Partnership? (YES or NO): YES
Student Name 1: Sushma Shankar
Student Name 2: Deveshi Modi

UW NetIDs: sshan854, dmodi
CSE 415, Autumn 2025, University of Washington

This code contains my implementation of the A* Search algorithm.

Usage:
python3 AStar.py FranceWithDXHeuristic
"""

import sys
import importlib
from PriorityQueue import My_Priority_Queue


class AStar:
    """
    Class that implements A* Search for any problem space (provided in the required format)
    """
    def __init__(self, problem):
        """ Initializing the AStar class.
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
        self.h = None  # Heuristic function

        print("\nWelcome to A*.")

    # key differences between UCS and A*:
        # - uniform cost search chooses the minimum cost node on the frontier (its like dijkstras)
        # - a* takes in the minimum of cost+heuristic within the frontier
        #     - heuristic = knowledge or experience, it learns from the past
    def runAStar(self):
        # Comment out the line below when this function is implemented.
        # raise NotImplementedError

        initial_state = self.Problem.CREATE_INITIAL_STATE()
        print("Initial State:")
        print(initial_state)

        self.COUNT = 0
        self.MAX_OPEN_LENGTH = 0
        self.BACKLINKS = {}

        self.AStar(initial_state)
        print(f"Number of states expanded: {self.COUNT}")
        print(f"Maximum length of the open list: {self.MAX_OPEN_LENGTH}")

    def AStar(self, initial_state):
        """A* Search: This is the actual algorithm."""
        self.CLOSED = []
        self.BACKLINKS[initial_state] = None
        # The "Step" comments below help relate A*'s implementation to
        # those of Depth-First Search and Breadth-First Search.

        # STEP 1a. Put the start state on a priority queue called OPEN
        self.OPEN = My_Priority_Queue()
        self.OPEN.insert(initial_state, 0)
        # STEP 1b. Assign g=0 to the start state.
        self.g[initial_state] = 0.0

        while True:
            if len(self.OPEN) == 0:
                print("Failure: No path found")
                return

            if self.VERBOSE:
                print(f"\n{self.COUNT} states expanded so far.")
                print(f"Length of OPEN: {len(self.OPEN)}")

            if len(self.OPEN) > self.MAX_OPEN_LENGTH:
                self.MAX_OPEN_LENGTH = len(self.OPEN)

            # STEP 2. Take the node off OPEN with the lowest f(n)=g(n)+h(n)
            (S, P) = self.OPEN.delete_min()
            self.CLOSED.append(S)
            if S.is_goal():
                if self.VERBOSE:
                    print("\nGoal reached!")
                self.PATH = []
                self.PATH_LENGTH = 0
                self.TOTAL_COST = self.g[n]
                while S is not None:
                    self.PATH.append(n)
                    S = self.BACKLINKS[n]
                    self.PATH_LENGTH += 1
                self.PATH.reverse()
                print("The path to the goal is:")
                for n in self.PATH:
                    print(n)
                print(f"Length of this path: {self.PATH_LENGTH} states")
                print(f"Total cost of this path: {self.TOTAL_COST}")
                print(self.Problem.goal_message(self.PATH[-1]))
                return

            # STEP 3. Add n to CLOSED
            self.CLOSED.append(S)

            # STEP 4. Expand node S, generating each of its successors S'
            for op in self.Problem.OPERATORS:
                if op.is_applicable(S):
                    S_prime = op.apply(S)
                    cost_S_to_Sprime = S.edge_distance(S_prime)
                    if S_prime not in self.g:
                        # This is the first time we've reached S'
                        self.g[S_prime] = float


if __name__ == '__main__':
    if sys.argv == [''] or len(sys.argv) < 2:
        Problem = "FranceWithDXHeuristic"
    else:
        Problem = sys.argv[1]
    aStar = AStar(Problem)
    aStar.runAStar()
