""" EightPuzzleWithManhattanDistances.py

Partnership? (YES or NO): YES
Student Name 1: Sushma Shankar
Student Name 2: Deveshi Modi

UW NetIDs: sshan854, dmodi
CSE 415, Autumn 2025, University of Washington

This file augments EightPuzzle.py with heuristic information, 
so that it can be used by an A* implementation. 
The particular heuristic finds the total of the Manhattan distances 
for the 8 tiles. 

Usage:
python3 AStar.py EightPuzzleWithManhattanDistances
"""
from EightPuzzle import *

def h(s):
    """We return an estimate of the total Manhattan distance
    between s and the goal state."""

    total_distance = 0
    goal_positions = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1)
    }

    for index, tile in enumerate(s.state):
        if tile != 0:  # Skip the blank tile
            current_row, current_col = divmod(index, 3)
            goal_row, goal_col = goal_positions[tile]
            total_distance += abs(current_row - goal_row) + abs(current_col - goal_col)

    return total_distance