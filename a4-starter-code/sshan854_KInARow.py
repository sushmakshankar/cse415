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
        intro = '\nMy name is {self.long_name}.\n'+\
            '"I was created by {AUTHORS[0]}.\n'+\
            'I use minimax with alpha-beta pruning to make strategic moves!\n'
            # 'Somebody please turn me into a real game-playing agent!\n'+\
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
        # print("make_move has been called")

        self.start_time = time.time()
        self.alpha_beta_cutoffs_this_turn = 0
        self.num_static_evals_this_turn = 0
        self.special_eval_fn = special_static_eval_fn
        
        # Get all legal moves
        legal_moves = self.get_legal_moves(current_state)
        
        if not legal_moves:
            return [[None, current_state], "No legal moves available!"]
        
        best_move = None
        best_state = None

        if current_state.whose_move == 'X':
            # Maximizing at root
            best_score = float('-inf')
            alpha = float('-inf')
            beta = float('inf')
            
            for move, new_state in legal_moves:
                if time.time() - self.start_time > time_limit * 0.8:
                    break
                
                score = self.minimax(new_state, max_ply - 1, 
                                    pruning=use_alpha_beta,
                                    alpha=alpha, 
                                    beta=beta)
                
                if score > best_score:
                    best_score = score
                    best_move = move
                    best_state = new_state
                
                if use_alpha_beta:
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        break
        else:
            # Minimizing at root
            best_score = float('inf')
            alpha = float('-inf')
            beta = float('inf')
            
            for move, new_state in legal_moves:
                if time.time() - self.start_time > time_limit * 0.8:
                    break
                
                score = self.minimax(new_state, max_ply - 1, 
                                    pruning=use_alpha_beta,
                                    alpha=alpha, 
                                    beta=beta)
                
                if score < best_score:
                    best_score = score
                    best_move = move
                    best_state = new_state
                
                if use_alpha_beta:
                    beta = min(beta, score)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        break
        
        if best_move is None:
            best_move, best_state = legal_moves[0]
        
        # Generate utterance
        utterance = self.generate_utterance(best_score)
        
        # Return based on mode
        if self.playing_mode == KAgent.AUTOGRADER:
            stats = [self.alpha_beta_cutoffs_this_turn,
                    self.num_static_evals_this_turn,
                    self.zobrist_table_num_entries_this_turn,
                    self.zobrist_table_num_hits_this_turn]
            return [[best_move, best_state] + stats, utterance]
        else:
            return [[best_move, best_state], utterance]
        
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
            beta=None):
            # eval_fn=None):

        # Check time limit
        if self.start_time and time.time() - self.start_time > self.time_limit * 0.9:
            # return (self.static_eval(state) if eval_fn is None else eval_fn(state), None)
            return self.evaluate_state(state)
        
        # Base case: depth limit or terminal state
        if depth_remaining <= 0 or self.is_terminal(state):
            # self.num_static_evals_this_turn += 1
            # return (self.static_eval(state) if eval_fn is None else eval_fn(state), None)
            return self.evaluate_state(state)
        
        legal_moves = self.get_legal_moves(state)
        
        if not legal_moves:
            # self.num_static_evals_this_turn += 1
            # return (self.static_eval(state) if eval_fn is None else eval_fn(state), None)
            return self.evaluate_state(state)
        
        # Maximizing player (X)
        if state.whose_move == 'X':
            max_score = float('-inf')
            # best_move = None
            
            for move, new_state in legal_moves:
                score = self.minimax(new_state, depth_remaining - 1, pruning, alpha, beta)
                max_score = max(max_score, score)
                
                if pruning and alpha is not None and beta is not None:
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        break  # Beta cutoff
            
            return max_score
        
        # Minimizing player (O)
        else:
            min_score = float('inf')
            # best_move = None
            
            for move, new_state in legal_moves:
                score = self.minimax(new_state, depth_remaining - 1, pruning, alpha, beta)
                min_score = min(min_score, score)
                
                if pruning and alpha is not None and beta is not None:
                    beta = min(beta, score)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        break  # Alpha cutoff
            
            return min_score
    
        # return [default_score, "my own optional stuff", "more of my stuff"]
        # Only the score is required here but other stuff can be returned
        # in the list, after the score, in case you want to pass info
        # back from recursive calls that might be used in your utterances,
        # etc. 
 
    def evaluate_state(self, state):
        """Wrapper for evaluation - uses special function if provided"""
        self.num_static_evals_this_turn += 1
        if self.special_eval_fn:
            return self.special_eval_fn(state)
        else:
            return self.static_eval(state)
        
    '''
An agent for playing "K-in-a-Row with Forbidden Squares" and related games.
CSE 415, University of Washington
'''

