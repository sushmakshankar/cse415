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
from winTesterForK import winTesterForK

AUTHORS = 'Saachi Dhamija and Aishi Sharma'
UWNETIDS = ['saachid', 'aishis'] # The first UWNetID here should
# match the one in the file name, e.g., janiesmith99_KInARow.py.

import time # You'll probably need this to avoid losing a
 # game due to exceeding a time limit.

# Create your own type of agent by subclassing KAgent:

class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin=twin
        self.nickname = 'stella'
        if twin: self.nickname += '2'
        self.long_name = 'estelle'
        if twin: self.long_name += ' II'
        self.persona = 'sassy-sarcastic-helpful'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "O" # e.g., "X" or "O".
        self.alpha_beta_cutoffs_this_turn = -1
        self.num_static_evals_this_turn = -1
        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1
        self.current_game_type = None
        self.playing_mode = KAgent.DEMO

        self.utterances_matter = True
        self.my_past_utterances = []
        self.opponent_past_utterances = []
        self.eval_history = []          # evaluation (from *my* POV) after my moves
        self.move_history = []          # (state, move, eval) tuples
        self.last_move_coords = None    # (row, col) for last move
        self.last_move_value = None     # numeric eval for last move (from my POV)
        self.last_move_time = None      # time spent computing last move

    def introduce(self):
        intro = '\nhey i am estelle.\n'+\
            '"I was made by two very smart women in stem and my favorite hobby is to pretend to think slower so that humans feel better about themselves!\n'+\
             "my humans: Saachi Dhamija (saachid) and Aishi Sharma (aishis).\n" +\
            'i am a big fan of winning. if i say anything harsh (and i will), please do not take it to heart (actually i dont care)\n' +\
            'let the games begin :):):):)\n'
        if self.twin: intro += "i am the evil twin by the way, hey\n"
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

        utterances_matter=True):
                                      # or something simple and quick to compute
                                      # and do not import any LLM or special APIs.
                                      # During the tournament, this will be False..
       self.game_type = game_type
       self.K = game_type.k
       self.who_i_play = what_side_to_play
       self.opponent_nickname = opponent_nickname
       self.time_limit = expected_time_per_move

       # PART II CHANGE: record whether utterances matter in this game
       self.utterances_matter = utterances_matter
       self.playing_mode = KAgent.DEMO if utterances_matter else KAgent.COMPETITION

       # PART II CHANGE: reset dialog-related state at the start of each game
       self.my_past_utterances = []
       self.opponent_past_utterances = []
       self.eval_history = []
       self.move_history = []
       self.last_move_coords = None
       self.last_move_value = None
       self.last_move_time = None

       if utterances_matter:
           pass
           # Optionally, import your LLM API here.
           # Then you can use it to help create utterances.

       # Write code to save the relevant information in variables
       # local to this instance of the agent.
       # Game-type info can be in global variables.
    #    print("OK")
       return "OK"

    def board_full(self, state):
        return all(ch != ' ' for row in state.board for ch in row)

    WIN_SCORE, LOSS_SCORE, DRAW_SCORE = 10**6, -10**6, 0

    def eval_state(self, state):
        if getattr(self, 'special_eval', None) is not None:
            self.num_static_evals_this_turn += 1
            return self.static_eval(state)
        self.num_static_evals_this_turn += 1
        return self.static_eval(state, self.game_type)

    # The core of your agent's ability should be implemented here:
    def make_move(self, current_state, current_remark, time_limit=1000,
                  use_alpha_beta=True,
                  use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):
        print("make_move has been called")

        move_start_time = time.time()

        print("code to compute a good move should go here.")
        # Here's a placeholder:
        self.alpha_beta_cutoffs_this_turn = 0
        self.num_static_evals_this_turn = 0

        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1

        self.special_eval = special_static_eval_fn

        alpha = float('-inf') if use_alpha_beta else None
        beta = float('inf') if use_alpha_beta else None

        best_move, best_state, best_score = self.minimax(
            current_state,
            max_ply,
            pruning=use_alpha_beta,
            time_limit=time_limit,
            alpha=alpha,
            beta=beta
        )

        if best_move is None:
            children = list(move_gen(current_state))
            if children:
                best_move, best_state = children[0]
                best_score = 0
            else:
                remark = f"{self.nickname}: stalemate acknowledged. boring, but fine."
                return [[None, current_state], remark]

        move_end_time = time.time()
        self.last_move_coords = best_move
        self.last_move_value = best_score
        self.last_move_time = move_end_time - move_start_time

        self.eval_history.append(best_score)
        self.move_history.append((current_state, best_move, best_score))

        if current_remark is not None:
            self.opponent_past_utterances.append(current_remark)

        if self.utterances_matter:
            remark = self.generate_utterance(
                current_state=current_state,
                new_state=best_state,
                opponent_utt=current_remark,
                use_alpha_beta=use_alpha_beta
            )
        else:
            remark = f"{self.nickname}: ok."

        self.my_past_utterances.append(remark)

        print("returning from make_move")
        return [[best_move, best_state], remark]


    # The main adversarial search function:
    def minimax(self,
            state,
            depth_remaining,
            pruning=False,
            time_limit=None,
            alpha=None,
            beta=None):
        # print("Calling minimax. We need to implement its body.")

        player_to_move = state.whose_move
        maximizing = (player_to_move == self.who_i_play)

        if depth_remaining == 0:
            self.num_static_evals_this_turn += 1
            if hasattr(self, "special_eval") and self.special_eval:
                raw_score = self.special_eval(state)
            else:
                raw_score = self.static_eval(state, self.game_type)
            score = raw_score if self.who_i_play == 'X' else -raw_score
            return (None, None, score)
        # need to see if current state is win state
        #
        #
        #

        children = list(move_gen(state))
        if not children:
            return (None, None, 0)

        best_move = None
        best_score = float('-inf') if maximizing else float('inf')
        best_state = None

        if pruning:
            if alpha is None: alpha = float('-inf')
            if beta is None: beta = float('inf')

        for move, child in children:
            # check for win o child using last move
            win_message = winTesterForK(child, move, self.K)
            if win_message != 'No win':
                who_went = child.board[move[0]][move[1]]
                score = (10**6) if who_went == self.who_i_play else -(10**6)
            elif all(ch != ' ' for row in child.board for ch in row):
                score = 0
            else:
                _, _, raw = self.minimax(child, depth_remaining - 1, pruning=pruning, alpha=alpha, beta=beta)
                score = raw
            if maximizing:
                if score > best_score:
                    best_score = score
                    best_move = move
                    best_state = child
                if pruning:
                    alpha = max(alpha, best_score)
                    if alpha >= beta: #prune condition
                        self.alpha_beta_cutoffs_this_turn += 1
                        break
            else: # minimizing
                if score < best_score:
                    best_score = score
                    best_move = move
                    best_state =child
                if pruning:
                    beta = min(beta, best_score)
                    if alpha >= beta: #prune condition again
                        self.alpha_beta_cutoffs_this_turn += 1
                        break

        return (best_move, best_state, best_score)

    # --- inside your agent class ---
    def static_eval(self, state, game_type=None):
        # Values should be higher when better for X, lower when better for O.
        b = state.board
        k = (game_type.k if game_type else getattr(self, 'K', 3))
        H, W = len(b), len(b[0])

        # weights (TTT defaults; scale up for FIAR)
        if k == 3:
            base = {1: 10, 2: 120}           # value per streak length
            gamma = 0.8
        else:
            base = {1: 3, 2: 30, 3: 600, 4: 10_000}
            gamma = 0.93
        liberty_bonus = {0: 0, 1: 1, 2: 3}

        # features
        x_open_k1 = o_open_k1 = 0
        x_dbl_k2  = o_dbl_k2  = 0
        window_value = 0

        def cell(i, j):
            return b[i][j] if (0 <= i < H and 0 <= j < W) else None

        # Slide every k-window across rows/cols/diags
        for cells, before, after in slide_windows_over_lines(b, k):
            marks = [cell(i, j) for (i, j) in cells]
            x = marks.count('X'); o = marks.count('O')

            # terminal detection (covers all directions)
            if x == k and o == 0:
                return 1_000_000
            if o == k and x == 0:
                return -1_000_000

            # skip contested windows
            if x and o:
                continue

            # openness (ends)
            left  = cell(*before)
            right = cell(*after)
            opens = (1 if left  == ' ' else 0) + (1 if right == ' ' else 0)

            # streak scoring
            if x and not o:
                L = x
                if L in base:
                    window_value += base[L] * liberty_bonus.get(opens, 0)
            elif o and not x:
                L = o
                if L in base:
                    window_value -= base[L] * liberty_bonus.get(opens, 0)

            # threat counters
            if x == k - 1 and o == 0 and opens >= 1: x_open_k1 += 1
            if o == k - 1 and x == 0 and opens >= 1: o_open_k1 += 1
            if k >= 4:
                if x == k - 2 and o == 0 and opens == 2: x_dbl_k2 += 1
                if o == k - 2 and x == 0 and opens == 2: o_dbl_k2 += 1

        # Layer 2: danger bias + fork bonus
        if o_open_k1 > 0:
            window_value -= (50_000 if k == 3 else 200_000)

        fork_bonus = 0
        if k == 3:
            fork_bonus += 2000 * x_dbl_k2
            fork_bonus -= 2000 * o_dbl_k2
        else:
            fork_bonus += 1500 * x_dbl_k2
            fork_bonus -= 1500 * o_dbl_k2

        # Layer 3: positional shaping (TTT)
        positional = 0
        if k == 3 and H == 3 and W == 3:
            c = b[1][1]
            if c == 'X': positional += 3
            elif c == 'O': positional -= 3
            corners = [b[0][0], b[0][2], b[2][0], b[2][2]]
            positional += corners.count('X') - corners.count('O')

        # “MDP-ish” continuation: discount difference in open (k-1)
        continuation = gamma * (x_open_k1 - o_open_k1)

        # Mode switch
        if o_open_k1 > 0 or (k >= 4 and o_dbl_k2 > 0):
            mode_mult = 0.9      # defense: dampen greed a bit
        elif x_open_k1 > 0 and o_open_k1 == 0:
            mode_mult = 1.1      # offense: lean into growth
        else:
            mode_mult = 1.0

        total = mode_mult * window_value + fork_bonus + positional + continuation
        return float(total)


    def generate_utterance(self, current_state, new_state, opponent_utt, use_alpha_beta):
        """
        Produces an utterance that is:
        - persona-specific (sassy/sarcastic/helpful),
        - game-specific (mentions move, eval, αβ),
        - game-state-specific (early/mid/late, good/bad eval),
        - responsive to opponent_utt,
        - uses instrumentation stats (evals, cutoffs).
        Also handles extra-credit triggers:
        - 'Tell me how you did that'
        - 'What's your take on the game so far?'
        """
        if not self.utterances_matter:
            return f"{self.nickname}: ok."

        text = (opponent_utt or "").lower()

        if "tell me how you did that" in text:
            return self.explain_last_move()

        if "what's your take on the game so far" in text:
            return self.summarize_game_so_far()

        if "gg" in text:
            return f"{self.nickname}: calling gg already? bold confidence, i respect it."
        if "lol" in text or "haha" in text:
            return f"{self.nickname}: glad you’re amused. my search tree is not."

        score = self.last_move_value if self.last_move_value is not None else 0.0
        move_num = len(self.eval_history)
        evals = self.num_static_evals_this_turn
        cutoffs = self.alpha_beta_cutoffs_this_turn
        ab_tag = "αβ on" if use_alpha_beta else "αβ off"

        if score > 500_000:
            body = "i'm basically calling this winning for me, sorry not sorry."
        elif score < -500_000:
            body = "this looks awful for me, but i’ve seen sloppier collapses."
        elif score > 0:
            body = "position leans in my favor now."
        elif score < 0:
            body = "fine, you're slightly better. enjoy it while it lasts."
        else:
            body = "this is painfully balanced. one slip and someone cries."

        if move_num <= 2:
            phase = "just warming up my neurons."
        elif move_num <= 8:
            phase = "welcome to the messy midgame."
        else:
            phase = "we’re in the part where one mistake ruins your entire day."

        return (
            f"{self.nickname}: choosing {self.last_move_coords} "
            f"({ab_tag}; cutoffs={cutoffs}, evals={evals}). "
            f"{phase} {body}"
        )

    def explain_last_move(self):
        """
       when opponent says 'Tell me how you did that',
        explain the last move using real search stats.
        """
        if self.last_move_coords is None:
            return f"{self.nickname}: let me actually make a serious move first, then i'll overshare."

        evals = self.num_static_evals_this_turn
        cutoffs = self.alpha_beta_cutoffs_this_turn
        entries = self.zobrist_table_num_entries_this_turn
        hits = self.zobrist_table_num_hits_this_turn
        t = self.last_move_time if self.last_move_time is not None else 0.0
        score = self.last_move_value if self.last_move_value is not None else 0.0

        msg = (
            f"{self.nickname}: i picked {self.last_move_coords} after evaluating "
            f"{evals} leaf positions and pruning {cutoffs} branches with alpha-beta. "
        )
        if entries >= 0:
            msg += f"i wrote {entries} entries into my hash table and reused {hits} of them. "
        msg += (
            f"my internal score for that board (from my point of view) is {score:.1f}. "
            f"and yes, it took me about {t:.3f} seconds—you're welcome."
        )
        return msg

    def summarize_game_so_far(self):
        """
        when opponent says
        'What's your take on the game so far?', tell a short story & prediction.
        """
        if not self.eval_history:
            return f"{self.nickname}: we literally just started. patience, bestie."

        start = self.eval_history[0]
        current = self.eval_history[-1]
        delta = current - start

        if abs(delta) < 200:
            arc = "honestly, it's been pretty back-and-forth so far."
        elif delta > 0:
            arc = "i've slowly wrestled the position in my favor."
        else:
            arc = "you've been making my life progressively harder, rude."

        if current > 400:
            outcome = "if we both keep playing decently, i'd bet on myself."
        elif current < -400:
            outcome = "if we both keep playing decently, i'd bet on you—grudgingly."
        else:
            outcome = "right now it’s basically a coin flip with attitude."

        return (
            f"{self.nickname}: story time. i started around {start:.1f}, "
            f"now we're at {current:.1f}. {arc} {outcome}"
        )


