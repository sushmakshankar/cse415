"""
Test script to demonstrate interactive dialog features
This shows examples for your report
"""

import game_types
from game_types import State
import sshan854_KInARow as agent_module

def test_explain_last_move():
    """Test Feature 1: Explain last move statistics"""
    print("\n" + "="*70)
    print("FEATURE 1: 'Tell me how you did that' - Move Explanation")
    print("="*70)
    
    # Create agent
    agent = agent_module.OurAgent()
    agent.prepare(game_types.TTT, 'X', 'TestOpponent')
    
    # Create a mid-game state
    test_state = game_types.State(initial_state_data = \
        [[['O','X',' '],
          ['X','O',' '],
          [' ',' ',' ']], "X"])
    
    print("\nCurrent board state:")
    print(test_state)
    
    # Agent makes a move
    print("Agent is thinking...")
    result = agent.make_move(test_state, "", time_limit=5,
                            use_alpha_beta=True,
                            use_zobrist_hashing=True,
                            max_ply=4)
    
    move, new_state = result[0][:2]
    utterance = result[1]
    
    print(f"\nAgent played: {move}")
    print(f"Agent said: {utterance}")
    
    # Now opponent asks for explanation
    print("\n" + "-"*70)
    print("OPPONENT: Tell me how you did that")
    print("-"*70)
    
    # Agent's next turn with the special phrase
    result2 = agent.make_move(new_state, "Tell me how you did that", 
                             time_limit=5,
                             use_alpha_beta=True,
                             use_zobrist_hashing=True,
                             max_ply=4)
    
    explanation = result2[1]
    print(f"\nBROOKLYN BRAIN: {explanation}")
    
    print("\n" + "="*70)
    print("Copy this exchange into your report as Example 1!")
    print("="*70)

def test_game_analysis():
    """Test Feature 2: Game history analysis"""
    print("\n" + "="*70)
    print("FEATURE 2: 'What's your take on the game so far?' - Game Analysis")
    print("="*70)
    
    # Create agent
    agent = agent_module.OurAgent()
    agent.prepare(game_types.TTT, 'O', 'CompetitivePlayer')
    
    # Simulate a few turns with conversation history
    states = [
        game_types.State(initial_state_data = \
            [[['X',' ',' '],
              [' ',' ',' '],
              [' ',' ',' ']], "O"]),
        
        game_types.State(initial_state_data = \
            [[['X',' ',' '],
              ['O',' ',' '],
              [' ',' ','X']], "O"]),
        
        game_types.State(initial_state_data = \
            [[['X','X',' '],
              ['O','O',' '],
              [' ',' ','X']], "O"])
    ]
    
    remarks = [
        "Let's go!",
        "Nice opening move!",
        "I'm going to win this one!"
    ]
    
    # Play through the turns
    for i, (state, remark) in enumerate(zip(states, remarks)):
        print(f"\n--- Turn {i+1} ---")
        print(f"Opponent says: {remark}")
        result = agent.make_move(state, remark, time_limit=5,
                                use_alpha_beta=True,
                                use_zobrist_hashing=True,
                                max_ply=3)
        move, new_state = result[0][:2]
        utterance = result[1]
        print(f"Brooklyn Brain plays {move} and says: {utterance[:100]}...")
    
    # Now ask for game analysis
    print("\n" + "-"*70)
    print("OPPONENT: What's your take on the game so far?")
    print("-"*70)
    
    # Agent responds with full analysis
    current_state = states[-1]
    result = agent.make_move(current_state, "What's your take on the game so far?",
                            time_limit=5,
                            use_alpha_beta=True,
                            max_ply=3)
    
    analysis = result[1]
    print(f"\nBROOKLYN BRAIN: {analysis}")
    
    print("\n" + "="*70)
    print("Copy this exchange into your report as Example 2!")
    print("="*70)

def test_both_features_in_sequence():
    """Show both features in one game"""
    print("\n" + "="*70)
    print("BONUS: Both Features in One Game")
    print("="*70)
    
    agent = agent_module.OurAgent()
    agent.prepare(game_types.TTT, 'X', 'CuriousPlayer')
    
    # Turn 1
    state1 = game_types.TTT.initial_state
    result1 = agent.make_move(state1, "", use_alpha_beta=True, max_ply=3)
    print(f"\nTurn 1: Brooklyn plays {result1[0][0]}")
    print(f"Says: {result1[1]}")
    
    # Turn 2 - opponent asks for explanation
    state2 = result1[0][1]
    result2 = agent.make_move(state2, "Tell me how you did that", 
                              use_alpha_beta=True, max_ply=3)
    print(f"\nOpponent: 'Tell me how you did that'")
    print(f"Brooklyn explains: {result2[1][:200]}...\n")
    
    # Turn 3 - normal play
    state3 = result2[0][1]
    result3 = agent.make_move(state3, "Interesting!", use_alpha_beta=True, max_ply=3)
    print(f"Turn 3: Brooklyn plays {result3[0][0]}")
    
    # Turn 4 - ask for game analysis
    state4 = result3[0][1]
    result4 = agent.make_move(state4, "What's your take on the game so far?",
                              use_alpha_beta=True, max_ply=3)
    print(f"\nOpponent: 'What's your take on the game so far?'")
    print(f"Brooklyn analyzes: {result4[1][:200]}...\n")
    
    print("="*70)

if __name__ == "__main__":
    print("\n" + "="*70)
    print("INTERACTIVE DIALOG FEATURES - DEMONSTRATION FOR REPORT")
    print("="*70)
    
    test_explain_last_move()
    input("\nPress Enter to continue to Feature 2...")
    
    test_game_analysis()
    input("\nPress Enter to see bonus example...")
    
    test_both_features_in_sequence()
    
    print("\n" + "="*70)
    print("TESTING COMPLETE!")
    print("Use these examples in your A4 report!")
    print("="*70)