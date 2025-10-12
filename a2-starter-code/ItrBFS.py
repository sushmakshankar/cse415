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
        if isinstance(problem_name, str):
            try:
                self.Problem = importlib.import_module(problem_name)
            except Exception as e:
                print("Error importing problem:", e)
                raise
        elif isinstance(problem_name, types.ModuleType):
            self.Problem = problem_name
        else:
            raise TypeError("Problem must be module name string or module object")

        self.COUNT = 0
        self.MAX_OPEN_LENGTH = 0
        self.PATH = []
        self.PATH_LENGTH = 0
        self.BACKLINKS = {}

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
        self.BACKLINKS[initial_state] = None
        OPEN = deque([initial_state])
        CLOSED = set()

        while OPEN:
            # Track queue size
            if len(OPEN) > self.MAX_OPEN_LENGTH:
                self.MAX_OPEN_LENGTH = len(OPEN)

            S = OPEN.popleft()

            # ---- robust goal test ----
            # Prefer module-level GOAL_TEST if present, otherwise try state.is_goal()
            # if hasattr(self.Problem, "GOAL_TEST") and callable(getattr(self.Problem, "GOAL_TEST")):
            #     is_goal = self.Problem.GOAL_TEST(S)
            # elif hasattr(S, "is_goal") and callable(getattr(S, "is_goal")):
            #     is_goal = S.is_goal()
            # else:
            #     raise AttributeError("No GOAL_TEST found in problem module and state has no is_goal() method.")
            # ---------------------------
            if hasattr(S, "is_goal") and callable(S.is_goal):
                is_goal = S.is_goal()
            elif hasattr(self.Problem, "GOAL_TEST"):
                is_goal = self.Problem.GOAL_TEST(S)
            else:
                raise AttributeError("No GOAL_TEST or is_goal() found.")
    
            if is_goal:
                # call goal message function if exists
                if hasattr(self.Problem, "GOAL_MESSAGE_FUNCTION") and callable(getattr(self.Problem, "GOAL_MESSAGE_FUNCTION")):
                    print(self.Problem.GOAL_MESSAGE_FUNCTION(S))
                self.PATH = self.backtrace(S)
                self.PATH_LENGTH = len(self.PATH) - 1
                print("Solution path found:")
                for p in self.PATH:
                    print(p)
                print("Length of solution path found:", self.PATH_LENGTH)
                print("Number of states expanded:", self.COUNT)
                print("Maximum length of open list:", self.MAX_OPEN_LENGTH)
                return self.PATH

            CLOSED.add(S)
            self.COUNT += 1

            for op in self.Problem.OPERATORS:
                if op.is_applicable(S):
                    new_state = op.apply(S)
                    if new_state not in CLOSED and new_state not in OPEN:
                        self.BACKLINKS[new_state] = S
                        OPEN.append(new_state)

        print("No solution found.")
        return None


    def backtrace(self, S):
        """Reconstruct the path from goal back to start."""
        path = []
        while S is not None:
            path.append(S)
            S = self.BACKLINKS[S]
        path.reverse()
        return path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ItrBFS.py ProblemName [OptionalParameter]")
    else:
        problem_name = sys.argv[1]
        bfs = ItrBFS(problem_name)
        bfs.runBFS()