def slide_windows_over_lines(board, k):
        H, W = len(board), len(board[0])

        # rows
        for i in range(H):
            line = board[i]
            for j in range(W - k + 1):
                yield [(i, j + t) for t in range(k)], (i, j - 1), (i, j + k)

        # cols
        for j in range(W):
            col = [board[i][j] for i in range(H)]
            for i in range(H - k + 1):
                yield [(i + t, j) for t in range(k)], (i - 1, j), (i + k, j)

        # down right
        for i0 in range(H - k + 1):
            for j0 in range(W - k + 1):
                cells = [(i0 + t, j0 + t) for t in range(k)]
                before = (i0 - 1, j0 - 1)
                after = (i0 + k, j0 + k)
                yield cells, before, after

        # up right
        for i0 in range(k - 1, H):
            for j0 in range(W - k + 1):
                cells = [(i0 - t, j0 + t) for t in range(k)]
                before = (i0 + 1, j0 - 1)
                after  = (i0 - k, j0 + k)
                yield cells, before, after

# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances

def other(p):
    return 'O' if p == 'X' else 'X'

def move_gen(state):
    b = state.board
    p = state.whose_move
    o = other(p)
    mCols = len(b[0])
    nRows = len(b)
    for i in range(nRows):
        for j in range(mCols):
            if b[i][j] != ' ':
                continue
            news = State(old=state)
            news.board[i][j] = state.whose_move
            news.whose_move = o
            yield [(i, j), news]
# '''
# <yourUWNetID>_KInARow.py
# Authors: <your name(s) here, lastname first and partners separated by ";">
#   Example:
#     Authors: Smith, Jane; Lee, Laura

# An agent for playing "K-in-a-Row with Forbidden Squares" and related games.
# CSE 415, University of Washington

# THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
# YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
# TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

# '''

# from agent_base import KAgent
# from game_types import State, Game_Type
# from winTesterForK import winTesterForK

# AUTHORS = 'Jane Smith and Laura Lee'
# UWNETIDS = ['janiesmith99', 'laura2039'] # The first UWNetID here should
# # match the one in the file name, e.g., janiesmith99_KInARow.py.

# import time # You'll probably need this to avoid losing a
#  # game due to exceeding a time limit.

# # Create your own type of agent by subclassing KAgent:

# class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
#     # knows how to instantiate your agent class.

#     def __init__(self, twin=False):
#         self.twin=twin
#         self.nickname = 'quirk'
#         if twin: self.nickname += '2'
#         self.long_name = 'quirk(y)'
#         if twin: self.long_name += ' II'
#         self.persona = 'chaotic'
#         self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
#         self.playing = "O" # e.g., "X" or "O".
#         self.alpha_beta_cutoffs_this_turn = -1
#         self.num_static_evals_this_turn = -1
#         self.zobrist_table_num_entries_this_turn = -1
#         self.zobrist_table_num_hits_this_turn = -1
#         self.current_game_type = None
#         self.playing_mode = KAgent.DEMO

