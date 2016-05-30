from hearthbreaker.engine import *
import random
import collections
import queue
from projectfiles.util import *

class ActionTreeNode():
    def __init__(self, game_state, state_set = None, parent = None, action = GameHelper.NO_ACTION) # , function_approximator = None):
        self.game = game_state
        self.parent = parent
        self.action = action
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1
        if state_set is None:
            self.state_set = parent.state_set
        else:
            self.state_set = state_set
        self.children = []

    def generate_children(self):
        actions = GameHelper.generate_actions(self.game)
        for action in actions:
            new_game = game.copy()
            GameHelper.execute(new_game, action)
            new_game_hash = GameHelper.hashgame(game);
            if not (new_game_hash in self.state_set):
                self.state_set.add(new_game_hash)
                self.children.append(ActionTreeNode(game_state = new_game, parent = self, action = action))

    def get_outcomes(self):
        if self.visited: return []
        outcome = [] # action_list game(reference)
        outcome.append(self.game)
        for [action, strategy] in self.substrategies:
            outcome += strategy.get_outcomes()
        return outcome

    def get_optimal(self, approximator, original_state, ans_pair):
        if self.visited: return
        value = approximator(original_state, self.game)
        if (value > ans_pair[0]):
            ans_pair[0] = value
            ans_pair[1] = self.game
        ans_pair[2] += 1
        if (ans_pair[2] > 100): return
        for [action, strategy] in self.substrategies:
            strategy.get_optimal(approximator, original_state, ans_pair)
            if (ans_pair[2] > 100): return

class ActionTreeManager():
    def __init__(self):
        self.clear()

    def encounter(self, game_state):
        self.root = ActionTreeNode(game_state = game_state, state_set = self.state_set)

    def think_fully(self):
        self.game_states_to_think = queue.Queue()
        

    def clear(self):
        self.state_set = set()
        self.root = None