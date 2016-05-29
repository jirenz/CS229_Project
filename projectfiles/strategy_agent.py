from hearthbreaker.agents.basic_agents import *
import collections
import numpy as np
from projectfiles.feature_extract import *
from learning.strategy import *

class StrategyAgent(DoNothingAgent):
	def __init__(self): # eta, explore_prob, discount, feature_extractor, learn = True):
		super().__init__()

	def do_card_check(self, cards):
		return [True, True, True, True]

	def do_turn(self, player):
		game = player.game
		action = self.decide(game)
		if action:
			GameHelper.execute(game, action)
		else: 
			return

	def choose_target(self, targets):
		raise
		return
		# return self.machine.choose_target(targets)

	def choose_index(self, card, player):
		raise
		return # self.machine.choose_index(card, player)

	def choose_option(self, options, player):
		raise
		# options = self.filter_options(options, player)
		return # self.machine.choose_option(options, player)

	def decide(self, game)

		return action