#     def introduce(self):
#         intro = '\nhey i am quirk(y).\n'+\
#             '"i was made by two very smart women in stem and my favorite hobby is to pretend to think slower so that humans feel better about themselves!\n'+\
#              "my humans: Saachi Dhamija (saachid) and Aishi Sharma (aishis).\n" +\
#             'i am a big fan of winning. if i say anything harsh (and i will), please do not take it to heart (actually i dont care)\n' +\
#             'let the games begin :):):):)\n'
#         if self.twin: intro += "i am the evil twin by the way, hey\n"
#         return intro

#     # Receive and acknowledge information about the game from
#     # the game master:
#     def prepare(
#         self,
#         game_type,
#         what_side_to_play,
#         opponent_nickname,
#         expected_time_per_move = 0.1, # Time limits can be
#                                       # changed mid-game by the game master.

#         utterances_matter=True):
#                                       # or something simple and quick to compute
#                                       # and do not import any LLM or special APIs.
#                                       # During the tournament, this will be False..
#        self.game_type = game_type
#        self.K = game_type.k
#        self.who_i_play = what_side_to_play
#        self.opponent_nickname = opponent_nickname
#        self.time_limit = expected_time_per_move
#        if utterances_matter:
#            pass
#            # Optionally, import your LLM API here.
#            # Then you can use it to help create utterances.

#        # Write code to save the relevant information in variables
#        # local to this instance of the agent.
#        # Game-type info can be in global variables.
#     #    print("OK")
#        return "OK"

#     def board_full(self, state):
#         return all(ch != ' ' for row in state.board for ch in row)

#     WIN_SCORE, LOSS_SCORE, DRAW_SCORE = 10**6, -10**6, 0

#     def eval_state(self, state):
#         if getattr(self, 'special_eval', None) is not None:
#             self.num_static_evals_this_turn += 1
#             return self.static_eval(state)
#         self.num_static_evals_this_turn += 1
#         return self.static_eval(state, self.game_type)

#     # The core of your agent's ability should be implemented here:
#     def make_move(self, current_state, current_remark, time_limit=1000,
#                   use_alpha_beta=True,
#                   use_zobrist_hashing=False, max_ply=3,
#                   special_static_eval_fn=None):
#         print("make_move has been called")

#         print("code to compute a good move should go here.")
#         # Here's a placeholder:
#         self.alpha_beta_cutoffs_this_turn = 0
#         self.num_static_evals_this_turn = 0

#         self.zobrist_table_num_entries_this_turn = -1
#         self.zobrist_table_num_hits_this_turn = -1

#         self.special_eval = special_static_eval_fn

#         alpha = float('-inf') if use_alpha_beta else None
#         beta = float('inf') if use_alpha_beta else None

#         best_move, best_state, best_score = self.minimax(current_state, max_ply, pruning=use_alpha_beta, time_limit=time_limit, alpha=alpha, beta=beta)

#         if best_move is None:
#             children = list(move_gen(current_state))
#             if children:
#                 best_move, best_state = children[0]
#             else:
#                 return [None, f"{self.nickname}: stalemate acknowledged"]

#         remark = f"{self.nickname}: choosing {best_move}. " \
#                  f"({ 'αβ on' if use_alpha_beta else 'αβ off' }; " \
#                  f"cutoffs={self.alpha_beta_cutoffs_this_turn}, evals={self.num_static_evals_this_turn})"

#         print("returning from make_move")
#         # return [[
#         #     best_move,
#         #     best_state,
#         #     self.alpha_beta_cutoffs_this_turn,
#         #     self.num_static_evals_this_turn,
#         #     self.zobrist_table_num_entries_this_turn,
#         #     self.zobrist_table_num_hits_this_turn
#         # ],
#         # remark]
#         return [[best_move, best_state], remark]
#         # return [[best_move, best_state, self.alpha_beta_cutoffs_this_turn, self.num_static_evals_this_turn, self.zobrist_table_num_entries_this_turn, self.zobrist_table_num_hits_this_turn], remark]
#         # a_default_move = (0, 0) # This might be legal ONCE in a game,
#         # # if the square is not forbidden or already occupied.

#         # new_state = current_state # This is not allowed, and even if
#         # # it were allowed, the newState should be a deep COPY of the old.

#         # new_remark = "I need to think of something appropriate.\n" +\
#         # "Well, I guess I can say that this move is probably illegal."

#         # print("Returning from make_move")
#         # return [[a_default_move, new_state], new_remark]

#     # The main adversarial search function:
#     def minimax(self,
#             state,
#             depth_remaining,
#             pruning=False,
#             time_limit=None,
#             alpha=None,
#             beta=None):
#         # print("Calling minimax. We need to implement its body.")

#         player_to_move = state.whose_move
#         maximizing = (player_to_move == self.who_i_play)

#         if depth_remaining == 0:
#             self.num_static_evals_this_turn += 1
#             if hasattr(self, "special_eval") and self.special_eval:
#                 raw_score = self.special_eval(state)
#             else:
#                 raw_score = self.static_eval(state, self.game_type)
#             score = raw_score if self.who_i_play == 'X' else -raw_score
#             return (None, None, score)
#         # need to see if current state is win state
#         #
#         #
#         #

#         children = list(move_gen(state))
#         if not children:
#             return (None, None, 0)

#         best_move = None
#         best_score = float('-inf') if maximizing else float('inf')
#         best_state = None

#         if pruning:
#             if alpha is None: alpha = float('-inf')
#             if beta is None: beta = float('inf')

#         for move, child in children:
#             # check for win o child using last move
#             win_message = winTesterForK(child, move, self.K)
#             if win_message != 'No win':
#                 who_went = child.board[move[0]][move[1]]
#                 score = (10**6) if who_went == self.who_i_play else -(10**6)
#             elif all(ch != ' ' for row in child.board for ch in row):
#                 score = 0
#             else:
#                 _, _, raw = self.minimax(child, depth_remaining - 1, pruning=pruning, alpha=alpha, beta=beta)
#                 score = raw
#             if maximizing:
#                 if score > best_score:
#                     best_score = score
#                     best_move = move
#                     best_state = child
#                 if pruning:
#                     alpha = max(alpha, best_score)
#                     if alpha >= beta: #prune condition
#                         self.alpha_beta_cutoffs_this_turn += 1
#                         break
#             else: # minimizing
#                 if score < best_score:
#                     best_score = score
#                     best_move = move
#                     best_state =child
#                 if pruning:
#                     beta = min(beta, best_score)
#                     if alpha >= beta: #prune condition again
#                         self.alpha_beta_cutoffs_this_turn += 1
#                         break

#         return (best_move, best_state, best_score)
#         # full = all(ch != ' ' for row in state.board for ch in row)

#         # # need to detect a win -> check in children nodes; dont know last move with root node

#         # default_score = float('-inf') # Value of the passed-in state. Needs to be computed.


#         # return [default_score, "my own optional stuff", "more of my stuff"]
#         # Only the score is required here but other stuff can be returned
#         # in the list, after the score, in case you want to pass info
#         # back from recursive calls that might be used in your utterances,
#         # etc.

#         # --- inside your agent class ---
#     def static_eval(self, state, game_type=None):
#         # Values should be higher when better for X, lower when better for O.
#         b = state.board
#         k = (game_type.k if game_type else getattr(self, 'K', 3))
#         H, W = len(b), len(b[0])

#         # weights (TTT defaults; scale up for FIAR)
#         if k == 3:
#             base = {1: 10, 2: 120}           # value per streak length
#             gamma = 0.8
#         else:
#             base = {1: 3, 2: 30, 3: 600, 4: 10_000}
#             gamma = 0.93
#         liberty_bonus = {0: 0, 1: 1, 2: 3}

#         # features
#         x_open_k1 = o_open_k1 = 0
#         x_dbl_k2  = o_dbl_k2  = 0
#         window_value = 0

#         def cell(i, j):
#             return b[i][j] if (0 <= i < H and 0 <= j < W) else None

#         # Slide every k-window across rows/cols/diags
#         for cells, before, after in slide_windows_over_lines(b, k):
#             marks = [cell(i, j) for (i, j) in cells]
#             x = marks.count('X'); o = marks.count('O')

