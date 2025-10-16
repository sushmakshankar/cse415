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

        while len(self.OPEN) > 0:
            # print("Failure: No path found")
            # return
            if self.VERBOSE:
                # print(f"\n{self.COUNT} states expanded so far.")
                # print(f"Length of OPEN: {len(self.OPEN)}")
                report(self.OPEN, self.CLOSED, self.COUNT)
            if len(self.OPEN) > self.MAX_OPEN_LENGTH:
                self.MAX_OPEN_LENGTH = len(self.OPEN)

            # STEP 2. Take the node off OPEN with the lowest f(n)=g(n)+h(n)
            (S, P) = self.OPEN.delete_min()
            self.CLOSED.append(S)


            if S.is_goal():
                print(self.Problem.GOAL_MESSAGE_FUNCTION(S))
                self.PATH = [str(state) for state in self.backtrace(S)]
                self.PATH_LENGTH = len(self.PATH) - 1
                print(f'Length of solution path found: {self.PATH_LENGTH} edges')
                self.TOTAL_COST = self.g[S]
                print(f'Total cost of solution path found: {self.TOTAL_COST}')
                return
            self.COUNT += 1

            # STEP 3. Add n to CLOSED
            self.CLOSED.append(S)

            # STEP 4. Expand node S, generating each of its successors S'
            gs = self.g[S]  # Save the cost of getting to S in a variable.
            for op in self.Problem.OPERATORS:
                if op.is_applicable(S):
                    S_prime = op.apply(S)
                    if S_prime in self.CLOSED:
                        # print("Already have this state, in CLOSED. del ...")
                        del S_prime
                        continue
                    cost_S_to_Sprime = S.edge_distance(S_prime)
                    new_g = gs + cost_S_to_Sprime

                    if S_prime in self.OPEN:
                        # print("new_state is in OPEN already, so...")
                        P = self.OPEN[S_prime]
                        if new_g < P:
                            # print("New priority value is lower, so del older one")
                            del self.OPEN[S_prime]
                            self.OPEN.insert(S_prime, new_g)
                        else:
                            # print("Older one is better, so del new_state")
                            del S_prime
                            continue
                    else:
                        # print("new_state was not on OPEN at all, so just put it on.")
                        self.OPEN.insert(S_prime, new_g)
                    self.BACKLINKS[S_prime] = S
                    self.g[S_prime] = new_g
        
        return None
    def backtrace(self, S):
        path = []
        while S:
            path.append(S)
            S = self.BACKLINKS[S]
        path.reverse()
        print("Solution path: ")
        for s in path:
            print(s)
        return path


def report(opn, closed, count):
    """
    Reports the current statistics:
    Length of open list
    Length of closed list
    Number of states expanded
    """
    print(f"len(OPEN)= {len(opn)}", end='; ')
    print(f"len(CLOSED)= {len(closed)}", end='; ')
    print(f"COUNT = {count}")
    
if __name__ == '__main__':
    if sys.argv == [''] or len(sys.argv) < 2:
        Problem = "FranceWithDXHeuristic"
    else:
        Problem = sys.argv[1]
    aStar = AStar(Problem)
    aStar.runAStar()
