from hearthbreaker.engine import *
import random
import collections
import queue
from projectfiles.util import *

class ActionTreeNode():
    def __init__(self, game_state, state_set = None, parent = None, action = GameHelper.NO_ACTION): # , function_approximator = None):
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
        self.priority = 0

    def __lt__(self, other):
        return (self.priority, random.random()) < (other.priority, random.random())


    def generate_children(self):
        actions = GameHelper.generate_actions(self.game)
        for action in actions:
            new_game = self.game.copy()
            GameHelper.execute(new_game, action)
            new_game_hash = GameHelper.hashgame(new_game);
            if not (new_game_hash in self.state_set):
                self.state_set.add(new_game_hash)
                self.children.append(ActionTreeNode(game_state = new_game, parent = self, action = action))
                if new_game.current_player_win():
                    print("Found Lethal")
                    return True # found lethal, no need to proceed
        return False

    def find_best_action(self, function_approximator):
        max_value = function_approximator(self.game)
        max_action = GameHelper.NO_ACTION
        for child in self.children:
            new_value = child.eval(function_approximator)
            if new_value > max_value:
                max_value = new_value
                max_action = child.action
        # print("Max value: " + str(max_value))
        return max_action

    def eval(self, function_approximator):
        max_value = function_approximator(self.game)
        for child in self.children:
            new_value = child.eval(function_approximator)
            if new_value > max_value:
                max_value = new_value
        return max_value

    def select_best_child(self, function_approximator):
        max_value = function_approximator(self.game)
        best_child = None
        for child in self.children:
            new_value = function_approximator(child.game)
            if new_value > max_value:
                max_value = new_value
                best_child = child
        return best_child

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
        if self.root is None: raise("Unnitialized root for growing.")
        q = queue.Queue()
        q.put(self.root)
        while not q.empty():
            node = q.get()
            node.generate_children()
            for child in node.children:
                q.put(child)

    def think_depth(self, depth = 1):
        if self.root is None: raise("Unnitialized root for growing.")
        q = queue.Queue()
        q.put(self.root)
        while not q.empty():
            # print("advance!")
            node = q.get()
            if node.depth <= depth:
                node.generate_children()
                for child in node.children:
                    q.put(child)

    def think_1(self, function_approximator, depth = 1):
        if self.root is None: raise("Unnitialized root for growing.")
        q = queue.Queue()
        q.put(self.root)
        while not q.empty():
            # print("advance!")
            node = q.get()
            if node.depth <= depth:
                node.generate_children()
                for child in node.children:
                    q.put(child)
            else:
                node.generate_children()
                best = node.select_best_child(function_approximator)
                if not best is None:
                    q.put(best)

    def think_2(self, function_approximator, depth = 1, budget = 30):
        if self.root is None: raise("Unnitialized root for growing.")
        q = queue.PriorityQueue()
        q.put(self.root)
        i = 0
        while not q.empty():
            # print("advance!")
            node = q.get()
            if node.depth <= depth:
                if node.generate_children(): break
                for child in node.children:
                    child.priority = child.depth * 2 - function_approximator(child.game)
                    q.put(child)
            else:
                if node.generate_children(): break
                best = node.select_best_child(function_approximator)
                if not best is None:
                    best.priority = best.depth * 2 - function_approximator(best.game)
                    q.put(best)
            i += 1
            if i > budget:
                break

    #deprecated
    def branch_think(self, branching_decider = None):
        if branching_decider is None:
            branching_decider = BasicBrachingDecider()

    def clear(self):
        self.state_set = set()
        self.root = None

    def find_best_action(self, function_approximator):
        return self.root.find_best_action(function_approximator)

class BasicBrachingDecider():
    def __init__(self, base_factor = 20):
        self.base_factor = base_factor

    def decide(self):
        pass