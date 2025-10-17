# EightPuzzleWithLinearConflict.py
# This file augments EightPuzzle.py with a simple misplaced tiles heuristic.
# This heuristic counts misplaced tiles and adds 1 if the blank is not in center.

import EightPuzzle

# Import all necessary components from EightPuzzle
from EightPuzzle import *

def h(s):
    """Simple heuristic: count misplaced tiles + 1 if blank not in center."""
    
    misplaced = 0
    
    # Count misplaced tiles (excluding blank)
    for i in range(3):
        for j in range(3):
            tile = s.b[i][j]
            if tile != 0:  # Skip blank tile
                expected_tile = i * 3 + j + 1  # What tile should be here
                if tile != expected_tile:
                    misplaced += 1
    
    # Add 1 if blank is not in center (position 1,1)
    if s.b[1][1] != 0:
        misplaced += 1
    
    return misplaced