from agent_base import KAgent
from game_types import State, Game_Type
import time

AUTHORS = 'Your Name Here'
UWNETIDS = ['yournetid']

class OurAgent(KAgent):
    
    def __init__(self, twin=False):
        self.twin = twin
        self.nickname = 'StratBot'
        if twin: self.nickname += '2'
        self.long_name = 'Strategic Bot'
        if twin: self.long_name += ' II'
        self.persona = 'strategic'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "don't know yet"
        self.alpha_beta_cutoffs_this_turn = 0
        self.num_static_evals_this_turn = 0
        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1
        self.current_game_type = None
        self.playing_mode = KAgent.DEMO
        self.opponent_nickname = None
        self.time_limit = 1.0
        self.start_time = None
        self.special_eval_fn = None
        
    def introduce(self):
        intro = f'\nMy name is {self.long_name}.\n'
        intro += f'Created by {AUTHORS[0]}.\n'
        intro += 'I use minimax with alpha-beta pruning to make strategic moves!\n'
        if self.twin: 
            intro += "I'm the twin version!\n"
        return intro
    
    def prepare(self, game_type, what_side_to_play, opponent_nickname,
                expected_time_per_move=0.1, utterances_matter=True):
        """Store game information"""
        self.current_game_type = game_type
        self.playing = what_side_to_play
        self.opponent_nickname = opponent_nickname
        self.time_limit = expected_time_per_move
        self.utterances_matter = utterances_matter
        return "OK"
    
    def make_move(self, current_state, current_remark, time_limit=1000,
                  use_alpha_beta=True, use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):
        """Main entry point for making a move"""
        self.start_time = time.time()
        self.alpha_beta_cutoffs_this_turn = 0
        self.num_static_evals_this_turn = 0
        self.special_eval_fn = special_static_eval_fn
        
        # Get all legal moves (in order for autograder compatibility)
        legal_moves = self.get_legal_moves(current_state)
        
        if not legal_moves:
            return [[None, current_state], "No legal moves available!"]
        
        # Find best move using minimax with alpha-beta at the root level
        best_move = None
        best_state = None
        
        if current_state.whose_move == 'X':
            # Maximizing at root
            best_score = float('-inf')
            alpha = float('-inf')
            beta = float('inf')
            
            for move, new_state in legal_moves:
                if time.time() - self.start_time > time_limit * 0.8:
                    break
                
                score = self.minimax(new_state, max_ply - 1, 
                                    pruning=use_alpha_beta,
                                    alpha=alpha, 
                                    beta=beta)
                
                if score > best_score:
                    best_score = score
                    best_move = move
                    best_state = new_state
                
                if use_alpha_beta:
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        break
        else:
            # Minimizing at root
            best_score = float('inf')
            alpha = float('-inf')
            beta = float('inf')
            
            for move, new_state in legal_moves:
                if time.time() - self.start_time > time_limit * 0.8:
                    break
                
                score = self.minimax(new_state, max_ply - 1, 
                                    pruning=use_alpha_beta,
                                    alpha=alpha, 
                                    beta=beta)
                
                if score < best_score:
                    best_score = score
                    best_move = move
                    best_state = new_state
                
                if use_alpha_beta:
                    beta = min(beta, score)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        break
        
        if best_move is None:
            best_move, best_state = legal_moves[0]
        
        # Generate utterance
        utterance = self.generate_utterance(best_score)
        
        # Return based on mode
        if self.playing_mode == KAgent.AUTOGRADER:
            stats = [self.alpha_beta_cutoffs_this_turn,
                    self.num_static_evals_this_turn,
                    self.zobrist_table_num_entries_this_turn,
                    self.zobrist_table_num_hits_this_turn]
            return [[best_move, best_state] + stats, utterance]
        else:
            return [[best_move, best_state], utterance]
    
    def minimax(self, state, depth_remaining, pruning=False,
                alpha=None, beta=None):
        """Minimax algorithm with optional alpha-beta pruning"""
        
        # Check time limit
        if self.start_time and time.time() - self.start_time > self.time_limit * 0.9:
            return self.evaluate_state(state)
        
        # Base case: depth limit or terminal state
        if depth_remaining <= 0 or self.is_terminal(state):
            return self.evaluate_state(state)
        
        # Get legal moves
        legal_moves = self.get_legal_moves(state)
        
        if not legal_moves:
            return self.evaluate_state(state)
        
        # Maximizing player (X)
        if state.whose_move == 'X':
            max_score = float('-inf')
            
            for move, new_state in legal_moves:
                score = self.minimax(new_state, depth_remaining - 1, pruning, alpha, beta)
                max_score = max(max_score, score)
                
                # Alpha-beta pruning for maximizer
                if pruning and alpha is not None and beta is not None:
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        break  # Beta cutoff
            
            return max_score
        
        # Minimizing player (O)
        else:
            min_score = float('inf')
            
            for move, new_state in legal_moves:
                score = self.minimax(new_state, depth_remaining - 1, pruning, alpha, beta)
                min_score = min(min_score, score)
                
                # Alpha-beta pruning for minimizer
                if pruning and alpha is not None and beta is not None:
                    beta = min(beta, score)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        break  # Alpha cutoff
            
            return min_score
    
    def evaluate_state(self, state):
        """Wrapper for evaluation - uses special function if provided"""
        self.num_static_evals_this_turn += 1
        if self.special_eval_fn:
            return self.special_eval_fn(state)
        else:
            return self.static_eval(state)
    
    def static_eval(self, state, game_type=None):
        """Evaluate the desirability of a state - WINDOW-BASED APPROACH"""
        
        if game_type is None:
            game_type = self.current_game_type
        
        k = game_type.k
        board = state.board
        n_rows = len(board)
        m_cols = len(board[0])
        
        score = 0
        
        # Check all possible k-length windows in all directions
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for i in range(n_rows):
            for j in range(m_cols):
                for d_row, d_col in directions:
                    # Check if we can fit a k-length window starting here
                    end_row = i + (k - 1) * d_row
                    end_col = j + (k - 1) * d_col
                    
                    if not (0 <= end_row < n_rows and 0 <= end_col < m_cols):
                        continue
                    
                    # Count pieces in this window
                    x_count = 0
                    o_count = 0
                    empty_count = 0
                    blocked = False
                    
                    for step in range(k):
                        r = i + step * d_row
                        c = j + step * d_col
                        cell = board[r][c]
                        
                        if cell == 'X':
                            x_count += 1
                        elif cell == 'O':
                            o_count += 1
                        elif cell == ' ':
                            empty_count += 1
                        else:  # forbidden square '-'
                            blocked = True
                            break
                    
                    if blocked:
                        continue
                    
                    # If window has both X and O, it's useless
                    if x_count > 0 and o_count > 0:
                        continue
                    
                    # Score for X
                    if x_count > 0 and o_count == 0:
                        score += self.score_window(x_count, empty_count, k)
                    
                    # Score for O (negative)
                    if o_count > 0 and x_count == 0:
                        score -= self.score_window(o_count, empty_count, k)
        
        return score
    
    
    def score_window(self, piece_count, empty_count, k):
        """Score a window based on how many pieces it has"""
        if piece_count == k:
            return 100000  # Win
        elif piece_count == k - 1 and empty_count == 1:
            return 1000  # One move from win
        elif piece_count == k - 2 and empty_count == 2:
            return 100  # Two moves from win
        elif piece_count == k - 3 and empty_count == 3:
            return 10  # Three moves from win
        else:
            return piece_count  # Some progress
    
    def get_legal_moves(self, state):
        """Generate all legal moves from current state IN ORDER"""
        moves = []
        board = state.board
        n_rows = len(board)
        m_cols = len(board[0])
        
        for i in range(n_rows):
            for j in range(m_cols):
                if board[i][j] == ' ':
                    new_state = State(old=state)
                    new_state.board[i][j] = state.whose_move
                    new_state.change_turn()
                    moves.append(((i, j), new_state))
        
        return moves
    
    def is_terminal(self, state):
        """Check if state is terminal (no more moves)"""
        board = state.board
        for row in board:
            if ' ' in row:
                return False
        return True
    
    def generate_utterance(self, score):
        """Generate a contextual utterance based on the game state"""
        if not self.utterances_matter:
            return "OK"
        
        if abs(score) > 1000:
            return "This looks like a winning position!"
        elif abs(score) > 100:
            return "I'm feeling confident about this move."
        elif abs(score) > 10:
            return "A solid strategic choice."
        else:
            return "Let's see how this plays out."
 
# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances