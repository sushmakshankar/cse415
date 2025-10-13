#!/usr/bin/python3
"""
ItrBFS.py
Iterative Breadth-First Search of a problem space.

by Deveshi Modi & Sushma Shankar
Assignment 2, Part A, CSE 415, Autumn 2025

This version is fully Gradescope-compatible.
"""

import sys
import importlib
from collections import deque
import types


class ItrBFS:
    """Iterative Breadth-First Search implementation."""

    def __init__(self, problem_name):
        """
        Dynamically import the problem formulation.
        Handles both string module names and direct module objects.
        """
        # if isinstance(problem_name, str):
        #     # try:
        #     self.Problem = importlib.import_module(problem_name)
        #     # except Exception as e:
        #     #     print("Error importing problem:", e)
        #     #     raise
        # elif isinstance(problem_name, types.ModuleType):
        #     self.Problem = problem_name
        # else:
        #     raise TypeError("Problem must be module name string or module object")

        self.Problem = importlib.import_module(problem_name)
        self.COUNT = None
        self.MAX_OPEN_LENGTH = None
        self.PATH = None
        self.PATH_LENGTH = None
        self.BACKLINKS = None

    def runBFS(self):
        """Run Breadth-First Search."""
        # try:
        #     initial_state = self.Problem.CREATE_INITIAL_STATE()
        # except AttributeError:
        #     if isinstance(self.Problem, str):
        #         self.Problem = importlib.import_module(self.Problem)
        #         initial_state = self.Problem.CREATE_INITIAL_STATE()
        #     else:
        #         raise

        # self.BACKLINKS[initial_state] = None
        # OPEN = deque([initial_state])
        # CLOSED = set()

        initial_state = self.Problem.CREATE_INITIAL_STATE()
        self.COUNT = 0 # new
        self.MAX_OPEN_LENGTH = 0 # new
        self.BACKLINKS = {} # new

        self.iterativeBFS(initial_state) # new
        

            # ---- robust goal test ----
            # Prefer module-level GOAL_TEST if present, otherwise try state.is_goal()
            # if hasattr(self.Problem, "GOAL_TEST") and callable(getattr(self.Problem, "GOAL_TEST")):
            #     is_goal = self.Problem.GOAL_TEST(S)
            # elif hasattr(S, "is_goal") and callable(getattr(S, "is_goal")):
            #     is_goal = S.is_goal()
            # else:
            #     raise AttributeError("No GOAL_TEST found in problem module and state has no is_goal() method.")
            # ---------------------------

            # -------- commented out in recent itr ----------
            # if hasattr(S, "is_goal") and callable(S.is_goal):
            #     is_goal = S.is_goal()
            # elif hasattr(self.Problem, "GOAL_TEST"):
            #     is_goal = self.Problem.GOAL_TEST(S)
            # else:
            #     raise AttributeError("No GOAL_TEST or is_goal() found.")
    
            # if is_goal:
            #     # call goal message function if exists
            #     if hasattr(self.Problem, "GOAL_MESSAGE_FUNCTION") and callable(getattr(self.Problem, "GOAL_MESSAGE_FUNCTION")):
            #         print(self.Problem.GOAL_MESSAGE_FUNCTION(S))
            #     self.PATH = self.backtrace(S)
            #     self.PATH_LENGTH = len(self.PATH) - 1
            #     print("Solution path found:")
            #     for p in self.PATH:
            #         print(p)
            #     print("Length of solution path found:", self.PATH_LENGTH)
            #     print("Number of states expanded:", self.COUNT)
            #     print("Maximum length of open list:", self.MAX_OPEN_LENGTH)
            #     return self.PATH
            # CLOSED.add(S)
            # self.COUNT += 1
            # ---------------------------
            


        # print("No solution found.")
        # return None

    def iterativeBFS(self, initial_state): 
        OPEN = [initial_state] # new
        CLOSED = [] #new
        self.BACKLINKS[initial_state] = None
        # OPEN = deque([initial_state])
        # CLOSED = set()

        while OPEN != []:
            # Track queue size
            report(OPEN, CLOSED, self.COUNT) # new
            if len(OPEN) > self.MAX_OPEN_LENGTH:
                self.MAX_OPEN_LENGTH = len(OPEN)

            S = OPEN.pop(0) # new
            CLOSED.append(S) # new
            # S = OPEN.popleft()

            # new below
            print(f"len(OPEN)= {len(OPEN)}; len(CLOSED)= {len(CLOSED)}; COUNT = {self.COUNT}")
            print("OPEN is now:", [str(s) for s in OPEN])

            if self.Problem.GOAL_TEST(S):
                print(self.Problem.GOAL_MESSAGE_FUNCTION(S))
                self.PATH = [str(state) for state in self.backtrace(S)]
                self.PATH_LENGTH = len(self.PATH) - 1
                print(f"Length of solution path found: {self.PATH_LENGTH} edges")
                return 
            self.COUNT += 1

            L = []
            for op in self.Problem.OPERATORS:
                if op.is_applicable(S):
                    new_state = op.apply(S)
                    if (new_state not in CLOSED) and (new_state not in OPEN):
                        self.BACKLINKS[new_state] = S
                        # OPEN.append(new_state)
            OPEN.extend(L)
            printStateList("OPEN", OPEN)


    def backtrace(self, S):
        """Reconstruct the path from goal back to start."""
        path = []
        while S:
            path.append(S)
            S = self.BACKLINKS[S]
        path.reverse()
        return path
    
    

def printStateList(lst_name, lst):
    """
    Prints the states in lst with name lst_name
    """
    print(f"{lst_name} is now: ", end='')
    for s in lst[:-1]:
        print(str(s), end=', ')
    print(str(lst[-1]))

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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ItrBFS.py ProblemName [OptionalParameter]")
    else:
        problem_name = sys.argv[1]
        bfs = ItrBFS(problem_name)
        bfs.runBFS()
