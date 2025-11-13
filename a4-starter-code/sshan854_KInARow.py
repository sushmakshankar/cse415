'''
<yourUWNetID>_KInARow.py
Authors: <your name(s) here, lastname first and partners separated by ";">
  Example:  
    Authors: Smith, Jane; Lee, Laura

An agent for playing "K-in-a-Row with Forbidden Squares" and related games.
CSE 415, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

'''

from agent_base import KAgent
from game_types import State, Game_Type

AUTHORS = 'Sushma Shankar and Deveshi Modi' 
UWNETIDS = ['sshan854', 'dmodi'] # The first UWNetID here should
# match the one in the file name, e.g., janiesmith99_KInARow.py.

import time # You'll probably need this to avoid losing a
 # game due to exceeding a time limit.

# Create your own type of agent by subclassing KAgent:

class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin=twin
        self.nickname = 'Nic'
        if twin: self.nickname += '2'
        self.long_name = 'Templatus Skeletus'
        if twin: self.long_name += ' II'
        self.persona = 'bland'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "don't know yet" # e.g., "X" or "O".
        self.alpha_beta_cutoffs_this_turn = -1
        self.num_static_evals_this_turn = -1
        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1
        self.current_game_type = None
        self.playing_mode = KAgent.DEMO

        # self.opponent_nickname = None
        # self.time_limit = 1.0
        # self.start_time = None

    def introduce(self):
        intro = '\nMy name is Templatus Skeletus.\n'+\
            '"An instructor" made me.\n'+\
            'Somebody please turn me into a real game-playing agent!\n'
        if self.twin: intro += "By the way, I'm the TWIN.\n"
        return intro

    # Receive and acknowledge information about the game from
    # the game master:
    def prepare(
        self,
        game_type,
        what_side_to_play,
        opponent_nickname,
        expected_time_per_move = 0.1, # Time limits can be
                                      # changed mid-game by the game master.

        utterances_matter=True):      # If False, just return 'OK' for each utterance,
                                      # or something simple and quick to compute
                                      # and do not import any LLM or special APIs.
                                      # During the tournament, this will be False..
    #    if utterances_matter:
    #        pass
    #        # Optionally, import your LLM API here.
    #        # Then you can use it to help create utterances.
           
    #    # Write code to save the relevant information in variables
    #    # local to this instance of the agent.
    #    # Game-type info can be in global variables.
    #    print("Change this to return 'OK' when ready to test the method.")
    #    return "Not-OK"

        self.current_game_type = game_type
        self.playing = what_side_to_play
        self.opponent_nickname = opponent_nickname
        self.time_limit = expected_time_per_move
        self.utterances_matter = utterances_matter
        return "OK"
   
    # The core of your agent's ability should be implemented here:             
    def make_move(self, current_state, current_remark, time_limit=1000,
                  use_alpha_beta=True,
                  use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):
        print("make_move has been called")

        self.start_time = time.time()
        self.alpha_beta_cutoffs_this_turn = 0
        self.num_static_evals_this_turn = 0
        
        # Get all legal moves
        legal_moves = self.get_legal_moves(current_state)
        
        if not legal_moves:
            return [[None, current_state], "No legal moves available!"]
        
                # Choose evaluation function
        eval_fn = special_static_eval_fn if special_static_eval_fn else self.static_eval
        
        # Find best move using minimax
        best_move = None
        best_score = float('-inf') if current_state.whose_move == 'X' else float('inf')
        
        for move, new_state in legal_moves:
            # Check time limit
            if time.time() - self.start_time > time_limit * 0.8:
                break
                
            # Evaluate move
            if use_alpha_beta:
                score, _ = self.minimax(new_state, max_ply - 1, True,
                                       float('-inf'), float('inf'), eval_fn)
            else:
                score, _ = self.minimax(new_state, max_ply - 1, False,
                                       None, None, eval_fn)
            
            # Update best move
            if current_state.whose_move == 'X':
                if score > best_score:
                    best_score = score
                    best_move = (move, new_state)
            else:
                if score < best_score:
                    best_score = score
                    best_move = (move, new_state)
        
        if best_move is None:
            best_move = legal_moves[0]
        
        move, new_state = best_move
        
        # Generate utterance
        utterance = self.generate_utterance(best_score)
        
        # Return based on mode
        if self.playing_mode == KAgent.AUTOGRADER:
            stats = [self.alpha_beta_cutoffs_this_turn,
                    self.num_static_evals_this_turn,
                    self.zobrist_table_num_entries_this_turn,
                    self.zobrist_table_num_hits_this_turn]
            return [[move, new_state] + stats, utterance]
        else:
            return [[move, new_state], utterance]
        
        # # Here's a placeholder:
        # a_default_move = (0, 0) # This might be legal ONCE in a game,
        # # if the square is not forbidden or already occupied.
    
        # new_state = current_state # This is not allowed, and even if
        # # it were allowed, the newState should be a deep COPY of the old.
    
        # new_remark = "I need to think of something appropriate.\n" +\
        # "Well, I guess I can say that this move is probably illegal."

        # print("Returning from make_move")
        # return [[a_default_move, new_state], new_remark]

    # The main adversarial search function:
    def minimax(self,
            state,
            depth_remaining,
            pruning=False,
            alpha=None,
            beta=None,
            eval_fn=None):
        print("Calling minimax. We need to implement its body.")

        # Check time limit
        if self.start_time and time.time() - self.start_time > self.time_limit * 0.9:
            return (self.static_eval(state) if eval_fn is None else eval_fn(state), None)
        
        # Base case: depth limit or terminal state
        if depth_remaining == 0 or self.is_terminal(state):
            self.num_static_evals_this_turn += 1
            return (self.static_eval(state) if eval_fn is None else eval_fn(state), None)
        
        legal_moves = self.get_legal_moves(state)
        
        if not legal_moves:
            self.num_static_evals_this_turn += 1
            return (self.static_eval(state) if eval_fn is None else eval_fn(state), None)
        
        # Maximizing player (X)
        if state.whose_move == 'X':
            max_score = float('-inf')
            best_move = None
            
            for move, new_state in legal_moves:
                score, _ = self.minimax(new_state, depth_remaining - 1, pruning,
                                       alpha, beta, eval_fn)
                
                if score > max_score:
                    max_score = score
                    best_move = move
                
                if pruning and alpha is not None:
                    alpha = max(alpha, score)
                    if beta is not None and beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        break
            
            return (max_score, best_move)
        
        # Minimizing player (O)
        else:
            min_score = float('inf')
            best_move = None
            
            for move, new_state in legal_moves:
                score, _ = self.minimax(new_state, depth_remaining - 1, pruning,
                                       alpha, beta, eval_fn)
                
                if score < min_score:
                    min_score = score
                    best_move = move
                
                if pruning and beta is not None:
                    beta = min(beta, score)
                    if alpha is not None and beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        break
            
            return (min_score, best_move)
    
        # return [default_score, "my own optional stuff", "more of my stuff"]
        # Only the score is required here but other stuff can be returned
        # in the list, after the score, in case you want to pass info
        # back from recursive calls that might be used in your utterances,
        # etc. 
 
    def static_eval(self, state, game_type=None):
        print('calling static_eval. Its value needs to be computed!')
        # Values should be higher when the states are better for X,
        # lower when better for O.
        return 0
 
# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances

