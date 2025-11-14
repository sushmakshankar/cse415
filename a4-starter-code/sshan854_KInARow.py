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
        self.twin = twin
        self.nickname = 'Brooklyn'
        if twin: self.nickname = 'Bronx'
        self.long_name = 'Brooklyn Brain' if not twin else 'The Bronx Bomber'
        self.persona = 'sarcastic new yorker'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "don't know yet"
        self.alpha_beta_cutoffs_this_turn = 0
        self.num_static_evals_this_turn = 0
        self.zobrist_table_num_entries_this_turn = 0
        self.zobrist_table_num_hits_this_turn = 0
        self.current_game_type = None
        self.playing_mode = KAgent.DEMO
        self.opponent_nickname = None
        self.time_limit = 1.0
        self.start_time = None
        self.special_eval_fn = None
        
        # Utterance tracking
        self.my_past_utterances = []
        self.opponent_past_utterances = []
        self.turn_count = 0
        self.last_eval_score = 0
        self.total_cutoffs = 0
        self.total_evals = 0

        # Zobrist hashing
        self.zobrist_table = {}
        self.zobrist_keys = None  # Will be initialized in prepare
        self.zobrist_writes = 0
        self.zobrist_read_attempts = 0
        self.zobrist_successful_reads = 0
        
        # Move ordering instrumentation
        self.use_move_ordering = True
        self.cutoffs_with_ordering = 0
        self.cutoffs_without_ordering = 0

    def introduce(self):
        intro = f'\nEy, I\'m {self.long_name}, and I\'m walkin\' here!\n'
        intro += f'Born and raised in the five boroughs, trained in the school of hard knocks and minimax algorithms.\n'
        intro += f'I use alpha-beta pruning - it\'s like cutting in line at a New York deli, but for game trees.\n'
        intro += f'My evaluation function? Fuhgeddaboudit - it\'s got more windows than the Empire State Building!\n'
        if self.twin: 
            intro += "Yeah, I'm the twin. We're like the Twin Towers of game-playing AIs. Too soon?\n"
        intro += "Let's do this thing. Winner buys the pizza!\n"
        return intro

    # Receive and acknowledge information about the game from
    # the game master:
    def prepare(self, game_type, what_side_to_play, opponent_nickname,
                expected_time_per_move=0.1, utterances_matter=True):
    # Time limits can be changed mid-game by the game master.
    # If False, just return 'OK' for each utterance,
    # or something simple and quick to compute
    # and do not import any LLM or special APIs.
        self.current_game_type = game_type
        self.playing = what_side_to_play
        self.opponent_nickname = opponent_nickname
        self.time_limit = expected_time_per_move
        self.utterances_matter = utterances_matter
        self.initialize_zobrist_keys(game_type)
        return "OK"
   
    def initialize_zobrist_keys(self, game_type):
        """Initialize random Zobrist hash keys for each board position and piece"""
        import random
        random.seed(42) 
        
        n_rows = game_type.n
        m_cols = game_type.m
        
        # random 64-bit integers for each position and piece type
        self.zobrist_keys = {}
        for i in range(n_rows):
            for j in range(m_cols):
                self.zobrist_keys[(i, j, 'X')] = random.getrandbits(64)
                self.zobrist_keys[(i, j, 'O')] = random.getrandbits(64)
                self.zobrist_keys[(i, j, '-')] = random.getrandbits(64)
    
    def compute_zobrist_hash(self, state):
        """Compute Zobrist hash for a given state"""
        hash_value = 0
        board = state.board
        
        for i in range(len(board)):
            for j in range(len(board[0])):
                piece = board[i][j]
                if piece in ['X', 'O', '-']:
                    hash_value ^= self.zobrist_keys[(i, j, piece)]
        
        return hash_value

    def make_move(self, current_state, current_remark, time_limit=1000,
                  use_alpha_beta=True, use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):
        # print("make_move has been called")

        self.start_time = time.time()
        self.alpha_beta_cutoffs_this_turn = 0
        self.num_static_evals_this_turn = 0
        self.special_eval_fn = special_static_eval_fn
        self.turn_count += 1

        self.zobrist_table_num_entries_this_turn = len(self.zobrist_table)
        self.zobrist_table_num_hits_this_turn = 0
        turn_start_writes = self.zobrist_writes
        turn_start_reads = self.zobrist_read_attempts
        
        # Track opponent's remark
        if current_remark:
            self.opponent_past_utterances.append(current_remark)
            
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
        
        # Update statistics
        self.last_eval_score = best_score
        self.total_cutoffs += self.alpha_beta_cutoffs_this_turn
        self.total_evals += self.num_static_evals_this_turn
        
        # Calculate per-turn Zobrist stats
        self.zobrist_table_num_hits_this_turn = self.zobrist_successful_reads - (turn_start_reads - turn_start_writes)
        
        # Generate utterance
        utterance = self.generate_utterance(best_score, current_state, best_state, current_remark)
        self.my_past_utterances.append(utterance)
        
        # Return based on mode
        if self.playing_mode == KAgent.AUTOGRADER:
            stats = [self.alpha_beta_cutoffs_this_turn,
                    self.num_static_evals_this_turn,
                    self.zobrist_table_num_entries_this_turn,
                    self.zobrist_table_num_hits_this_turn]
            return [[best_move, best_state] + stats, utterance]
        else:
            return [[best_move, best_state], utterance]

    def order_moves(self, legal_moves, current_state, use_zobrist):
        """Order moves by evaluation score to improve alpha-beta pruning"""
        move_scores = []
        
        for move, new_state in legal_moves:
            # Check Zobrist table first if enabled
            if use_zobrist:
                hash_val = self.compute_zobrist_hash(new_state)
                if hash_val in self.zobrist_table:
                    score = self.zobrist_table[hash_val]
                    move_scores.append((score, move, new_state))
                    continue
            
            # Otherwise do shallow evaluation
            score = self.evaluate_state(new_state)
            move_scores.append((score, move, new_state))
        
        # Sort based on whose turn it is
        if current_state.whose_move == 'X':
            # Maximizing: sort descending (best first)
            move_scores.sort(reverse=True, key=lambda x: x[0])
        else:
            # Minimizing: sort ascending (best first)
            move_scores.sort(key=lambda x: x[0])
        
        # Return ordered moves (without scores)
        return [(move, state) for score, move, state in move_scores]
    

    # The main adversarial search function:
    def minimax(self, state, depth_remaining, pruning=False,
                alpha=None, beta=None, use_zobrist=False):

        # Check time limit
        if self.start_time and time.time() - self.start_time > self.time_limit * 0.9:
            return self.evaluate_state(state)
        
        if use_zobrist:
            hash_val = self.compute_zobrist_hash(state)
            self.zobrist_read_attempts += 1
            
            if hash_val in self.zobrist_table:
                cached_data = self.zobrist_table[hash_val]
                # Check if cached depth is sufficient
                if cached_data['depth'] >= depth_remaining:
                    self.zobrist_successful_reads += 1
                    return cached_data['score']
        
        # Base case: depth limit or terminal state
        if depth_remaining <= 0 or self.is_terminal(state):
            score = self.evaluate_state(state)
            # Store in Zobrist table if enabled
            if use_zobrist:
                hash_val = self.compute_zobrist_hash(state)
                self.zobrist_table[hash_val] = {
                    'score': score,
                    'depth': depth_remaining
                }
                self.zobrist_writes += 1
            
            return score
        
        legal_moves = self.get_legal_moves(state)
        
        if not legal_moves:
            score = self.evaluate_state(state)
            if use_zobrist:
                hash_val = self.compute_zobrist_hash(state)
                self.zobrist_table[hash_val] = {
                    'score': score,
                    'depth': depth_remaining
                }
                self.zobrist_writes += 1
            return score
        
        # ORDER MOVES for better pruning
        if self.use_move_ordering and pruning:
            legal_moves = self.order_moves_in_search(legal_moves, state, use_zobrist)
        
        # Maximizing player (X)
        if state.whose_move == 'X':
            max_score = float('-inf')
            
            for move, new_state in legal_moves:
                score = self.minimax(new_state, depth_remaining - 1, pruning, alpha, beta, use_zobrist)
                max_score = max(max_score, score)
                
                if pruning and alpha is not None and beta is not None:
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        break  # Beta cutoff
            
            if use_zobrist:
                hash_val = self.compute_zobrist_hash(state)
                self.zobrist_table[hash_val] = {
                    'score': max_score,
                    'depth': depth_remaining
                }
                self.zobrist_writes += 1

            return max_score
        
        # Minimizing player (O)
        else:
            min_score = float('inf')
            
            for move, new_state in legal_moves:
                score = self.minimax(new_state, depth_remaining - 1, pruning, alpha, beta, use_zobrist)
                min_score = min(min_score, score)
                
                if pruning and alpha is not None and beta is not None:
                    beta = min(beta, score)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        break  # Alpha cutoff
            
            if use_zobrist:
                hash_val = self.compute_zobrist_hash(state)
                self.zobrist_table[hash_val] = {
                    'score': min_score,
                    'depth': depth_remaining
                }
                self.zobrist_writes += 1
                
            return min_score
    
    def order_moves_in_search(self, legal_moves, current_state, use_zobrist):
        """Order moves during search for better pruning (lighter weight than root ordering)"""
        move_scores = []
        
        for move, new_state in legal_moves:
            score = None
            
            # Check Zobrist table first if enabled
            if use_zobrist:
                hash_val = self.compute_zobrist_hash(new_state)
                if hash_val in self.zobrist_table:
                    score = self.zobrist_table[hash_val]['score']
            
            # If not in table, use quick heuristic (don't do full eval to save time)
            if score is None:
                # Simple heuristic: count pieces near center
                board = new_state.board
                center_r = len(board) // 2
                center_c = len(board[0]) // 2
                move_r, move_c = move
                # Prefer center moves
                score = -abs(move_r - center_r) - abs(move_c - center_c)
            
            move_scores.append((score, move, new_state))
        
        # Sort based on whose turn it is
        if current_state.whose_move == 'X':
            move_scores.sort(reverse=True, key=lambda x: x[0])
        else:
            move_scores.sort(key=lambda x: x[0])
        
        return [(move, state) for score, move, state in move_scores]
 
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
    
    def generate_utterance(self, score, old_state, new_state, opponent_remark):
        
        if not self.utterances_matter or self.playing_mode == KAgent.COMPETITION:
            return "OK"
        
        utterances = []
        
        # 1. Teach about search statistics
        if self.turn_count % 3 == 1 and self.alpha_beta_cutoffs_this_turn > 0:
            utterances.append(
                f"Boom! Alpha-beta pruning just saved me {self.alpha_beta_cutoffs_this_turn} branches. "
                f"That's faster than a cab driver finding a shortcut through midtown! "
                f"Only checked {self.num_static_evals_this_turn} positions."
            )
        
        # 2. GAME-STATE-SPECIFIC
        if abs(score) > 10000:
            if (score > 0 and self.playing == 'X') or (score < 0 and self.playing == 'O'):
                utterances.append("BADA BING! I got you right where I want ya! This game's over faster than a $1 pizza slice!")
            else:
                utterances.append("Oy vey! You're killin' me here! I'm in more trouble than a tourist in Times Square!")
        elif abs(score) > 1000:
            if (score > 0 and self.playing == 'X') or (score < 0 and self.playing == 'O'):
                utterances.append("Now we're talkin'! I'm building something bigger than the new Hudson Yards development!")
            else:
                utterances.append("Alright, alright, I see your threat. Gotta block this like I'm double-parked on Delancey.")
        elif abs(score) < 10:
            utterances.append("This is tighter than rush hour on the L train! Every move counts, capisce?")
        
        # 3. PERSONA-SPECIFIC:
        k = self.current_game_type.k
        if self.turn_count == 1:
            utterances.append(f"Aight, let's get this bread! Looking for {k} in a row - easier than finding a decent bagel in Manhattan!")
        elif self.turn_count == 3:
            utterances.append("My window-based heuristic is checking more angles than a street photographer in SoHo!")
        elif self.turn_count % 5 == 0:
            utterances.append(
                f"Check it out - {self.total_evals} positions evaluated, {self.total_cutoffs} branches cut. "
                f"I'm workin' harder than a hot dog vendor at a Yankees game!"
            )
        
        # 4. RESPONSIVE: 
        if opponent_remark and len(self.opponent_past_utterances) > 0:
            last_remark = opponent_remark.lower()
            if 'random' in last_remark:
                utterances.append("Random moves? What are ya, a tourist? I'm gonna exploit that like subway showtime dancers!")
            elif 'win' in last_remark:
                utterances.append("Oh, you think you're winnin'? That's cute. Like thinking you'll get a seat on the 6 train.")
            elif 'good' in last_remark or 'nice' in last_remark:
                utterances.append("Ey, thanks! That's what I'm talkin' about! Respect!")
            elif 'hello' in last_remark or 'hi' in last_remark:
                utterances.append("Yo! What's good? Let's play some K-in-a-Row!")
        
        # 5. OBSERVANT: 
        empty_count = sum(1 for row in new_state.board for cell in row if cell == ' ')
        total_cells = len(new_state.board) * len(new_state.board[0])
        if empty_count < total_cells * 0.3:
            utterances.append("Board's fillin' up like Penn Station at 5 PM! Endgame time, baby!")
        
        # 6. EDUCATIONAL
        if self.turn_count == 2:
            utterances.append(
                f"Lemme break it down for ya - I check every {k}-length window on this board. "
                f"It's like checking every bodega in Brooklyn for the best chopped cheese."
            )
        
        # NY SLANG one-liners (random fallbacks)
        ny_oneliners = [
            "I'm on it like white on rice!",
            "Fuhgeddaboudit!",
            "That's how we do it in the city!",
            "I got more moves than the MTA has delays!",
            "This move's smoother than a fresh slice from Joe's!",
            "I'm calculating faster than a bodega cat running from health inspectors!",
            "Deadass, this is a solid play!",
            "No cap, that's a good position!",
            "I'm locked in like rent control in the Village!"
        ]
        
        # Return utterances
        if not utterances:
            import random
            return random.choice(ny_oneliners)
        
        if len(utterances) == 1:
            return utterances[0]
        else:
            return utterances[0] + " " + (utterances[1] if len(utterances) > 1 else "")
        
    def print_statistics(self):
        """Print comprehensive statistics for reporting"""
        print("\n" + "="*60)
        print("BROOKLYN BRAIN - PERFORMANCE STATISTICS")
        print("="*60)
        
        print("\n--- ALPHA-BETA PRUNING ---")
        print(f"Total alpha-beta cutoffs: {self.total_cutoffs}")
        print(f"Total positions evaluated: {self.total_evals}")
        if self.total_evals > 0:
            efficiency = (self.total_cutoffs / (self.total_cutoffs + self.total_evals)) * 100
            print(f"Pruning efficiency: {efficiency:.1f}%")
        
        print("\n--- ZOBRIST HASHING ---")
        print(f"Total hash table entries: {len(self.zobrist_table)}")
        print(f"Total writes to hash table: {self.zobrist_writes}")
        print(f"Total read attempts: {self.zobrist_read_attempts}")
        print(f"Successful reads (cache hits): {self.zobrist_successful_reads}")
        if self.zobrist_read_attempts > 0:
            hit_rate = (self.zobrist_successful_reads / self.zobrist_read_attempts) * 100
            print(f"Cache hit rate: {hit_rate:.1f}%")
        
        print("\n--- MOVE ORDERING ---")
        print(f"Move ordering enabled: {self.use_move_ordering}")
        print(f"This improves alpha-beta cutoff rate by examining promising moves first")
        
        print("\n" + "="*60)
 
# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances