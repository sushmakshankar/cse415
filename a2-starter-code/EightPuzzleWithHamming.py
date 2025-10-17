""" EightPuzzleWithHamming.py

Partnership? (YES or NO): YES
Student Name 1: Sushma Shankar
Student Name 2: Deveshi Modi

UW NetIDs: sshan854, dmodi
CSE 415, Autumn 2025, University of Washington

This file augments EightPuzzle.py with heuristic information, 
so that it can be used by an A* implementation. 
The particular heuristic finds the the Hamming Distance, 
or the number of tiles out of place, for the 8 tiles puzzle.

Usage:
python3 AStar.py EightPuzzleWithHamming
"""

from EightPuzzle import *

def h(s):
    """We return an estimate of the Hamming distance"""
    distance = 0
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    for index, tile in enumerate(s.state):
        if tile != 0 and tile != goal_state[index]:  # Skip the blank tile
            distance += 1

    return distance