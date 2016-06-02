from hearthbreaker.engine import *
import random
import collections
import queue
from projectfiles.util import *

class ActionTreeNode():
    def __init__(self, game_state, state_set = None, parent = None, depth = 2, action = GameHelper.NO_ACTION): # , model = None):
        self.game = game_state
        self.parent = parent
        self.action = action
        self.depth = depth
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

    def find_best_action(self, initial_game, model):
        max_action = GameHelper.NO_ACTION
        max_value = model(initial_game, self.game)
        for child in self.children:
            new_value = child.eval(initial_game, model)
            if new_value > max_value:
                max_value = new_value
                max_action = child.action
        # print("Max value: " + str(max_value))
        return max_action

    def eval(self, initial_game, model):
        max_value = model(initial_game, self.game)
        for child in self.children:
            new_value = child.eval(initial_game, model)
            if new_value > max_value:
                max_value = new_value
        return max_value

    def select_best_child(self, initial_game, model):
        max_value = model(initial_game, self.game)
        best_child = []
        for child in self.children:
            new_value = model(initial_game, child.game)
            if new_value > max_value:
                max_value = new_value
                best_child = [child]
        return best_child

class ActionTreeManager():
    def __init__(self, depth = 2, budget = 15):
        self.budget = budget
        self.depth = depth
        self.clear()

    def encounter(self, game_state):
        self.root = ActionTreeNode(game_state = game_state, state_set = self.state_set)

    # def think_depth(self):
    #   if self.root is None: raise("Unnitialized root for growing.")
    #   q = collections.deque()
    #   q.append(self.root)
    #   while len(q) > 0:
    #       # print("advance!")
    #       node = q.popleft()
    #       if node.depth <= self.depth:
    #           node.generate_children()
    #           for child in node.children:
    #               q.append(child)

    #def think_1(self, model):
    #   if self.root is None: raise("Unnitialized root for growing.")
    #   q = collections.deque()
    #   q.append(self.root)
    #   while len(q) > 0:
    #       # print("advance!")
    #       node = q.popleft()
    #       if node.depth <= self.depth:
    #           node.generate_children()
    #           for child in node.children:
    #               q.append(child)
    #       else:
    #           node.generate_children()
    #           best = node.select_best_child(self.root.game, model)
    #           if not best is None:
    #               q.append(best)

    def think(self, model):
        if self.root is None: raise("Unnitialized root for growing.")
        q = queue.PriorityQueue()
        q.put(self.root)
        i = 0
        while not q.empty():
            node = q.get()
            if node.generate_children(): break
            if node.depth <= self.depth:
                for child in node.children:
                    child.priority = self.depth_function(child.depth) - model(self.root.game, child.game)
                    q.put(child)
            else:
                for best in node.select_best_child(self.root.game, model):
                    best.priority = self.depth_function(best.depth) - model(self.root.game, child.game)
                    q.put(best)
            i += 1
            if i > self.budget:
                break

    def depth_function(self, new_node_depth):
        return 2 * new_node_depth

    def clear(self):
        self.state_set = set()
        self.root = None

    def find_best_action(self, model):
        return self.root.find_best_action(self.root.game, model)
