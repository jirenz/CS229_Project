from hearthbreaker.agents.basic_agents import *
import collections
import numpy as np
from projectfiles.feature_extract import *
from learning.strategy import *

class StrategyAgent(DoNothingAgent, GameHelper):
	def __init__(self, function_approximator): # eta, explore_prob, discount, feature_extractor, learn = True):
		super().__init__()
		self.strategy_manager = StrategyManager(function_approximator)

	def do_card_check(self, cards):
		return [True, True, True, True]

	def do_turn(self, player):
		self.player = player
		game = self.player.game
		self.strategy_manager.clear()
		self.strategy_manager.think(game)
		action_list = self.strategy_manager.best_action_list()
		score = action_list[0]
		actions = action_list[1]
		print("Using strategy with score: " + str(score) + ", number of actions: " + str(len(actions)))
		for action in actions:
			print(str(action))
			self.excecute(game, action)
		return

	def choose_target(self, targets):
		raise
		return self.machine.choose_target(targets)

	def choose_index(self, card, player):
		raise
		return self.machine.choose_index(card, player)

	def choose_option(self, options, player):
		raise
		options = self.filter_options(options, player)
		return self.machine.choose_option(options, player)
