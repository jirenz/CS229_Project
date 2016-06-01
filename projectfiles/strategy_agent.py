from hearthbreaker.agents.basic_agents import *
import collections
from projectfiles.feature_extract import *
from learning.strategy import *
import json
from projectfiles.tree_manager import *

class StrategyAgent(DoNothingAgent):
    def __init__(self, function_approximator = None, name = 'StrategyAgent', max_depth = 2): # eta, explore_prob, discount, feature_extractor, learn = True):
        super().__init__()
        self.name = name
        self.function_approximator = function_approximator if function_approximator is not None else BasicHeuristicModel()
        self.max_depth = max_depth

    def do_card_check(self, cards):
        return [True, True, True, True]

    def do_turn(self, player):
        self.player = player
        game = player.game
        while True:
            self.action = self.decide(game)
            GameHelper.execute(game, self.action)

            if self.action == GameHelper.NO_ACTION:
                print("Me: " + str(player.hero.health) + " Opponent: " + str(game.other_player.hero.health))
                return

    def choose_target(self, targets):
        print("Warning: Deciding target through Strategy Agent")
        # raise Exception("asked to choose target")
        if self.action[2] is not None and self.action[2] < len(targets):
            return targets[self.action[2]]
        else:
            return targets[random.randint(0, len(targets) - 1)]
        # return self.machine.choose_target(targets)

    def choose_index(self, card, player):
        print("Warning: Deciding index through Strategy Agent")
        if self.action[1] is not None: 
            return self.action[1]
        else:
            return 0
        # raise Exception("asked to choose index")
        # self.machine.choose_index(card, player)

    def choose_option(self, options, player):
        print("Warning: Deciding option through Strategy Agent")
        # raise Exception("asked to choose option")
        # options = self.filter_options(options, player)
        return options[random.randint(0, len(options) - 1)]

    def decide(self, game):
        manager = ActionTreeManager(depth = self.max_depth)
        manager.encounter(game)
        manager.think(self.function_approximator)
        return manager.find_best_action(self.function_approximator)

        # max_value = -1000
        # max_action = GameHelper.NO_ACTION
        # actions = GameHelper.generate_actions(game)
        # for action in actions:
        #   new_game = game.copy()
        #   GameHelper.execute(new_game, action)
        #   new_value = self.function_approximator.eval(None, new_game)
        #   if new_value > max_value:
        #       max_value = new_value
        #       max_action = action
        # print("BEST:", max_action, max_value)
        # return max_action