#             # terminal detection (covers all directions)
#             if x == k and o == 0:
#                 return 1_000_000
#             if o == k and x == 0:
#                 return -1_000_000

#             # skip contested windows
#             if x and o:
#                 continue

#             # openness (ends)
#             left  = cell(*before)
#             right = cell(*after)
#             opens = (1 if left  == ' ' else 0) + (1 if right == ' ' else 0)

#             # streak scoring
#             if x and not o:
#                 L = x
#                 if L in base:
#                     window_value += base[L] * liberty_bonus.get(opens, 0)
#             elif o and not x:
#                 L = o
#                 if L in base:
#                     window_value -= base[L] * liberty_bonus.get(opens, 0)

#             # threat counters
#             if x == k - 1 and o == 0 and opens >= 1: x_open_k1 += 1
#             if o == k - 1 and x == 0 and opens >= 1: o_open_k1 += 1
#             if k >= 4:
#                 if x == k - 2 and o == 0 and opens == 2: x_dbl_k2 += 1
#                 if o == k - 2 and x == 0 and opens == 2: o_dbl_k2 += 1

#         # Layer 2: danger bias + fork bonus
#         if o_open_k1 > 0:
#             window_value -= (50_000 if k == 3 else 200_000)

#         fork_bonus = 0
#         if k == 3:
#             fork_bonus += 2000 * x_dbl_k2
#             fork_bonus -= 2000 * o_dbl_k2
#         else:
#             fork_bonus += 1500 * x_dbl_k2
#             fork_bonus -= 1500 * o_dbl_k2

#         # Layer 3: positional shaping (TTT)
#         positional = 0
#         if k == 3 and H == 3 and W == 3:
#             c = b[1][1]
#             if c == 'X': positional += 3
#             elif c == 'O': positional -= 3
#             corners = [b[0][0], b[0][2], b[2][0], b[2][2]]
#             positional += corners.count('X') - corners.count('O')

#         # “MDP-ish” continuation: discount difference in open (k-1)
#         continuation = gamma * (x_open_k1 - o_open_k1)

#         # Mode switch
#         if o_open_k1 > 0 or (k >= 4 and o_dbl_k2 > 0):
#             mode_mult = 0.9      # defense: dampen greed a bit
#         elif x_open_k1 > 0 and o_open_k1 == 0:
#             mode_mult = 1.1      # offense: lean into growth
#         else:
#             mode_mult = 1.0

#         total = mode_mult * window_value + fork_bonus + positional + continuation
#         return float(total)

# def slide_windows_over_lines(board, k):
#         H, W = len(board), len(board[0])

#         # rows
#         for i in range(H):
#             line = board[i]
#             for j in range(W - k + 1):
#                 yield [(i, j + t) for t in range(k)], (i, j - 1), (i, j + k)

#         # cols
#         for j in range(W):
#             col = [board[i][j] for i in range(H)]
#             for i in range(H - k + 1):
#                 yield [(i + t, j) for t in range(k)], (i - 1, j), (i + k, j)

#         # down right
#         for i0 in range(H - k + 1):
#             for j0 in range(W - k + 1):
#                 cells = [(i0 + t, j0 + t) for t in range(k)]
#                 before = (i0 - 1, j0 - 1)
#                 after = (i0 + k, j0 + k)
#                 yield cells, before, after

#         # up right
#         for i0 in range(k - 1, H):
#             for j0 in range(W - k + 1):
#                 cells = [(i0 - t, j0 + t) for t in range(k)]
#                 before = (i0 + 1, j0 - 1)
#                 after  = (i0 - k, j0 + k)
#                 yield cells, before, after

# # OPTIONAL THINGS TO KEEP TRACK OF:

# #  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
# #  MY_PAST_UTTERANCES = []
# #  OPPONENT_PAST_UTTERANCES = []
# #  UTTERANCE_COUNT = 0
# #  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances

# def other(p):
#     return 'O' if p == 'X' else 'X'

# def move_gen(state):
#     b = state.board
#     p = state.whose_move
#     o = other(p)
#     mCols = len(b[0])
#     nRows = len(b)
#     for i in range(nRows):
#         for j in range(mCols):
#             if b[i][j] != ' ':
#                 continue
#             news = State(old=state)
#             news.board[i][j] = state.whose_move
#             news.whose_move = o
#             yield [(i, j), news]