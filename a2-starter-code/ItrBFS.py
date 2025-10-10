#!/usr/bin/python3
""" ItrBFS.py
Student Names:
UW NetIDs:
CSE 415, Autumn, 2025, University of Washington

This code contains my implementation of the Iterative BFS algorithm.

Usage:
 python ItrBFS.py HumansRobotsFerry
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
        # Comment out the line below when this function is implemented.
        raise NotImplementedError


if __name__ == '__main__':
    if sys.argv == [''] or len(sys.argv) < 2:
        Problem = "TowersOfHanoi"
    else:
        problem_name = sys.argv[1]
        bfs = ItrBFS(problem_name)
        bfs.runBFS()
