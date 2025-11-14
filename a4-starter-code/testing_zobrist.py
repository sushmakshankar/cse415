"""
Test script to measure benefits of move ordering and Zobrist hashing
Run this to generate statistics for your report
"""

import game_types
import sshan854_KInARow as agent_module

def test_move_ordering_benefit():
    """Test the benefit of move ordering on alpha-beta cutoffs"""
    print("\n" + "="*70)
    print("TESTING MOVE ORDERING BENEFIT")
    print("="*70)
    
    # Test state with multiple branches
    test_state = game_types.State(initial_state_data = \
        [[['O','O',' '],
          ['X',' ',' '],
          [' ',' ','X']], "O"])
    
    # Test WITHOUT move ordering
    agent1 = agent_module.OurAgent()
    agent1.prepare(game_types.TTT, 'O', 'Test')
    agent1.use_move_ordering = False
    
    result1 = agent1.make_move(test_state, "", time_limit=10, 
                               use_alpha_beta=True, max_ply=4)
    
    cutoffs_without = agent1.alpha_beta_cutoffs_this_turn
    evals_without = agent1.num_static_evals_this_turn
    
    print(f"\nWITHOUT Move Ordering (depth=4):")
    print(f"  Alpha-beta cutoffs: {cutoffs_without}")
    print(f"  Static evaluations: {evals_without}")
    print(f"  Total nodes examined: {cutoffs_without + evals_without}")
    
    # Test WITH move ordering
    agent2 = agent_module.OurAgent()
    agent2.prepare(game_types.TTT, 'O', 'Test')
    agent2.use_move_ordering = True
    
    result2 = agent2.make_move(test_state, "", time_limit=10,
                               use_alpha_beta=True, max_ply=4)
    
    cutoffs_with = agent2.alpha_beta_cutoffs_this_turn
    evals_with = agent2.num_static_evals_this_turn
    
    print(f"\nWITH Move Ordering (depth=4):")
    print(f"  Alpha-beta cutoffs: {cutoffs_with}")
    print(f"  Static evaluations: {evals_with}")
    print(f"  Total nodes examined: {cutoffs_with + evals_with}")
    
    # Calculate improvement
    nodes_saved = (cutoffs_without + evals_without) - (cutoffs_with + evals_with)
    if nodes_saved > 0:
        percent_improvement = (nodes_saved / (cutoffs_without + evals_without)) * 100
        print(f"\nIMPROVEMENT:")
        print(f"  Nodes saved: {nodes_saved}")
        print(f"  Efficiency gain: {percent_improvement:.1f}%")
        print(f"  Cutoff rate improved by: {cutoffs_with - cutoffs_without} cutoffs")
    else:
        print(f"\nMove ordering didn't improve performance on this particular state")
        print(f"(This can happen with simple positions)")

def test_zobrist_hashing_benefit():
    """Test the benefit of Zobrist hashing"""
    print("\n" + "="*70)
    print("TESTING ZOBRIST HASHING BENEFIT")
    print("="*70)
    
    # Test state
    test_state = game_types.FIAR.initial_state
    
    # Test WITHOUT Zobrist hashing
    agent1 = agent_module.OurAgent()
    agent1.prepare(game_types.FIAR, 'X', 'Test')
    
    result1 = agent1.make_move(test_state, "", time_limit=10,
                               use_alpha_beta=True, 
                               use_zobrist_hashing=False,
                               max_ply=3)
    
    evals_without = agent1.num_static_evals_this_turn
    
    print(f"\nWITHOUT Zobrist Hashing (Five-in-a-Row, depth=3):")
    print(f"  Static evaluations: {evals_without}")
    print(f"  Cache hits: 0 (no caching)")
    
    # Test WITH Zobrist hashing
    agent2 = agent_module.OurAgent()
    agent2.prepare(game_types.FIAR, 'X', 'Test')
    
    result2 = agent2.make_move(test_state, "", time_limit=10,
                               use_alpha_beta=True,
                               use_zobrist_hashing=True,
                               max_ply=3)
    
    evals_with = agent2.num_static_evals_this_turn
    writes = agent2.zobrist_writes
    reads = agent2.zobrist_read_attempts
    hits = agent2.zobrist_successful_reads
    
    print(f"\nWITH Zobrist Hashing (Five-in-a-Row, depth=3):")
    print(f"  Static evaluations: {evals_with}")
    print(f"  Hash table writes: {writes}")
    print(f"  Hash table read attempts: {reads}")
    print(f"  Cache hits: {hits}")
    if reads > 0:
        hit_rate = (hits / reads) * 100
        print(f"  Cache hit rate: {hit_rate:.1f}%")
    
    # Calculate improvement
    if evals_without > evals_with:
        evals_saved = evals_without - evals_with
        percent_improvement = (evals_saved / evals_without) * 100
        print(f"\nIMPROVEMENT:")
        print(f"  Evaluations saved: {evals_saved}")
        print(f"  Efficiency gain: {percent_improvement:.1f}%")
    else:
        print(f"\nNote: First move has limited transpositions")
        print(f"Zobrist hashing shows more benefit in mid-game positions")

def test_combined_features():
    """Test both features together"""
    print("\n" + "="*70)
    print("TESTING COMBINED FEATURES (Move Ordering + Zobrist)")
    print("="*70)
    
    # Mid-game state with transpositions
    test_state = game_types.State(initial_state_data = \
        [[['X','O','X'],
          ['O','X',' '],
          [' ',' ','O']], "X"])
    
    agent = agent_module.OurAgent()
    agent.prepare(game_types.TTT, 'X', 'Test')
    agent.use_move_ordering = True
    
    # Multiple moves to build up cache
    states = [test_state]
    for i in range(3):
        if i < len(states):
            result = agent.make_move(states[i], "", time_limit=10,
                                   use_alpha_beta=True,
                                   use_zobrist_hashing=True,
                                   max_ply=4)
            print(f"\nMove {i+1}:")
            print(f"  Cutoffs: {agent.alpha_beta_cutoffs_this_turn}")
            print(f"  Evaluations: {agent.num_static_evals_this_turn}")
            print(f"  Cache hits: {agent.zobrist_table_num_hits_this_turn}")
            print(f"  Total hash entries: {len(agent.zobrist_table)}")
    
    # Print final statistics
    agent.print_statistics()

if __name__ == "__main__":
    print("\n" + "="*70)
    print("ADVANCED FEATURES TESTING FOR A4 REPORT")
    print("="*70)
    
    test_move_ordering_benefit()
    test_zobrist_hashing_benefit()
    test_combined_features()
    
    print("\n" + "="*70)
    print("TESTING COMPLETE - Use these statistics in your report!")
    print("="*70)