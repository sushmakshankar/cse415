""" EightPuzzleWithManhattan.py

Partnership? (YES or NO): YES
Student Name 1: Sushma Shankar
Student Name 2: Deveshi Modi
`
UW NetIDs: sshan854, dmodi
CSE 415, Autumn 2025, University of Washington

This file augments EightPuzzle.py with heuristic information, 
so that it can be used by an A* implementation. 
The particular heuristic finds the total of the Manhattan distances 
for the 8 tiles. 

Usage:
python3 AStar.py EightPuzzleWithManhattan
"""
from EightPuzzle import *

def h(s):
    """We return an estimate of the total Manhattan distance
    between s and the goal state."""

    total_distance = 0
    goal_positions = {
        0: (0, 0),  # blank
        1: (0, 1),
        2: (0, 2),
        3: (1, 0),
        4: (1, 1),
        5: (1, 2),
        6: (2, 0),
        7: (2, 1),
        8: (2, 2)
    }

    # Calculate Manhattan distance for each tile
    for i in range(3):
        for j in range(3):
            tile = s.b[i][j]
            # Skip the blank tile (0)
            if tile != 0:
                # Get goal position for this tile
                goal_row, goal_col = goal_positions[tile]
                # Calculate Manhattan distance
                distance = abs(i - goal_row) + abs(j - goal_col)
                total_distance += distance
    
    return total_distance
    