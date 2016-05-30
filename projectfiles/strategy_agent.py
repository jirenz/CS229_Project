from hearthbreaker.agents.basic_agents import *
import collections
from projectfiles.feature_extract import *
from learning.strategy import *
from learning.function_approximator import *
import json

class StrategyAgent(DoNothingAgent):
	def __init__(self): # eta, explore_prob, discount, feature_extractor, learn = True):
		super().__init__()

	def do_card_check(self, cards):
		return [True, True, True, True]

	def do_turn(self, player):
		self.player = player
		game = player.game
		while True:
			self.action = self.decide(game)
			GameHelper.execute(game, self.action)
			# print("Me: " + str(player.hero.health) + " Him: " + str(game.other_player.hero.health))
			if self.action == "No_Action":
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
		return self.action[1]
		# raise Exception("asked to choose index")
		# self.machine.choose_index(card, player)

	def choose_option(self, options, player):
		print("Warning: Deciding option through Strategy Agent")
		# raise Exception("asked to choose option")
		# options = self.filter_options(options, player)
		return # self.machine.choose_option(options, player)

	def decide(self, game):
		max_value = -1000
		max_action = "No_Action"
		actions = GameHelper.generate_actions(game)
		for action in actions:
			new_game = game.copy()
			GameHelper.execute(new_game, action)
			new_value = BasicFunctionApproximator.eval(None, new_game)
			if new_value > max_value:
				max_value = new_value
				max_action = action
		return max_action
